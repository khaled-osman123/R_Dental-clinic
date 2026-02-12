# ==========================================
# implant.py  (PyQt5) - Implant Department
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


class ImplantWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Implant Department")
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

        # ✅ حسب ملفاتك: d2.jpg
        img_path = os.path.join(self.base_path, "images", "d2.jpg")
        try:
            img.setPixmap(load_pixmap_pil(img_path))
        except:
            img.setText("Image Not Found")
            img.setAlignment(Qt.AlignCenter)

        def make_btn(text, x, y, fn):
            b = QPushButton(text, left)
            b.setGeometry(x, y, 155, 32)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton{background:#0f5f73;color:white;font-weight:600;border:none;}
                QPushButton:hover{background:#14839e;}
            """)
            b.clicked.connect(fn)
            return b

        make_btn("Update", 0, 210, self.update_data)
        make_btn("Add", 170, 210, self.add_data)
        make_btn("Clear", 0, 245, self.clear_fields)
        make_btn("Delete", 170, 245, self.delete_data)

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
        title = QLabel("Implant Record", self)
        title.setGeometry(345, 90, 635, 30)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background:#0f5f73;color:white;font-weight:700;")

        # -------- Form (Grid Clean) --------
        form = QFrame(self)
        form.setGeometry(345, 125, 635, 155)

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

        # Fields (مطابقة لقاعدة البيانات implant)
        # cont=Total, con2=Inst2, con1=Inst1, con=Count, price=UnitPrice, type=Type
        self.in_name = small_line()
        self.in_gender = small_combo(["Select", "Male", "Female"])
        self.in_age = small_line()
        self.in_date = small_line()
        self.in_contact = small_line()
        self.in_address = small_line()

        self.in_type = small_line()
        self.in_unit_price = small_line()
        self.in_count = small_line()
        self.in_inst1 = small_line()
        self.in_inst2 = small_line()
        self.in_total = small_line()

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
        grid.addWidget(QLabel("Contact"), 1, 2)
        grid.addWidget(self.in_contact, 1, 3)
        grid.addWidget(QLabel("Address"), 1, 4)
        grid.addWidget(self.in_address, 1, 5)

        # Row 2
        grid.addWidget(QLabel("Type"), 2, 0)
        grid.addWidget(self.in_type, 2, 1)
        grid.addWidget(QLabel("Unit Price"), 2, 2)
        grid.addWidget(self.in_unit_price, 2, 3)
        grid.addWidget(QLabel("Count"), 2, 4)
        grid.addWidget(self.in_count, 2, 5)

        # Row 3
        grid.addWidget(QLabel("Inst 1"), 3, 0)
        grid.addWidget(self.in_inst1, 3, 1)
        grid.addWidget(QLabel("Inst 2"), 3, 2)
        grid.addWidget(self.in_inst2, 3, 3)
        grid.addWidget(QLabel("Total"), 3, 4)
        grid.addWidget(self.in_total, 3, 5)

        # -------- Table --------
        self.table = QTableWidget(self)
        self.table.setGeometry(0, 290, 995, 260)
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "Total", "Inst2", "Inst1", "Count", "UnitPrice", "Type",
            "Address", "Contact", "Date", "Age", "Gender", "Name", "ID"
        ])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.pick_row)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # ================= Table pick =================
    def pick_row(self, row, col):
        rid_item = self.table.item(row, 12)
        if not rid_item:
            return
        self.selected_id = rid_item.text()

        self.in_total.setText(self.table.item(row, 0).text())
        self.in_inst2.setText(self.table.item(row, 1).text())
        self.in_inst1.setText(self.table.item(row, 2).text())
        self.in_count.setText(self.table.item(row, 3).text())
        self.in_unit_price.setText(self.table.item(row, 4).text())
        self.in_type.setText(self.table.item(row, 5).text())
        self.in_address.setText(self.table.item(row, 6).text())
        self.in_contact.setText(self.table.item(row, 7).text())
        self.in_date.setText(self.table.item(row, 8).text())
        self.in_age.setText(self.table.item(row, 9).text())
        self.in_gender.setCurrentText(self.table.item(row, 10).text())
        self.in_name.setText(self.table.item(row, 11).text())

    # ================= Helpers =================
    def clear_fields(self):
        self.in_name.clear()
        self.in_gender.setCurrentIndex(0)
        self.in_age.clear()
        self.in_date.clear()
        self.in_contact.clear()
        self.in_address.clear()

        self.in_type.clear()
        self.in_unit_price.clear()
        self.in_count.clear()
        self.in_inst1.clear()
        self.in_inst2.clear()
        self.in_total.clear()

        self.selected_id = None
        self.search_combo.setCurrentIndex(0)
        self.search_txt.clear()
        self.load_data()

    def load_data(self):
        with self.con() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT cont, con2, con1, con, price, type, adress, contact, date, age, gender, name, pid
                FROM implant
            """)
            rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    # ================= CRUD =================
    def add_data(self):
        # ✅ Required منطقي
        if not self.in_name.text().strip() or not self.in_contact.text().strip() or not self.in_date.text().strip():
            QMessageBox.warning(self, "Error", "Required: Name + Contact + Date")
            return

        with self.con() as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO implant(cont, con2, con1, con, price, type, adress, contact, date, age, gender, name)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                self.in_total.text().strip(),
                self.in_inst2.text().strip(),
                self.in_inst1.text().strip(),
                self.in_count.text().strip(),
                self.in_unit_price.text().strip(),
                self.in_type.text().strip(),
                self.in_address.text().strip(),
                self.in_contact.text().strip(),
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
                UPDATE implant
                SET cont=?, con2=?, con1=?, con=?, price=?, type=?, adress=?, contact=?, date=?, age=?, gender=?, name=?
                WHERE pid=?
            """, (
                self.in_total.text().strip(),
                self.in_inst2.text().strip(),
                self.in_inst1.text().strip(),
                self.in_count.text().strip(),
                self.in_unit_price.text().strip(),
                self.in_type.text().strip(),
                self.in_address.text().strip(),
                self.in_contact.text().strip(),
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
            cur.execute("DELETE FROM implant WHERE pid=?", (self.selected_id,))
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
                SELECT cont, con2, con1, con, price, type, adress, contact, date, age, gender, name, pid
                FROM implant
                WHERE {col} LIKE ?
            """, ("%" + val + "%",))
            rows = cur.fetchall()

        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))


if __name__ == "__main__":
    app = QApplication([])
    w = ImplantWindow()
    w.show()
    app.exec_()
