from Modules.database import koneksi_db
import csv
import matplotlib.pyplot as plt


# Jumlah transaksi
def jumlah_transaksi():
    conn, cursor = koneksi_db()

    cursor.execute("SELECT COUNT(*) FROM transaksi")
    jumlah = cursor.fetchone()[0]

    conn.close()

    print("Jumlah Transaksi :", jumlah)


# Total pendapatan
def total_pendapatan():
    conn, cursor = koneksi_db()

    cursor.execute("SELECT SUM(total_bayar) FROM transaksi")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    conn.close()

    print("=" * 40)
    print(f"Total Pendapatan : Rp {total:,}")
    print("=" * 40)


# Produk terlaris
def produk_terlaris():
    conn, cursor = koneksi_db()

    cursor.execute("""
    SELECT produk.nama_produk,
           SUM(detail_transaksi.jumlah) as total_terjual
    FROM detail_transaksi
    JOIN produk
    ON detail_transaksi.id_produk = produk.id
    GROUP BY produk.id
    ORDER BY total_terjual DESC
    LIMIT 1
    """)

    hasil = cursor.fetchone()

    conn.close()

    if hasil:
        print("Produk Terlaris :", hasil[0])
        print("Jumlah Terjual :", hasil[1])
    else:
        print("Belum ada transaksi.")


# Stok hampir habis
def stok_hampir_habis():
    conn, cursor = koneksi_db()

    cursor.execute("""
    SELECT nama_produk, stok
    FROM produk
    WHERE stok < 10
    """)

    hasil = cursor.fetchall()

    conn.close()

    if hasil:
        print("\nProduk yang harus direstock:")

        for data in hasil:
            print("-", data[0], "(", data[1], "pcs )")
    else:
        print("Tidak ada produk yang hampir habis.")


# Export laporan ke CSV (Bonus)
def export_csv():
    conn, cursor = koneksi_db()

    cursor.execute("""
    SELECT *
    FROM transaksi
    """)

    data = cursor.fetchall()

    with open("Smart-Retail/laporan_penjualan.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID Transaksi",
            "Tanggal",
            "Total Bayar"
        ])

        writer.writerows(data)

    conn.close()

    print("Laporan berhasil diexport ke laporan_penjualan.csv")


# Grafik penjualan (Bonus)
def grafik_penjualan():
    conn, cursor = koneksi_db()

    cursor.execute("""
    SELECT produk.nama_produk,
           SUM(detail_transaksi.jumlah)
    FROM detail_transaksi
    JOIN produk
    ON detail_transaksi.id_produk = produk.id
    GROUP BY produk.id
    """)

    data = cursor.fetchall()

    conn.close()

    if data:

        nama_produk = []
        jumlah_terjual = []

        for item in data:
            nama_produk.append(item[0])
            jumlah_terjual.append(item[1])

        plt.figure(figsize=(8,5))
        plt.bar(nama_produk, jumlah_terjual)

        plt.xlabel("Produk")
        plt.ylabel("Jumlah Terjual")
        plt.title("Grafik Penjualan Produk")

        plt.show()

    else:
        print("Belum ada data penjualan.")

def riwayat_transaksi():

    conn, cursor = koneksi_db()

    cursor.execute("""
        SELECT *
        FROM transaksi
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    print("\n===== RIWAYAT TRANSAKSI =====")

    for transaksi in data:
        print(transaksi)

    conn.close()       


# Menu laporan
def menu_laporan():

    while True:

        print("\n===== LAPORAN PENJUALAN =====")
        print("1. Jumlah Transaksi")
        print("2. Total Pendapatan")
        print("3. Produk Terlaris")
        print("4. Stok Hampir Habis")
        print("5. Export CSV")
        print("6. Grafik Penjualan")
        print("7. Riwayat Transaksi")
        print("0. Kembali")

        pilihan = input("Pilih menu : ")

        if pilihan == "1":
            jumlah_transaksi()

        elif pilihan == "2":
            total_pendapatan()

        elif pilihan == "3":
            produk_terlaris()

        elif pilihan == "4":
            stok_hampir_habis()

        elif pilihan == "5":
            export_csv()

        elif pilihan == "6":
            grafik_penjualan()
        elif pilihan == "7":
            riwayat_transaksi()

        elif pilihan == "0":
            break

        else:
            print("Pilihan tidak tersedia!")

