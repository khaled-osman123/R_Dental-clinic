# ==========================================
# xray.py  (PyQt5) - Radiology / X-Ray (FIXED UI)
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


class XraysWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radiology (X-Ray)")
        self.setFixedSize(995, 550)
        self.setStyleSheet("background:white;")
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.selected_id = None

        self.build_ui()
        self.load_data()

    # ================= DB =================
    def con(self):
        return sqlite3.connect("clinic.db")

    # ================= UI =================
    def build_ui(self):
        # -------- Left Image Panel --------
        left = QFrame(self)
        left.setGeometry(5, 5, 325, 280)

        img = QLabel(left)
        img.setGeometry(0, 0, 325, 200)
        img.setScaledContents(True)
        img_path = os.path.join(self.base_path, "images", "pat2.jpg")
        try:
            img.setPixmap(load_pixmap_pil(img_path))
        except:
            img.setText("Image Not Found")
            img.setAlignment(Qt.AlignCenter)

        def btn(text, x, y, fn):
            b = QPushButton(text, left)
            b.setGeometry(x, y, 155, 32)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton{background:#0f5f73;color:white;font-weight:600;border:none;}
                QPushButton:hover{background:#14839e;}
            """)
            b.clicked.connect(fn)
            return b

        btn("Update", 0, 210, self.update_data)
        btn("Add", 170, 210, self.add_data)
        btn("Clear", 0, 245, self.clear_fields)
        btn("Delete", 170, 245, self.delete_data)

        # -------- Search (Top Right) --------
        search_box = QGroupBox("Search", self)
        search_box.setGeometry(345, 10, 635, 70)

        self.search_combo = QComboBox(search_box)
        self.search_combo.setGeometry(10, 28, 170, 28)
        self.search_combo.addItems(["Select", "name", "contact"])

        self.search_txt = QLineEdit(search_box)
        self.search_txt.setGeometry(190, 28, 280, 28)
        self.search_txt.setPlaceholderText("Search value")

        sbtn = QPushButton("Search", search_box)
        sbtn.setGeometry(480, 28, 145, 28)
        sbtn.setStyleSheet("background:#0f5f73;color:white;font-weight:600;border:none;")
        sbtn.clicked.connect(self.search_data)

        # -------- Title --------
        title = QLabel("X-Ray Record", self)
        title.setGeometry(345, 90, 635, 30)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background:#0f5f73;color:white;font-weight:700;")

        # -------- Form (Grid Clean) --------
        form = QFrame(self)
        form.setGeometry(345, 125, 635, 150)

        grid = QGridLayout(form)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        def small_line():
            e = QLineEdit()
            e.setFixedHeight(26)
            return e

        def small_combo(items):
            c = QComboBox()
            c.setFixedHeight(26)
            c.addItems(items)
            return c

        self.in_name = small_line()
        self.in_gender = small_combo(["Select", "Male", "Female"])
        self.in_age = small_line()
        self.in_date = small_line()
        self.in_state = small_line()
        self.in_price = small_line()
        self.in_contact = small_line()
        self.in_adress = small_line()

        # Row 0
        grid.addWidget(QLabel("Name"), 0, 0)
        grid.addWidget(self.in_name, 0, 1)
        grid.addWidget(QLabel("Gender"), 0, 2)
        grid.addWidget(self.in_gender, 0, 3)
        grid.addWidget(QLabel("Age"), 0, 4)
        grid.addWidget(self.in_age, 0, 5)

        # Row 1
        grid.addWidget(QLabel("Date"), 1, 0)
        grid.addWidget(self.in_date, 1, 1)
        grid.addWidget(QLabel("State"), 1, 2)
        grid.addWidget(self.in_state, 1, 3)
        grid.addWidget(QLabel("Price"), 1, 4)
        grid.addWidget(self.in_price, 1, 5)

        # Row 2
        grid.addWidget(QLabel("Contact"), 2, 0)
        grid.addWidget(self.in_contact, 2, 1)
        grid.addWidget(QLabel("Address"), 2, 2)
        grid.addWidget(self.in_adress, 2, 3, 1, 3)

        # -------- Table --------
        self.table = QTableWidget(self)
        self.table.setGeometry(0, 290, 995, 260)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["Address", "Contact", "Price", "State", "Date", "Age", "Gender", "Name", "ID"]
        )
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.pick_row)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # ================= Table pick =================
    def pick_row(self, row, col):
        rid = self.table.item(row, 8)
        if not rid:
            return
        self.selected_id = rid.text()

        self.in_adress.setText(self.table.item(row, 0).text())
        self.in_contact.setText(self.table.item(row, 1).text())
        self.in_price.setText(self.table.item(row, 2).text())
        self.in_state.setText(self.table.item(row, 3).text())
        self.in_date.setText(self.table.item(row, 4).text())
        self.in_age.setText(self.table.item(row, 5).text())
        self.in_gender.setCurrentText(self.table.item(row, 6).text())
        self.in_name.setText(self.table.item(row, 7).text())

    # ================= Helpers =================
    def clear_fields(self):
        self.in_name.clear()
        self.in_gender.setCurrentIndex(0)
        self.in_age.clear()
        self.in_date.clear()
        self.in_state.clear()
        self.in_price.clear()
        self.in_contact.clear()
        self.in_adress.clear()
        self.selected_id = None
        self.search_combo.setCurrentIndex(0)
        self.search_txt.clear()
        self.load_data()

    def load_data(self):
        with self.con() as con:
            cur = con.cursor()
            cur.execute("SELECT adress,contact,price,state,date,age,gender,name,xid FROM xrays")
            rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    # ================= CRUD =================
    def add_data(self):
        # ✅ required only:
        if not self.in_name.text().strip() or not self.in_date.text().strip() or not self.in_contact.text().strip():
            QMessageBox.warning(self, "Error", "Required: Name + Date + Contact")
            return

        with self.con() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO xrays(adress,contact,price,state,date,age,gender,name)
                VALUES(?,?,?,?,?,?,?,?)
            """, (
                self.in_adress.text().strip(),
                self.in_contact.text().strip(),
                self.in_price.text().strip(),
                self.in_state.text().strip(),
                self.in_date.text().strip(),
                self.in_age.text().strip(),
                self.in_gender.currentText(),
                self.in_name.text().strip()
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
                UPDATE xrays SET adress=?,contact=?,price=?,state=?,date=?,age=?,gender=?,name=?
                WHERE xid=?
            """, (
                self.in_adress.text().strip(),
                self.in_contact.text().strip(),
                self.in_price.text().strip(),
                self.in_state.text().strip(),
                self.in_date.text().strip(),
                self.in_age.text().strip(),
                self.in_gender.currentText(),
                self.in_name.text().strip(),
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
            cur.execute("DELETE FROM xrays WHERE xid=?", (self.selected_id,))
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
                SELECT adress,contact,price,state,date,age,gender,name,xid
                FROM xrays
                WHERE {col} LIKE ?
            """, ("%" + val + "%",))
            rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))
