# ==========================================
# dashboard.py
# FINAL WORKING VERSION (Load Images With PIL)
# ==========================================

import sys
import time
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image  # ✅ مهم


# استدعاء الأقسام حسب ملفاتك
from xray import XraysWindow
from dentel import DentalWindow
from implant import ImplantWindow
from press import PressWindow


def load_pixmap_pil(path: str) -> QPixmap:
    """تحميل الصور عبر PIL وتحويلها إلى QPixmap (حل مضمون حتى لو Qt ما يقرأ JPG/PNG)"""
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    data = img.tobytes("raw", "RGBA")
    qimg = QImage(data, w, h, QImage.Format_RGBA8888)
    return QPixmap.fromImage(qimg)


class Clinic(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Clinic")
        self.setFixedSize(1200, 650)
        self.setStyleSheet("background-color:white;")

        # ======== مسار المشروع الحقيقي ========
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # ==========================
        # Top Bar (Time & Date)
        # ==========================
        self.top_label = QLabel(self)
        self.top_label.setGeometry(0, 0, 1200, 70)
        self.top_label.setStyleSheet("""
            background-color:#0f5f73;
            color:white;
            font-size:18px;
            font-weight:bold;
        """)
        self.top_label.setAlignment(Qt.AlignCenter)

        self.update_time()
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        # ==========================
        # Background Image (LEFT)
        # ==========================
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 70, 995, 580)
        self.bg_label.setScaledContents(True)

        bg_path = os.path.join(self.base_path, "images", "one.jpg")
        print("BG PATH:", bg_path, "| exists:", os.path.exists(bg_path))

        try:
            bg_pixmap = load_pixmap_pil(bg_path)
            self.bg_label.setPixmap(bg_pixmap)
        except Exception as e:
            print("❌ PIL Failed:", e)
            self.bg_label.setText("Background Not Found")
            self.bg_label.setAlignment(Qt.AlignCenter)

        # ==========================
        # Right Menu
        # ==========================
        self.menu_frame = QFrame(self)
        self.menu_frame.setGeometry(995, 70, 205, 580)
        self.menu_frame.setStyleSheet("""
            background:white;
            border-left:1px solid #cccccc;
        """)

        # Logo
        self.logo = QLabel(self.menu_frame)
        self.logo.setGeometry(0, 0, 205, 200)
        self.logo.setScaledContents(True)

        logo_path = os.path.join(self.base_path, "images", "logo.jpg")
        print("LOGO PATH:", logo_path, "| exists:", os.path.exists(logo_path))

        try:
            logo_pixmap = load_pixmap_pil(logo_path)
            self.logo.setPixmap(logo_pixmap)
        except Exception as e:
            print("❌ PIL Logo Failed:", e)

        # Menu Title
        self.menu_title = QLabel("Menu", self.menu_frame)
        self.menu_title.setGeometry(0, 200, 205, 50)
        self.menu_title.setAlignment(Qt.AlignCenter)
        self.menu_title.setStyleSheet("""
            font-size:20px;
            color:#0f5f73;
            font-weight:bold;
        """)

        # Buttons
        self.create_button("X-Rays", 250, self.open_xray)
        self.create_button("dentel", 310, self.open_dental)
        self.create_button("Implant", 370, self.open_implant)
        self.create_button("Press", 430, self.open_press)
        self.create_button("Exit", 490, self.close)

    def create_button(self, text, y, func):
        btn = QPushButton(text, self.menu_frame)
        btn.setGeometry(0, y, 205, 50)
        btn.setStyleSheet("""
            QPushButton{
                background-color:#0f5f73;
                color:white;
                font-size:16px;
                border:none;
            }
            QPushButton:hover{
                background-color:#14839e;
            }
        """)
        btn.clicked.connect(func)

    def update_time(self):
        now = time.strftime("%d-%m-%Y   %H:%M:%S")
        self.top_label.setText(f"Dental Clinic Management System      {now}")

    def open_xray(self):
        self.win = XraysWindow()
        self.win.show()

    def open_dental(self):
        self.win = DentalWindow()
        self.win.show()

    def open_implant(self):
        self.win = ImplantWindow()
        self.win.show()

    def open_press(self):
        self.win = PressWindow()
        self.win.show()



