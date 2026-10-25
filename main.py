"""Sistem Pencarian Buku dengan Linear Search dan Binary Search.

Dataset dibaca dari CSV. Implementasi algoritma pencarian dibuat manual,
 tanpa list.index(), operator `in` untuk mencari data, atau library pencarian.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path
from typing import Any


UKURAN_UJI = (100, 1_000, 10_000)
FOLDER_OUTPUT = Path("output")


def normalisasi(teks: Any) -> str:
    """Ubah nilai menjadi teks yang siap dibandingkan tanpa membedakan kapital."""
    if teks is None:
        return ""
    return str(teks).strip().casefold()


def normalisasi_nama_kolom(nama: str) -> str:
    """Samakan format nama kolom, misalnya 'Book Title' menjadi 'booktitle'."""
    return "".join(karakter.lower() for karakter in nama if karakter.isalnum())


def baca_dataset(lokasi_csv: str | Path) -> tuple[list[dict[str, str]], list[str]]:
    """Baca file CSV dan kembalikan data buku serta daftar nama kolom."""
    path = Path(lokasi_csv)
    if not path.is_file():
        raise FileNotFoundError(f"File dataset tidak ditemukan: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file_csv:
        contoh = file_csv.read(4096)
        file_csv.seek(0)
        try:
            format_csv = csv.Sniffer().sniff(contoh, delimiters=",;\t")
        except csv.Error:
            format_csv = csv.excel

        pembaca = csv.DictReader(file_csv, dialect=format_csv)
        if not pembaca.fieldnames:
            raise ValueError("CSV tidak memiliki header/nama kolom.")

        kolom = [str(nama).strip() for nama in pembaca.fieldnames if nama]
        if not kolom:
            raise ValueError("Nama kolom pada CSV tidak valid.")

        daftar_buku: list[dict[str, str]] = []
        for baris in pembaca:
            buku = {
                kolom_asli: str(baris.get(kolom_asli) or "").strip()
                for kolom_asli in kolom
            }
            # Abaikan baris yang seluruh isinya kosong.
            ada_isi = False
            for nilai in buku.values():
                if nilai != "":
                    ada_isi = True
                    break
            if ada_isi:
                daftar_buku.append(buku)

    if not daftar_buku:
        raise ValueError("CSV berhasil dibaca, tetapi tidak berisi data buku.")
    return daftar_buku, kolom


def cari_kolom_judul(kolom: list[str]) -> str:
    """Temukan kolom judul buku dengan beberapa nama yang umum digunakan."""
    kandidat_judul = {
        "title", "booktitle", "bookname", "nameofbook", "judul",
        "judulbuku", "booktitletext",
    }
    for nama in kolom:
        if normalisasi_nama_kolom(nama) in kandidat_judul:
            return nama
    return kolom[0]


def linear_search(
    daftar_buku: list[dict[str, str]], kolom_cari: str, target: str
) -> tuple[dict[str, str] | None, int]:
    """Cari dari elemen pertama sampai ditemukan/daftar habis.

    Nilai balik: (buku yang ditemukan atau None, jumlah perbandingan nilai).
    Satu perbandingan kesamaan nilai dihitung untuk setiap buku yang diperiksa.
    """
    target_normal = normalisasi(target)
    jumlah_perbandingan = 0

    for buku in daftar_buku:
        jumlah_perbandingan += 1
        if normalisasi(buku.get(kolom_cari, "")) == target_normal:
            return buku, jumlah_perbandingan

    return None, jumlah_perbandingan


def binary_search(
    daftar_buku_terurut: list[dict[str, str]], kolom_cari: str, target: str
) -> tuple[dict[str, str] | None, int]:
    """Cari dengan bagi-dua pada data yang SUDAH diurutkan berdasarkan kolom.

    Setiap operator perbandingan nilai (== atau <) dihitung satu operasi.
    Data harus terurut berdasarkan kolom_cari menggunakan normalisasi yang sama.
    """
    target_normal = normalisasi(target)
    kiri = 0
    kanan = len(daftar_buku_terurut) - 1
    jumlah_perbandingan = 0

    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        nilai_tengah = normalisasi(daftar_buku_terurut[tengah].get(kolom_cari, ""))

        jumlah_perbandingan += 1
        if nilai_tengah == target_normal:
            return daftar_buku_terurut[tengah], jumlah_perbandingan

        jumlah_perbandingan += 1
        if nilai_tengah < target_normal:
            kiri = tengah + 1
        else:
            kanan = tengah - 1

    return None, jumlah_perbandingan


def pilih_kolom(kolom: list[str], kolom_default: str) -> str:
    """Minta pengguna memilih kolom yang akan dijadikan kunci pencarian."""
    print("\nKolom yang bisa digunakan untuk pencarian:")
    for nomor, nama in enumerate(kolom, start=1):
        penanda = " (default)" if nama == kolom_default else ""
        print(f"  {nomor}. {nama}{penanda}")

    jawaban = input(f"Pilih nomor kolom [Enter = {kolom_default}]: ").strip()
    if jawaban == "":
        return kolom_default
    try:
        nomor_kolom = int(jawaban)
        if 1 <= nomor_kolom <= len(kolom):
            return kolom[nomor_kolom - 1]
    except ValueError:
        pass

    print("Pilihan tidak valid. Kolom default digunakan:", kolom_default)
    return kolom_default


def tampilkan_buku(buku: dict[str, str], maksimal_kolom: int = 8) -> None:
    """Tampilkan beberapa kolom buku supaya hasil tetap mudah dibaca."""
    ditampilkan = 0
    for nama_kolom, nilai in buku.items():
        if nilai:
            nilai_tampil = nilai if len(nilai) <= 100 else nilai[:97] + "..."
            print(f"  {nama_kolom}: {nilai_tampil}")
            ditampilkan += 1
            if ditampilkan >= maksimal_kolom:
                break
    if ditampilkan == 0:
        print("  (Data buku tidak memiliki nilai yang bisa ditampilkan.)")


def lakukan_pencarian(
    daftar_buku: list[dict[str, str]], kolom_cari: str, target: str
) -> None:
    """Jalankan kedua algoritma, lalu tampilkan hasil, perbandingan, dan waktu."""
    # Pengurutan dilakukan sebelum timer Binary Search dimulai.
    daftar_terurut = sorted(
        daftar_buku,
        key=lambda buku: normalisasi(buku.get(kolom_cari, "")),
    )

    mulai_linear = time.perf_counter()
    hasil_linear, banding_linear = linear_search(daftar_buku, kolom_cari, target)
    waktu_linear_ms = (time.perf_counter() - mulai_linear) * 1_000

    mulai_binary = time.perf_counter()
    hasil_binary, banding_binary = binary_search(daftar_terurut, kolom_cari, target)
    waktu_binary_ms = (time.perf_counter() - mulai_binary) * 1_000

    print("\n=== HASIL LINEAR SEARCH ===")
    if hasil_linear is None:
        print("Buku tidak ditemukan.")
    else:
        print("Buku ditemukan:")
        tampilkan_buku(hasil_linear)
    print(f"Jumlah perbandingan : {banding_linear}")
    print(f"Waktu pencarian     : {waktu_linear_ms:.6f} ms")

    print("\n=== HASIL BINARY SEARCH ===")
    if hasil_binary is None:
        print("Buku tidak ditemukan.")
    else:
        print("Buku ditemukan:")
        tampilkan_buku(hasil_binary)
    print(f"Jumlah perbandingan : {banding_binary}")
    print(f"Waktu pencarian     : {waktu_binary_ms:.6f} ms")
    print("Catatan: waktu Binary Search tidak memasukkan waktu pengurutan data.")


def buat_grafik(hasil: list[dict[str, str | int | float]]) -> None:
    """Simpan grafik waktu dan jumlah perbandingan, jika matplotlib tersedia."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib belum terpasang; tabel dan CSV tetap dibuat.")
        print("Pasang grafik dengan perintah: pip install matplotlib")
        return

    FOLDER_OUTPUT.mkdir(parents=True, exist_ok=True)
    ukuran = [int(baris["n"]) for baris in hasil]

    plt.figure(figsize=(8, 5))
    plt.plot(ukuran, [float(baris["linear_ms"]) for baris in hasil], marker="o", label="Linear Search")
    plt.plot(ukuran, [float(baris["binary_ms"]) for baris in hasil], marker="o", label="Binary Search")
    plt.xlabel("Jumlah data buku (n)")
    plt.ylabel("Rata-rata waktu pencarian (ms)")
    plt.title("Perbandingan Waktu Pencarian")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FOLDER_OUTPUT / "grafik_waktu.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(ukuran, [int(baris["linear_comparisons"]) for baris in hasil], marker="o", label="Linear Search")
    plt.plot(ukuran, [int(baris["binary_comparisons"]) for baris in hasil], marker="o", label="Binary Search")
    plt.xlabel("Jumlah data buku (n)")
    plt.ylabel("Jumlah operasi perbandingan")
    plt.title("Perbandingan Operasi Pencarian")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FOLDER_OUTPUT / "grafik_perbandingan.png", dpi=150)
    plt.close()
    print("Grafik tersimpan di output/grafik_waktu.png dan output/grafik_perbandingan.png")


def benchmark(
    daftar_buku: list[dict[str, str]], kolom_cari: str
) -> list[dict[str, str | int | float]]:
    """Uji n=100, 1.000, 10.000. Target benchmark sengaja berupa nilai tak cocok."""
    hasil: list[dict[str, str | int | float]] = []
    print("\n=== BENCHMARK ALGORITMA ===")
    print("Benchmark menggunakan target yang sengaja tidak ditemukan agar Linear Search memeriksa seluruh data.")
    print("Waktu pengurutan untuk Binary Search tidak termasuk dalam waktu pencarian.")

    for n in UKURAN_UJI:
        if len(daftar_buku) < n:
            print(f"n={n:,} dilewati: dataset hanya memiliki {len(daftar_buku):,} baris.")
            continue

        sampel = daftar_buku[:n]
        daftar_terurut = sorted(
            sampel,
            key=lambda buku: normalisasi(buku.get(kolom_cari, "")),
        )
        target_uji = f"__TARGET_BENCHMARK_TIDAK_DITEMUKAN___{n}__"

        # Hitung operasi untuk satu pencarian, terpisah dari pengukuran waktu berulang.
        _, perbandingan_linear = linear_search(sampel, kolom_cari, target_uji)
        _, perbandingan_binary = binary_search(daftar_terurut, kolom_cari, target_uji)

        # Ulangi pencarian supaya waktu sangat singkat masih bisa diukur lebih stabil.
        pengulangan = max(10, min(100, 100_000 // n))
        mulai = time.perf_counter()
        for _ in range(pengulangan):
            linear_search(sampel, kolom_cari, target_uji)
        waktu_linear_ms = (time.perf_counter() - mulai) * 1_000 / pengulangan

        mulai = time.perf_counter()
        for _ in range(pengulangan):
            binary_search(daftar_terurut, kolom_cari, target_uji)
        waktu_binary_ms = (time.perf_counter() - mulai) * 1_000 / pengulangan

        hasil.append({
            "n": n,
            "kolom": kolom_cari,
            "target_uji": target_uji,
            "linear_comparisons": perbandingan_linear,
            "binary_comparisons": perbandingan_binary,
            "linear_ms": round(waktu_linear_ms, 8),
            "binary_ms": round(waktu_binary_ms, 8),
            "pengulangan_waktu": pengulangan,
        })

    if not hasil:
        print("Belum ada ukuran uji yang memenuhi. Pastikan dataset memiliki setidaknya 100 baris.")
        return hasil

    print("\nTabel hasil pengujian (waktu adalah rata-rata per pencarian):")
    print(f"{'n':>8} | {'Linear cmp':>11} | {'Binary cmp':>11} | {'Linear ms':>12} | {'Binary ms':>12}")
    print("-" * 67)
    for baris in hasil:
        print(
            f"{int(baris['n']):>8,} | {int(baris['linear_comparisons']):>11,} | "
            f"{int(baris['binary_comparisons']):>11,} | {float(baris['linear_ms']):>12.6f} | "
            f"{float(baris['binary_ms']):>12.6f}"
        )

    FOLDER_OUTPUT.mkdir(parents=True, exist_ok=True)
    path_hasil = FOLDER_OUTPUT / "hasil_benchmark.csv"
    with path_hasil.open("w", encoding="utf-8-sig", newline="") as file_csv:
        nama_kolom = list(hasil[0].keys())
        penulis = csv.DictWriter(file_csv, fieldnames=nama_kolom)
        penulis.writeheader()
        penulis.writerows(hasil)
    print(f"\nTabel hasil tersimpan di: {path_hasil}")
    buat_grafik(hasil)
    return hasil


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sistem pencarian data buku dengan Linear Search dan Binary Search."
    )
    parser.add_argument(
        "--data",
        default="dataset/books.csv",
        help="Lokasi file dataset CSV (default: dataset/books.csv).",
    )
    args = parser.parse_args()

    try:
        daftar_buku, kolom = baca_dataset(args.data)
    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"ERROR: {error}")
        print("\nCara menyiapkan dataset:")
        print("1. Unduh dataset dari tautan Kaggle pada README.md.")
        print("2. Ekstrak file CSV dan letakkan di folder dataset/.")
        print("3. Ubah nama file menjadi books.csv atau jalankan: python main.py --data path/file.csv")
        return 1

    kolom_default = cari_kolom_judul(kolom)
    print("=" * 58)
    print(" SISTEM PENCARIAN DATA BUKU PERPUSTAKAAN DIGITAL")
    print("=" * 58)
    print(f"Dataset           : {args.data}")
    print(f"Jumlah data buku  : {len(daftar_buku):,}")
    print(f"Jumlah kolom      : {len(kolom)}")
    print(f"Kolom default     : {kolom_default}")

    while True:
        print("\nMENU UTAMA")
        print("1. Cari buku (Linear Search dan Binary Search)")
        print("2. Uji kinerja (n = 100, 1.000, 10.000)")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            kolom_cari = pilih_kolom(kolom, kolom_default)
            target = input(f"Masukkan nilai {kolom_cari} yang dicari: ").strip()
            if target == "":
                print("Kata kunci tidak boleh kosong.")
                continue
            lakukan_pencarian(daftar_buku, kolom_cari, target)
        elif pilihan == "2":
            kolom_cari = pilih_kolom(kolom, kolom_default)
            benchmark(daftar_buku, kolom_cari)
        elif pilihan == "0":
            print("Program selesai. Terima kasih.")
            return 0
        else:
            print("Pilihan tidak dikenal. Masukkan 1, 2, atau 0.")


if __name__ == "__main__":
    sys.exit(main())
