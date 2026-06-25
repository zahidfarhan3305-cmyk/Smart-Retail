from Modules.database import koneksi_db


# Tambah Produk
def tambah_produk():
    conn, cursor = koneksi_db()

    nama = input("Nama Produk : ")
    harga_modal = int(input("Harga Modal : "))
    harga_jual = int(input("Harga Jual : "))
    stok = int(input("Stok : "))

    cursor.execute("""
    INSERT INTO produk (nama_produk, harga_modal, harga_jual, stok)
    VALUES (?, ?, ?, ?)
    """, (nama, harga_modal, harga_jual, stok))

    conn.commit()
    conn.close()

    print("Produk berhasil ditambahkan!")


# Lihat Produk
def lihat_produk():
    conn, cursor = koneksi_db()

    cursor.execute("SELECT * FROM produk")
    data = cursor.fetchall()

    print("\n===== DAFTAR PRODUK =====")
    print("ID | Nama Produk | Harga Jual | Stok")

    for row in data:
        print(f"{row[0]} | {row[1]} | Rp{row[3]} | {row[4]}")

    conn.close()


# Update Produk
def update_produk():
    conn, cursor = koneksi_db()

    lihat_produk()

    id_produk = int(input("\nMasukkan ID produk yang ingin diubah : "))

    nama = input("Nama baru : ")
    harga_jual = int(input("Harga jual baru : "))
    stok = int(input("Stok baru : "))

    cursor.execute("""
    UPDATE produk
    SET nama_produk=?, harga_jual=?, stok=?
    WHERE id=?
    """, (nama, harga_jual, stok, id_produk))

    conn.commit()
    conn.close()

    print("Produk berhasil diperbarui!")


# Hapus Produk
def hapus_produk():
    conn, cursor = koneksi_db()

    lihat_produk()

    id_produk = int(input("\nMasukkan ID produk yang akan dihapus : "))

    konfirmasi = input("Yakin menghapus produk? (Y/T) : ")

    if konfirmasi.upper() == "Y":
        cursor.execute("DELETE FROM produk WHERE id=?", (id_produk,))
        conn.commit()
        print("Produk berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

    conn.close()


# Cari berdasarkan nama
def cari_nama_produk():
    conn, cursor = koneksi_db()

    keyword = input("Masukkan nama produk : ")

    cursor.execute("""
    SELECT * FROM produk
    WHERE nama_produk LIKE ?
    """, ('%' + keyword + '%',))

    hasil = cursor.fetchall()

    if hasil:
        print("\nHasil pencarian:")
        for row in hasil:
            print(f"ID:{row[0]} | {row[1]} | Rp{row[3]} | Stok:{row[4]}")
    else:
        print("Produk tidak ditemukan.")

    conn.close()


# Cari berdasarkan ID
def cari_id_produk():
    conn, cursor = koneksi_db()

    id_produk = int(input("Masukkan ID produk : "))

    cursor.execute("""
    SELECT * FROM produk
    WHERE id=?
    """, (id_produk,))

    hasil = cursor.fetchone()

    if hasil:
        print("\nProduk ditemukan:")
        print(f"ID:{hasil[0]}")
        print(f"Nama:{hasil[1]}")
        print(f"Harga Jual: Rp{hasil[3]}")
        print(f"Stok:{hasil[4]}")
    else:
        print("Produk tidak ditemukan.")

    conn.close()


# Menu Produk
def menu_produk():
    while True:
        print("\n===== MENU PRODUK =====")
        print("1. Tambah Produk")
        print("2. Lihat Produk")
        print("3. Update Produk")
        print("4. Hapus Produk")
        print("5. Cari Nama Produk")
        print("6. Cari ID Produk")
        print("0. Kembali")

        pilihan = input("Pilih menu : ")

        if pilihan == "1":
            tambah_produk()

        elif pilihan == "2":
            lihat_produk()

        elif pilihan == "3":
            update_produk()

        elif pilihan == "4":
            hapus_produk()

        elif pilihan == "5":
            cari_nama_produk()

        elif pilihan == "6":
            cari_id_produk()

        elif pilihan == "0":
            break

        else:
            print("Pilihan tidak tersedia!")