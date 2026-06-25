import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "smart_retail.db")

def koneksi_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor


def buat_tabel():
    conn, cursor = koneksi_db()

    # Tabel users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Tabel produk
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_produk TEXT NOT NULL,
        harga_modal INTEGER NOT NULL,
        harga_jual INTEGER NOT NULL,
        stok INTEGER NOT NULL
    )
    """)

    # Tabel transaksi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanggal TEXT NOT NULL,
        total_bayar INTEGER NOT NULL
    )
    """)

    # Tabel detail transaksi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detail_transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_transaksi INTEGER,
        id_produk INTEGER,
        jumlah INTEGER,
        subtotal INTEGER,
        FOREIGN KEY (id_transaksi) REFERENCES transaksi(id),
        FOREIGN KEY (id_produk) REFERENCES produk(id)
    )
    """)

    conn.commit()
    conn.close()


def tambah_user_default():
    conn, cursor = koneksi_db()

    # Admin
    cursor.execute("""
    INSERT OR IGNORE INTO users(username, password, role)
    VALUES ('admin', 'admin123', 'admin')
    """)

    # Kasir
    cursor.execute("""
    INSERT OR IGNORE INTO users(username, password, role)
    VALUES ('kasir', 'kasir123', 'kasir')
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    buat_tabel()
    tambah_user_default()
    print("Database smart_retail.db berhasil dibuat.")