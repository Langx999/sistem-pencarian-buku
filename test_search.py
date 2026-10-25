"""Unit test untuk implementasi pencarian buku."""

import unittest

from main import binary_search, linear_search, normalisasi


class TestAlgoritmaPencarian(unittest.TestCase):
    def setUp(self):
        self.buku = [
            {"title": "Zebra", "author": "A. Penulis"},
            {"title": "Algoritma Python", "author": "B. Penulis"},
            {"title": "Dasar Komputer", "author": "C. Penulis"},
            {"title": "Struktur Data", "author": "D. Penulis"},
        ]
        self.buku_terurut = sorted(self.buku, key=lambda item: normalisasi(item["title"]))

    def test_linear_search_menemukan_data(self):
        hasil, perbandingan = linear_search(self.buku, "title", "Algoritma Python")
        self.assertIsNotNone(hasil)
        self.assertEqual(hasil["title"], "Algoritma Python")
        self.assertGreater(perbandingan, 0)

    def test_binary_search_menemukan_data_tanpa_beda_kapital(self):
        hasil, perbandingan = binary_search(self.buku_terurut, "title", "DASAR KOMPUTER")
        self.assertIsNotNone(hasil)
        self.assertEqual(hasil["title"], "Dasar Komputer")
        self.assertGreater(perbandingan, 0)

    def test_linear_search_data_tidak_ditemukan(self):
        hasil, perbandingan = linear_search(self.buku, "title", "Buku Tidak Ada")
        self.assertIsNone(hasil)
        self.assertEqual(perbandingan, len(self.buku))

    def test_binary_search_data_tidak_ditemukan(self):
        hasil, perbandingan = binary_search(self.buku_terurut, "title", "Buku Tidak Ada")
        self.assertIsNone(hasil)
        self.assertGreater(perbandingan, 0)

    def test_linear_search_menghitung_perbandingan(self):
        hasil, perbandingan = linear_search(self.buku, "title", "Struktur Data")
        self.assertIsNotNone(hasil)
        self.assertEqual(perbandingan, 4)


if __name__ == "__main__":
    unittest.main()
