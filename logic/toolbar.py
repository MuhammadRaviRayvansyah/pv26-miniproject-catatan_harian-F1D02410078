from database.db_manager import PengelolaDatabase

class PengendaliJurnal:
    def __init__(self):
        self.db = PengelolaDatabase()

    def tambah_entri(self, data):
        self.db.tambah_jurnal(
            data['judul'], data['tanggal'], data['suasana_hati'], 
            data['target'], data['catatan']
        )

    def ambil_semua_entri(self):
        return self.db.ambil_semua_jurnal()
        
    def ambil_detail_entri(self, id_jurnal):
        return self.db.ambil_jurnal_berdasarkan_id(id_jurnal)

    def perbarui_entri(self, id_jurnal, data):
        self.db.perbarui_jurnal(
            id_jurnal, data['judul'], data['tanggal'], data['suasana_hati'], 
            data['target'], data['catatan']
        )

    def hapus_entri(self, id_jurnal):
        self.db.hapus_jurnal(id_jurnal)

    def cari_entri(self, kata_kunci):
        return self.db.cari_jurnal_berdasarkan_judul(kata_kunci)