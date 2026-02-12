# ==========================================
# database.py
# ==========================================
# ملف إنشاء قاعدة بيانات Easy Clinic
# يحتوي على جميع الجداول الخاصة بالمشروع
# ==========================================

import sqlite3


def create_db():
    """
    إنشاء قاعدة البيانات والجداول إذا لم تكن موجودة
    """

    # الاتصال بقاعدة البيانات
    con = sqlite3.connect("clinic.db")
    cur = con.cursor()

    # ==========================================
    # جدول الأشعة
    # ==========================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS xrays (
            xid INTEGER PRIMARY KEY AUTOINCREMENT,
            adress TEXT,
            contact TEXT,
            price TEXT,
            state TEXT,
            date TEXT,
            age TEXT,
            gender TEXT,
            name TEXT
        )
    """)

    # ==========================================
    # جدول العلاجات السنية
    # ==========================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dental (
            aid INTEGER PRIMARY KEY AUTOINCREMENT,
            adress TEXT,
            contact TEXT,
            state TEXT,
            date TEXT,
            age TEXT,
            gender TEXT,
            name TEXT
        )
    """)

    # ==========================================
    # جدول الزرعات
    # ==========================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS implant (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            cont TEXT,
            con2 TEXT,
            con1 TEXT,
            con TEXT,
            price TEXT,
            type TEXT,
            adress TEXT,
            contact TEXT,
            date TEXT,
            age TEXT,
            gender TEXT,
            name TEXT
        )
    """)

    # ==========================================
    # جدول الحشوات
    # ==========================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS press (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            cont TEXT,
            con TEXT,
            price TEXT,
            type TEXT,
            adress TEXT,
            contact TEXT,
            date TEXT,
            age TEXT,
            gender TEXT,
            name TEXT
        )
    """)

    # حفظ التعديلات
    con.commit()

    # عرض الجداول الموجودة (للتأكد)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("✅ Tables in clinic.db:", tables)

    # إغلاق الاتصال
    con.close()


# تشغيل إنشاء القاعدة عند تشغيل الملف
if __name__ == "__main__":
    create_db()
