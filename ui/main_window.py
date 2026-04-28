import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHeaderView, QDialog, QToolBar, QLineEdit) 
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt, QSize
from logic.toolbar import PengendaliJurnal
from ui.input_catatan import DialogJurnal

class JendelaUtama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pengelola Catatan Harian")
        self.resize(900, 550)
        
        self.pengendali = PengendaliJurnal()
        self.atur_tampilan()
        self.atur_menu()
        self.atur_toolbar() 
        self.muat_data_tabel()

    def atur_menu(self):
        bar_menu = self.menuBar()
        aksi_tentang = QAction("Tentang Aplikasi", self)
        aksi_tentang.triggered.connect(self.tampilkan_dialog_tentang)
        bar_menu.addAction(aksi_tentang)

    def atur_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)
        
        direktori_sekarang = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(direktori_sekarang, '..', 'icon')
        
        def load_icon(name):
            return QIcon(os.path.join(icon_path, name))

        self.aksi_tambah = QAction(load_icon("tambah.png"), "Tambah", self, shortcut=QKeySequence.New, triggered=self.tambah_jurnal)
        self.aksi_lihat = QAction(load_icon("lihat.png"), "Lihat", self, triggered=self.lihat_jurnal)
        self.aksi_edit = QAction(load_icon("edit.png"), "Edit", self, triggered=self.edit_jurnal)
        self.aksi_hapus = QAction(load_icon("hapus.png"), "Hapus", self, shortcut=QKeySequence.Delete, triggered=self.hapus_jurnal)
        self.aksi_segarkan = QAction(load_icon("segarkan.png"), "Segarkan", self, shortcut=QKeySequence.Refresh, triggered=self.muat_data_tabel)

        toolbar.addAction(self.aksi_tambah)
        toolbar.addAction(self.aksi_lihat)
        toolbar.addSeparator()
        toolbar.addAction(self.aksi_edit)
        toolbar.addAction(self.aksi_hapus)
        toolbar.addSeparator()
        toolbar.addAction(self.aksi_segarkan)
        toolbar.addSeparator()

        self.input_cari = QLineEdit()
        self.input_cari.setPlaceholderText("🔍 Cari judul catatan...")
        self.input_cari.setFixedWidth(250)
        self.input_cari.textChanged.connect(self.cari_jurnal) # Deteksi ketikan secara real-time
        toolbar.addWidget(self.input_cari)

    def atur_tampilan(self):
        widget_tengah = QWidget()
        self.setCentralWidget(widget_tengah)
        layout_utama = QVBoxLayout(widget_tengah)
        layout_utama.setContentsMargins(20, 10, 20, 20) 
        layout_utama.setSpacing(15)

        self.label_judul = QLabel("Buku Catatan Harian")
        self.label_judul.setObjectName("judulUtama")
        self.label_judul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_judul.setStyleSheet("color: black; font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout_utama.addWidget(self.label_judul)

        self.tabel = QTableWidget()
        self.tabel.setColumnCount(5) 
        self.tabel.setHorizontalHeaderLabels(["Tanggal", "Judul", "Suasana Hati", "Catatan", "Target Besok"])
        
        self.tabel.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabel.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabel.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabel.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        self.tabel.verticalHeader().setVisible(False) 
        self.tabel.setShowGrid(False) 
        
        layout_utama.addWidget(self.tabel)

    def muat_data_tabel(self):
        self.tabel.setRowCount(0)
        rekam_data = self.pengendali.ambil_semua_entri()
        self.tampilkan_data_ke_tabel(rekam_data)

    def cari_jurnal(self, kata_kunci):
        self.tabel.setRowCount(0)
        if not kata_kunci.strip():
            rekam_data = self.pengendali.ambil_semua_entri()
        else:
            rekam_data = self.pengendali.cari_entri(kata_kunci)
        
        self.tampilkan_data_ke_tabel(rekam_data)

    def tampilkan_data_ke_tabel(self, rekam_data):
        """Fungsi pembantu agar tidak menulis ulang perulangan tabel"""
        for indeks_baris, data_baris in enumerate(rekam_data):
            self.tabel.insertRow(indeks_baris)
            id_jurnal = data_baris[0]
            data_tampilan = data_baris[1:] 
            
            for indeks_kolom, item in enumerate(data_tampilan):
                tabel_item = QTableWidgetItem(str(item))
                if indeks_kolom == 0:
                    tabel_item.setData(Qt.UserRole, id_jurnal)
                self.tabel.setItem(indeks_baris, indeks_kolom, tabel_item)

    def dapatkan_id_terpilih(self):
        baris_terpilih = self.tabel.selectionModel().selectedRows()
        if not baris_terpilih:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih baris data terlebih dahulu!")
            return None
        baris = baris_terpilih[0].row()
        return int(self.tabel.item(baris, 0).data(Qt.UserRole))

    def tambah_jurnal(self):
        dialog = DialogJurnal(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.pengendali.tambah_entri(dialog.dapatkan_data())
            # Refresh tabel dengan memicu fungsi pencarian yang ada saat ini (agar sesuai filter)
            self.cari_jurnal(self.input_cari.text())

    def lihat_jurnal(self):
        id_jurnal = self.dapatkan_id_terpilih()
        if id_jurnal is None: return
            
        data = self.pengendali.ambil_detail_entri(id_jurnal)
        dialog = DialogJurnal(self, data_jurnal=data, baca_saja=True)
        dialog.exec()

    def edit_jurnal(self):
        id_jurnal = self.dapatkan_id_terpilih()
        if id_jurnal is None: return
            
        data = self.pengendali.ambil_detail_entri(id_jurnal)
        dialog = DialogJurnal(self, data_jurnal=data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.pengendali.perbarui_entri(id_jurnal, dialog.dapatkan_data())
            self.cari_jurnal(self.input_cari.text())

    def hapus_jurnal(self):
        id_jurnal = self.dapatkan_id_terpilih()
        if id_jurnal is None: return

        jawaban = QMessageBox.question(
            self, 'Konfirmasi Hapus', 
            'Apakah Anda yakin ingin menghapus catatan ini?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )

        if jawaban == QMessageBox.StandardButton.Yes:
            self.pengendali.hapus_entri(id_jurnal)
            self.cari_jurnal(self.input_cari.text())

    def tampilkan_dialog_tentang(self):
        QMessageBox.about(
            self, 
            "Tentang Aplikasi", 
            "<h3>Pengelola Catatan Harian</h3>"
            "<p>Aplikasi sederhana untuk manajemen catatan harian pribadi.</p>"
            "<hr>"
            "<b>Dibuat oleh:</b><br>"
            "Nama: Muhammad Ravi Rayvansyah<br>"
            "NIM: F1D02410078<br>"
            "Program Studi: Sistem Informatika<br>"
            "Universitas Mataram"
        )

    def closeEvent(self, event):
        kotak_pesan = QMessageBox(self)
        kotak_pesan.setWindowTitle('Konfirmasi Keluar')
        kotak_pesan.setText('Apakah Anda yakin ingin keluar dari aplikasi?')
        
        tombol_iya = kotak_pesan.addButton("Iya", QMessageBox.ButtonRole.YesRole)
        tombol_tidak = kotak_pesan.addButton("Tidak", QMessageBox.ButtonRole.NoRole)
        kotak_pesan.setDefaultButton(tombol_tidak)
        
        kotak_pesan.exec()
        
        if kotak_pesan.clickedButton() == tombol_iya:
            event.accept() 
        else:
            event.ignore()