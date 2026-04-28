from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QDateEdit, QComboBox, QTextEdit, QPushButton, QMessageBox, QLabel)
from PySide6.QtCore import QDate, Qt

class DialogJurnal(QDialog):
    def __init__(self, induk=None, data_jurnal=None, baca_saja=False):
        super().__init__(induk)
        self.data_jurnal = data_jurnal
        self.baca_saja = baca_saja
        
        judul_jendela = "Lihat Catatan" if baca_saja else ("Edit Jurnal" if data_jurnal else "Tambah Jurnal")
        self.setWindowTitle(judul_jendela)
        self.setFixedSize(450, 620)
        
        self.atur_tampilan()

        if self.data_jurnal and not self.baca_saja:
            self.muat_data()

    def atur_tampilan(self):
        layout_utama = QVBoxLayout(self)
        layout_utama.setContentsMargins(25, 20, 25, 20) 
        layout_utama.setSpacing(10)

        if self.baca_saja:
            self.setStyleSheet("background-color: #FFFFFF;") 
            
            judul_label = QLabel(self.data_jurnal[1])
            judul_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1B2559;")
            judul_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            judul_label.setWordWrap(True)
            
            info_label = QLabel(f"📅 {self.data_jurnal[2]}   |   😊 {self.data_jurnal[3]}")
            info_label.setStyleSheet("font-size: 14px; color: #718096; margin-bottom: 10px;")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Menggunakan 1 widget teks dengan format HTML agar kodenya pendek dan bisa discroll
            isi_nota = QTextEdit()
            isi_nota.setReadOnly(True)
            isi_nota.setStyleSheet("border: none; background-color: transparent; font-size: 15px; color: #2D3748;")
            
            # Format teks menyerupai catatan menggunakan HTML
            teks_html = f"""
            <h3 style='color: #4318FF;'>📝 Catatan:</h3>
            <p style='line-height: 1.5;'>{self.data_jurnal[5]}</p>
            <br>
            <h3 style='color: #4318FF;'>🎯 Target Besok:</h3>
            <p style='line-height: 1.5;'>{self.data_jurnal[4]}</p>
            """
            isi_nota.setHtml(teks_html)
            
            layout_utama.addWidget(judul_label)
            layout_utama.addWidget(info_label)
            layout_utama.addWidget(isi_nota)
            
            layout_tombol = QHBoxLayout()
            self.tombol_tutup = QPushButton("Tutup")
            self.tombol_tutup.setCursor(Qt.CursorShape.PointingHandCursor)
            self.tombol_tutup.clicked.connect(self.accept)
            
            layout_tombol.addStretch()
            layout_tombol.addWidget(self.tombol_tutup)
            layout_tombol.addStretch()
            layout_utama.addLayout(layout_tombol)

        else:
            # ==========================================
            # TAMPILAN FORM (UNTUK TAMBAH / EDIT)
            # ==========================================
            self.input_judul = QLineEdit()
            self.input_judul.setPlaceholderText("Masukkan judul...")
            
            self.input_tanggal = QDateEdit()
            self.input_tanggal.setCalendarPopup(True)
            self.input_tanggal.setDate(QDate.currentDate())
            
            self.input_suasana_hati = QComboBox()
            self.input_suasana_hati.addItems(["Sangat Baik", "Baik", "Biasa Saja", "Buruk", "Sangat Buruk"])
            
            self.input_catatan = QTextEdit()
            
            self.input_target = QTextEdit()
            self.input_target.setPlaceholderText("Apa rencana untuk besok?")
            self.input_target.setMaximumHeight(100)

            layout_form = QVBoxLayout()
            layout_form.setSpacing(5)
            
            layout_form.addWidget(QLabel("Judul:"))
            layout_form.addWidget(self.input_judul)
            
            layout_form.addWidget(QLabel("Tanggal:"))
            layout_form.addWidget(self.input_tanggal)
            
            layout_form.addWidget(QLabel("Suasana Hati:"))
            layout_form.addWidget(self.input_suasana_hati)
            
            layout_form.addWidget(QLabel("Catatan:"))
            layout_form.addWidget(self.input_catatan)
            
            layout_form.addWidget(QLabel("Target Besok:"))
            layout_form.addWidget(self.input_target)

            layout_utama.addLayout(layout_form)

            # Atur Tombol Bawah
            layout_tombol = QHBoxLayout()
            layout_tombol.setContentsMargins(0, 15, 0, 0) 
            
            self.tombol_simpan = QPushButton("Simpan")
            self.tombol_batal = QPushButton("Batal")
            self.tombol_simpan.setObjectName("tombolSimpan")
            self.tombol_batal.setObjectName("tombolBatal")
            
            self.tombol_simpan.setCursor(Qt.CursorShape.PointingHandCursor)
            self.tombol_batal.setCursor(Qt.CursorShape.PointingHandCursor)
            
            self.tombol_simpan.clicked.connect(self.validasi_dan_simpan)
            self.tombol_batal.clicked.connect(self.reject)
            
            layout_tombol.addStretch()
            layout_tombol.addWidget(self.tombol_batal)
            layout_tombol.addWidget(self.tombol_simpan)
            layout_utama.addLayout(layout_tombol)

    def muat_data(self):
        # Index: 0:id, 1:judul, 2:tanggal, 3:suasana_hati, 4:target, 5:catatan
        self.input_judul.setText(self.data_jurnal[1])
        self.input_tanggal.setDate(QDate.fromString(self.data_jurnal[2], "yyyy-MM-dd"))
        self.input_suasana_hati.setCurrentText(self.data_jurnal[3])
        self.input_target.setPlainText(self.data_jurnal[4])
        self.input_catatan.setPlainText(self.data_jurnal[5])

    def validasi_dan_simpan(self):
        if not self.input_judul.text().strip():
            QMessageBox.warning(self, "Peringatan", "Judul tidak boleh kosong!")
            return
        self.accept()

    def dapatkan_data(self):
        return {
            'judul': self.input_judul.text(),
            'tanggal': self.input_tanggal.date().toString("yyyy-MM-dd"),
            'suasana_hati': self.input_suasana_hati.currentText(),
            'target': self.input_target.toPlainText(),
            'catatan': self.input_catatan.toPlainText()
        }