from Modules.database import koneksi_db
from datetime import datetime


def transaksi_penjualan():
    conn, cursor = koneksi_db()

    keranjang = []
    total = 0

    while True:

        # Menampilkan daftar produk
        cursor.execute("SELECT * FROM produk")
        produk = cursor.fetchall()

        print("\n===== DAFTAR PRODUK =====")
        print("ID | Nama Produk | Harga | Stok")

        for p in produk:
            print(f"{p[0]} | {p[1]} | Rp{p[3]} | {p[4]}")

        try:
            id_produk = int(input("\nMasukkan ID Produk : "))
            jumlah = int(input("Jumlah beli : "))
        except ValueError:
            print("Input harus berupa angka!")
            continue

        cursor.execute(
            "SELECT * FROM produk WHERE id=?",
            (id_produk,)
        )

        data = cursor.fetchone()

        if not data:
            print("Produk tidak ditemukan.")
            continue

        nama_produk = data[1]
        harga_jual = data[3]
        stok = data[4]

        if jumlah <= 0:
            print("Jumlah pembelian harus lebih dari 0.")
            continue

        # Hitung jumlah barang yang sudah ada di keranjang
        jumlah_di_keranjang = 0

        for item in keranjang:
            if item["id_produk"] == id_produk:
                jumlah_di_keranjang += item["jumlah"]

        stok_tersedia = stok - jumlah_di_keranjang

        if jumlah > stok_tersedia:
            print(f"Stok tidak mencukupi! Sisa stok yang dapat dibeli: {stok_tersedia}")
            continue

        # Cek apakah produk sudah ada di keranjang
        ditemukan = False

        for item in keranjang:
            if item["id_produk"] == id_produk:
                item["jumlah"] += jumlah
                item["subtotal"] = item["jumlah"] * item["harga"]
                ditemukan = True
                break

        if not ditemukan:
            keranjang.append({
                "id_produk": id_produk,
                "nama_produk": nama_produk,
                "harga": harga_jual,
                "jumlah": jumlah,
                "subtotal": harga_jual * jumlah
            })

        # Hitung ulang total
        total = sum(item["subtotal"] for item in keranjang)

        lagi = input("Tambah barang lain? (Y/T) : ")

        if lagi.upper() != "Y":
            break

    if len(keranjang) == 0:
        print("Tidak ada transaksi.")
        conn.close()
        return

    # ==========================
    # CETAK STRUK
    # ==========================
    print("\n==============================")
    print("        SMART RETAIL")
    print("==============================")

    for item in keranjang:
        print(
            f"{item['nama_produk']} "
            f"{item['jumlah']} x Rp{item['harga']} = Rp{item['subtotal']}"
        )

    print("------------------------------")
    print(f"TOTAL = Rp{total}")

    # Pembayaran
    while True:

        try:
            uang_bayar = int(input("Uang Bayar : Rp"))
        except ValueError:
            print("Masukkan angka!")
            continue

        if uang_bayar < total:
            print("Uang kurang!")
        else:
            break

    kembalian = uang_bayar - total

    print(f"Kembalian = Rp{kembalian}")

    # ==========================
    # SIMPAN TRANSAKSI
    # ==========================

    tanggal = datetime.now().strftime("%d-%m-%Y")

    cursor.execute(
        """
        INSERT INTO transaksi(tanggal,total_bayar)
        VALUES (?,?)
        """,
        (tanggal, total)
    )

    id_transaksi = cursor.lastrowid

    for item in keranjang:

        cursor.execute(
            """
            INSERT INTO detail_transaksi
            (id_transaksi,id_produk,jumlah,subtotal)
            VALUES (?,?,?,?)
            """,
            (
                id_transaksi,
                item["id_produk"],
                item["jumlah"],
                item["subtotal"]
            )
        )

        cursor.execute(
            """
            UPDATE produk
            SET stok = stok - ?
            WHERE id = ?
            """,
            (
                item["jumlah"],
                item["id_produk"]
            )
        )

    conn.commit()
    conn.close()

    print("\n===================================")
    print("Transaksi berhasil disimpan.")
    print("===================================")