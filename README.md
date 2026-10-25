# Sistem Pencarian Data Buku Perpustakaan Digital

Proyek Python untuk membandingkan algoritma **Linear Search** dan **Binary Search** pada dataset buku CSV dari Kaggle.

## Sumber dataset

Unduh dataset dari tautan yang diberikan pada tugas:

<https://www.kaggle.com/datasets/mihikaajayjadhav/books-dataset-15k-books-across-100-categories>

Ekstrak file ZIP dari Kaggle, lalu salin file CSV yang memuat data buku ke folder `dataset/` dengan nama `books.csv`. Dataset tidak disertakan dalam repository ini supaya pengguna mengunduh versi sumbernya secara langsung dan memeriksa lisensi dataset.

## Fitur

- Membaca file CSV dengan modul `csv` dari Python.
- Menyimpan setiap baris sebagai dictionary dan seluruh buku sebagai list.
- Mendeteksi kolom judul secara otomatis jika nama kolom mengandung variasi seperti `title`, `book_title`, `Book Title`, atau `judul`.
- Mencari berdasarkan kolom pilihan, misalnya judul, penulis, atau kategori.
- Mengimplementasikan Linear Search dan Binary Search secara manual.
- Menampilkan data jika ditemukan dan pesan jika tidak ditemukan.
- Menghitung perbandingan dan mengukur waktu eksekusi.
- Menguji ukuran input `n = 100`, `n = 1.000`, dan `n = 10.000` jika jumlah data yang tersedia mencukupi.
- Menyimpan tabel hasil ke `output/hasil_benchmark.csv` dan membuat grafik waktu serta jumlah perbandingan.
- Memiliki unit test dengan modul `unittest`.

## Persiapan

Pastikan Python 3.10 atau lebih baru sudah terpasang. Buka terminal pada folder proyek, lalu jalankan:

```bash
python -m pip install -r requirements.txt
```

Siapkan dataset menjadi `dataset/books.csv`, kemudian jalankan:

```bash
python main.py
```

Jika file CSV memiliki nama/lokasi berbeda, masukkan path-nya sebagai argumen:

```bash
python main.py --data "dataset/nama_file.csv"
```

## Cara menggunakan

1. Pilih menu `1` untuk mencari buku atau menu `2` untuk benchmark.
2. Pilih kolom yang akan dijadikan kunci pencarian. Kolom judul otomatis menjadi pilihan default jika dikenali.
3. Untuk menu pencarian, masukkan nilai yang dicari. Pencarian memakai kecocokan teks **persis**, tetapi tidak membedakan huruf besar dan kecil.
4. Kedua algoritma akan menampilkan hasil, jumlah perbandingan, dan waktu eksekusi.
5. Untuk benchmark, lihat tabel di terminal dan file hasil di folder `output/`.

## Penjelasan algoritma

### Linear Search

Memeriksa data dari urutan awal satu per satu hingga target ditemukan atau semua elemen selesai diperiksa. Kompleksitas waktu terburuknya adalah **O(n)**. Implementasi menghitung satu perbandingan kesamaan untuk setiap elemen yang diperiksa.

### Binary Search

Membandingkan target dengan nilai di tengah, lalu membuang setengah rentang pencarian setiap iterasi. Data **harus diurutkan terlebih dahulu** berdasarkan kolom yang dicari. Kompleksitas pencariannya adalah **O(log n)**. Di kode ini, operasi perbandingan `==` dan `<` dihitung masing-masing sebagai satu perbandingan. Waktu pengurutan tidak dimasukkan ke pengukuran waktu pencarian, karena yang diukur adalah pencarian setelah data siap dan terurut.

### Metode pengujian

Benchmark memilih `n` baris pertama untuk setiap ukuran input dan menggunakan kata kunci buatan yang dirancang agar tidak ditemukan. Ini menampilkan kasus pencarian gagal, sehingga Linear Search umumnya memeriksa semua `n` baris. Waktu adalah rata-rata dari beberapa pengulangan agar pengukuran lebih stabil. Hasil bergantung pada perangkat, versi Python, dan dataset yang digunakan; angka hasil bukan nilai tetap.

> Catatan: jika file CSV kurang dari 10.000 baris, ukuran uji yang lebih besar akan dilewati dan diberi keterangan. Dataset tugas seharusnya cukup besar untuk semua ukuran yang diminta.

## Menjalankan pengujian otomatis

```bash
python -m unittest -v
```

## Struktur folder

```text
sistem_pencarian_buku/
├── main.py
├── test_search.py
├── requirements.txt
├── README.md
├── dataset/
│   └── README.md
└── output/
    └── (hasil benchmark dibuat otomatis)
```

## Mengunggah ke GitHub sebagai repository publik

1. Buka GitHub dan buat repository baru, misalnya `sistem-pencarian-buku`. Pilih visibilitas **Public**.
2. Buka terminal di folder proyek ini, lalu jalankan perintah berikut (ganti URL dengan URL repository milikmu):

```bash
git init
git add .
git commit -m "Implementasi Linear Search dan Binary Search"
git branch -M main
git remote add origin https://github.com/USERNAME/sistem-pencarian-buku.git
git push -u origin main
```

3. Periksa halaman repository. Pastikan `main.py`, `test_search.py`, `requirements.txt`, dan `README.md` tampil.
4. Dataset CSV diabaikan oleh `.gitignore`. Cantumkan tautan Kaggle pada README dan unggah dataset hanya jika lisensinya mengizinkan. Untuk tugas, dosen dapat mengunduh dataset dari sumber yang sama dan mengikuti petunjuk di atas.

## Batasan yang perlu dituliskan dalam laporan

- Binary Search memerlukan tahap pengurutan terlebih dahulu; tahap itu tidak dihitung di waktu pencarian.
- Kedua algoritma mencari nilai teks yang cocok persis, bukan pencarian sebagian kata.
- Jumlah perbandingan Linear Search dan Binary Search memakai definisi yang dituliskan pada bagian penjelasan algoritma.
- Hasil waktu dipengaruhi perangkat dan lingkungan eksekusi, sehingga fokuskan pembahasan pada tren dan jumlah perbandingan, bukan hanya angka waktu.
