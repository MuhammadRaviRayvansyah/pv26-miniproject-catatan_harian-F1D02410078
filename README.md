Aplikasi Buku Catatan Harian

Aplikasi Buku Catatan Harian adalah platform manajemen catatan harian digital berbasis desktop yang dirancang dengan antarmuka modern dan intuitif. Aplikasi ini memungkinkan pengguna untuk mencatat pengalaman, memantau suasana hati, dan merencanakan target harian.

Deskripsi Singkat
Aplikasi ini menggunakan arsitektur Separation of Concerns (SoC) yang memisahkan tanggung jawab antara antarmuka pengguna (UI), logika bisnis (Controller), dan manajemen data (Database). Dengan desain yang minimalis, aplikasi ini memberikan pengalaman pengguna yang nyaman dan estetik.

Fitur Utama
1. Tambah, Lihat, Edit, dan Hapus catatan harian.
2. Mencari catatan berdasarkan judul secara instan saat mengetik.
3. Menampilkan catatan dalam format lembaran nota elegan berbasis HTML.
4. Konfirmasi hapus dan pop-up konfirmasi keluar untuk mencegah kehilangan data.
5. Menggunakan QSS (Qt Style Sheets) untuk desain.

Teknologi yang Digunakan
1. Bahasa Pemrograman Python
2. Framework GUI PySide6
3. Database SQLite3
4. Styling QSS

Struktur Proyek
catatan_aktivitas/
├── main.py                Titik masuk utama aplikasi
├── database/
│   └── db_manager.py      Pengelolaan database SQLite
├── logic/
│   └── toolbar.py         Logika bisnis dan pengontrol
├── ui/
│   ├── main_window.py     Tampilan jendela utama
│   └── input_catatan.py   Dialog input dan mode lihat catatan
├── styles/
│   └── style.qss          File desain antarmuka
└── icon/                  Aset ikon aplikasi
