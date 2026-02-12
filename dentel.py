# ==========================================
# dentel.py (PyQt5) - Appointments
# ==========================================

import os
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image


def load_pixmap_pil(path: str) -> QPixmap:
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    data = img.tobytes("raw", "RGBA")
    qimg = QImage(data, w, h, QImage.Format_RGBA8888)
    return QPixmap.fromImage(qimg)


class DentalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Appointments")
        self.setFixedSize(995, 550)
        self.setStyleSheet("background:white;")
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.selected_id = None

        self.build_ui()
        self.load_data()

    def con(self):
        return sqlite3.connect("clinic.db")

    def build_ui(self):
        img = QLabel(self)
        img.setGeometry(5, 5, 325, 200)
        img.setScaledContents(True)
        img_path = os.path.join(self.base_path, "images", "m.jpg")
        try:
            img.setPixmap(load_pixmap_pil(img_path))
        except:
            img.setText("Image")

        g = QGroupBox("Search", self)
        g.setGeometry(350, 15, 630, 65)

        self.search_combo = QComboBox(g)
        self.search_combo.setGeometry(10, 25, 170, 28)
        self.search_combo.addItems(["Select", "name", "contact"])

        self.search_txt = QLineEdit(g)
        self.search_txt.setGeometry(190, 25, 260, 28)
        self.search_txt.setPlaceholderText("Search value")

        btn = QPushButton("Search", g)
        btn.setGeometry(460, 25, 160, 28)
        btn.setStyleSheet("background:#0f5f73;color:white;")
        btn.clicked.connect(self.search_data)

        title = QLabel("Appointment Record", self)
        title.setGeometry(340, 90, 645, 30)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background:#0f5f73;color:white;font-weight:700;")

        y1 = 130
        QLabel("Name", self).setGeometry(930, y1, 60, 22)
        QLabel("Gender", self).setGeometry(705, y1, 60, 22)
        QLabel("Age", self).setGeometry(505, y1, 60, 22)

        self.in_name = QLineEdit(self); self.in_name.setGeometry(770, y1, 150, 26)
        self.in_gender = QComboBox(self); self.in_gender.setGeometry(550, y1, 140, 26)
        self.in_gender.addItems(["Select", "Male", "Female"])
        self.in_age = QLineEdit(self); self.in_age.setGeometry(345, y1, 150, 26)

        y2 = 165
        QLabel("Date", self).setGeometry(930, y2, 60, 22)
        QLabel("State", self).setGeometry(705, y2, 60, 22)
        QLabel("Contact", self).setGeometry(505, y2, 60, 22)

        self.in_date = QLineEdit(self); self.in_date.setGeometry(770, y2, 150, 26)
        self.in_state = QLineEdit(self); self.in_state.setGeometry(550, y2, 140, 26)
        self.in_contact = QLineEdit(self); self.in_contact.setGeometry(345, y2, 150, 26)

        y3 = 200
        QLabel("Address", self).setGeometry(930, y3, 60, 22)
        self.in_adress = QLineEdit(self); self.in_adress.setGeometry(345, y3, 575, 26)

        def mkbtn(text, x, y, fn):
            b = QPushButton(text, self)
            b.setGeometry(x, y, 155, 28)
            b.setStyleSheet("background:#0f5f73;color:white;")
            b.clicked.connect(fn)
            return b

        mkbtn("Add", 175, 215, self.add_data)
        mkbtn("Update", 5, 215, self.update_data)
        mkbtn("Delete", 175, 250, self.delete_data)
        mkbtn("Clear", 5, 250, self.clear_fields)

        self.table = QTableWidget(self)
        self.table.setGeometry(0, 290, 995, 260)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Address", "Contact", "State", "Date", "Age", "Gender", "Name", "ID"]
        )
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.pick_row)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def pick_row(self, row, col):
        rid = self.table.item(row, 7)
        if not rid:
            return
        self.selected_id = rid.text()
        self.in_adress.setText(self.table.item(row, 0).text())
        self.in_contact.setText(self.table.item(row, 1).text())
        self.in_state.setText(self.table.item(row, 2).text())
        self.in_date.setText(self.table.item(row, 3).text())
        self.in_age.setText(self.table.item(row, 4).text())
        self.in_gender.setCurrentText(self.table.item(row, 5).text())
        self.in_name.setText(self.table.item(row, 6).text())

    def clear_fields(self):
        self.in_name.clear()
        self.in_gender.setCurrentIndex(0)
        self.in_age.clear()
        self.in_date.clear()
        self.in_state.clear()
        self.in_contact.clear()
        self.in_adress.clear()
        self.selected_id = None
        self.search_combo.setCurrentIndex(0)
        self.search_txt.clear()
        self.load_data()

    def load_data(self):
        with self.con() as con:
            cur = con.cursor()
            cur.execute("SELECT adress,contact,state,date,age,gender,name,aid FROM dental")
            rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    def add_data(self):
        if (not self.in_name.text().strip() or self.in_gender.currentText() == "Select" or
            not self.in_age.text().strip() or not self.in_date.text().strip() or
            not self.in_state.text().strip() or not self.in_contact.text().strip() or
            not self.in_adress.text().strip()):
            QMessageBox.warning(self, "Error", "Please enter all fields")
            return

        with self.con() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO dental(adress,contact,state,date,age,gender,name)
                VALUES(?,?,?,?,?,?,?)
            """, (
                self.in_adress.text(),
                self.in_contact.text(),
                self.in_state.text(),
                self.in_date.text(),
                self.in_age.text(),
                self.in_gender.currentText(),
                self.in_name.text()
            ))
            con.commit()

        QMessageBox.information(self, "OK", "Added successfully")
        self.load_data()
        self.clear_fields()

    def update_data(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Error", "Select a record first")
            return
        if QMessageBox.question(self, "Confirm", "Update this record?") != QMessageBox.Yes:
            return

        with self.con() as con:
            cur = con.cursor()
            cur.execute("""
                UPDATE dental SET adress=?,contact=?,state=?,date=?,age=?,gender=?,name=?
                WHERE aid=?
            """, (
                self.in_adress.text(),
                self.in_contact.text(),
                self.in_state.text(),
                self.in_date.text(),
                self.in_age.text(),
                self.in_gender.currentText(),
                self.in_name.text(),
                self.selected_id
            ))
            con.commit()

        QMessageBox.information(self, "OK", "Updated successfully")
        self.load_data()
        self.clear_fields()

    def delete_data(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Error", "Select a record first")
            return
        if QMessageBox.question(self, "Confirm", "Delete this record?") != QMessageBox.Yes:
            return

        with self.con() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM dental WHERE aid=?", (self.selected_id,))
            con.commit()

        QMessageBox.information(self, "OK", "Deleted successfully")
        self.load_data()
        self.clear_fields()

    def search_data(self):
        col = self.search_combo.currentText()
        val = self.search_txt.text().strip()
        if col == "Select" or val == "":
            QMessageBox.warning(self, "Error", "Select field and enter value")
            return

        with self.con() as con:
            cur = con.cursor()
            cur.execute(f"""
                SELECT adress,contact,state,date,age,gender,name,aid
                FROM dental
                WHERE {col} LIKE ?
            """, ("%" + val + "%",))
            rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))
