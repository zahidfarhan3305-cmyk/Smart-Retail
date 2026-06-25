from Modules.database import koneksi_db
import matplotlib.pyplot as plt


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

    if len(data) == 0:
        print("Belum ada data penjualan.")
        return

    nama_produk = []
    jumlah_terjual = []

    for item in data:
        nama_produk.append(item[0])
        jumlah_terjual.append(item[1])

    plt.figure(figsize=(8, 5))
    plt.bar(nama_produk, jumlah_terjual)

    plt.xlabel("Produk")
    plt.ylabel("Jumlah Terjual")
    plt.title("Grafik Penjualan Produk")

    plt.tight_layout()
    plt.show()