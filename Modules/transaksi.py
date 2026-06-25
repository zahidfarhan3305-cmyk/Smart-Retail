from Modules.database import koneksi_db
from datetime import datetime


def transaksi_penjualan():
    conn, cursor = koneksi_db()

    keranjang = []
    total = 0

    while True:

        # tampilkan produk
        cursor.execute("SELECT * FROM produk")
        produk = cursor.fetchall()

        print("\n===== DAFTAR PRODUK =====")
        print("ID | Nama Produk | Harga | Stok")

        for p in produk:
            print(f"{p[0]} | {p[1]} | Rp{p[3]} | {p[4]}")

        id_produk = int(input("\nMasukkan ID Produk : "))
        jumlah = int(input("Jumlah beli : "))

        cursor.execute("SELECT * FROM produk WHERE id=?", (id_produk,))
        data = cursor.fetchone()

        if data:

            nama_produk = data[1]
            harga_jual = data[3]
            stok = data[4]

            if jumlah <= 0:
                print("Jumlah pembelian harus lebih dari 0.")
                return

            if jumlah > stok:
                print("Stok tidak mencukupi.")
                return
            else:
                subtotal = harga_jual * jumlah

                keranjang.append({
                    "id_produk": id_produk,
                    "nama_produk": nama_produk,
                    "harga": harga_jual,
                    "jumlah": jumlah,
                    "subtotal": subtotal
                })

                total += subtotal

        else:
            print("Produk tidak ditemukan.")

        lagi = input("Tambah barang lain? (Y/T) : ")

        if lagi.upper() != "Y":
            break

    # Cetak struk
    print("\n======================")
    print("      SMART RETAIL")
    print("======================")

    for item in keranjang:
        print(
            f"{item['nama_produk']} "
            f"{item['jumlah']} x {item['harga']} = Rp{item['subtotal']}"
        )

    print("----------------------")
    print("TOTAL = Rp", total)

    # pembayaran
    while True:

        uang_bayar = int(input("Uang Bayar : Rp"))

        if uang_bayar < total:
            print("Uang kurang!")
        else:
            break

    kembalian = uang_bayar - total

    print("Kembalian = Rp", kembalian)

    # simpan transaksi
    tanggal = datetime.now().strftime("%d-%m-%Y")

    cursor.execute(
        "INSERT INTO transaksi(tanggal,total_bayar) VALUES (?,?)",
        (tanggal, total)
    )

    id_transaksi = cursor.lastrowid

    # simpan detail transaksi dan update stok
    for item in keranjang:

        cursor.execute("""
        INSERT INTO detail_transaksi
        (id_transaksi,id_produk,jumlah,subtotal)
        VALUES (?,?,?,?)
        """,
        (
            id_transaksi,
            item["id_produk"],
            item["jumlah"],
            item["subtotal"]
        ))

        cursor.execute("""
        UPDATE produk
        SET stok = stok - ?
        WHERE id = ?
        """,
        (
            item["jumlah"],
            item["id_produk"]
        ))

    conn.commit()
    print("\n===================================")
    print("Transaksi berhasil disimpan.")
    print("===================================")
    conn.close()

    print("Transaksi berhasil disimpan.")