import sqlite3

class PengelolaDatabase:
    def __init__(self, nama_db="catatan_harian_v2.db"):
        self.nama_db = nama_db
        self._buat_tabel()

    def _dapatkan_koneksi(self):
        return sqlite3.connect(self.nama_db)

    def _buat_tabel(self):
        with self._dapatkan_koneksi() as koneksi:
            kursor = koneksi.cursor()
            kursor.execute('''
                CREATE TABLE IF NOT EXISTS jurnal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    judul TEXT NOT NULL,
                    tanggal TEXT NOT NULL,
                    suasana_hati TEXT,
                    target TEXT,
                    catatan TEXT
                )
            ''')
            koneksi.commit()

    def tambah_jurnal(self, judul, tanggal, suasana_hati, target, catatan):
        with self._dapatkan_koneksi() as koneksi:
            kursor = koneksi.cursor()
            kursor.execute('''
                INSERT INTO jurnal (judul, tanggal, suasana_hati, target, catatan)
                VALUES (?, ?, ?, ?, ?)
            ''', (judul, tanggal, suasana_hati, target, catatan))
            koneksi.commit()

    def ambil_semua_jurnal(self):
        with self._dapatkan_koneksi() as koneksi:
            kursor = koneksi.cursor()
            kursor.execute('SELECT id, tanggal, judul, suasana_hati, catatan, target FROM jurnal ORDER BY tanggal DESC')
            return kursor.fetchall()    
            
    def ambil_jurnal_berdasarkan_id(self, id_jurnal):
        with self._dapatkan_koneksi() as koneksi:
            kursor = koneksi.cursor()
            kursor.execute('SELECT * FROM jurnal WHERE id = ?', (id_jurnal,))
            return kursor.fetchone()

    def perbarui_jurnal(self, id_jurnal, judul, tanggal, suasana_hati, target, catatan):
        with self._dapatkan_koneksi() as koneksi:
            kursor = koneksi.cursor()
            kursor.execute('''
                UPDATE jurnal 
                SET judul=?, tanggal=?, suasana_hati=?, target=?, catatan=?
                WHERE id=?
            ''', (judul, tanggal, suasana_hati, target, catatan, id_jurnal))
            koneksi.commit()

    def hapus_jurnal(self, id_jurnal):
        with self._dapatkan_koneksi() as koneksi:
            kursor = koneksi.cursor()
            kursor.execute('DELETE FROM jurnal WHERE id = ?', (id_jurnal,))
            koneksi.commit()

    def cari_jurnal_berdasarkan_judul(self, kata_kunci):
        with self._dapatkan_koneksi() as koneksi:
            kursor = koneksi.cursor()
            kursor.execute('''
                SELECT id, tanggal, judul, suasana_hati, catatan, target 
                FROM jurnal 
                WHERE judul LIKE ? 
                ORDER BY tanggal DESC
            ''', ('%' + kata_kunci + '%',))
            return kursor.fetchall()