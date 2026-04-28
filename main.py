import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import JendelaUtama

def muat_gaya_tampilan(aplikasi):
    direktori_sekarang = os.path.dirname(os.path.abspath(__file__))
    jalur_qss = os.path.join(direktori_sekarang, 'styles', 'style.qss')
    
    try:
        with open(jalur_qss, "r") as file:
            aplikasi.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Peringatan: File style.qss tidak ditemukan. UI akan menggunakan gaya default.")

def utama():
    aplikasi = QApplication(sys.argv)
    muat_gaya_tampilan(aplikasi)
    
    jendela = JendelaUtama()
    jendela.show()
    
    sys.exit(aplikasi.exec())

if __name__ == "__main__":
    utama()