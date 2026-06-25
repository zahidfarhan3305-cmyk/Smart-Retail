from Modules.database import buat_tabel, tambah_user_default
from Modules.login import login
from Modules.produk import menu_produk
from Modules.transaksi import transaksi_penjualan
from Modules.laporan import menu_laporan

# Menu Admin
def menu_admin():

    while True:

        print("\n===== MENU ADMIN =====")
        print("1. Kelola Produk")
        print("2. Transaksi Penjualan")
        print("3. Laporan Penjualan")
        print("4. Logout")

        pilihan = input("Pilih menu : ")

        if pilihan == "1":
            menu_produk()

        elif pilihan == "2":
            transaksi_penjualan()

        elif pilihan == "3":
            menu_laporan()

        elif pilihan == "4":
            print("Logout berhasil.")
            break

        else:
            print("Pilihan tidak tersedia!")


# Menu Kasir
def menu_kasir():

    while True:

        print("\n===== MENU KASIR =====")
        print("1. Lihat Produk")
        print("2. Transaksi Penjualan")
        print("3. Logout")

        pilihan = input("Pilih menu : ")

        if pilihan == "1":
            menu_produk()

        elif pilihan == "2":
            transaksi_penjualan()

        elif pilihan == "3":
            print("Logout berhasil.")
            break

        else:
            print("Pilihan tidak tersedia!")


# Program utama
def main():

    # Membuat tabel database
    buat_tabel()

    # Menambahkan user default
    tambah_user_default()

    while True:

        role = login()

        if role == "admin":
            menu_admin()

        elif role == "kasir":
            menu_kasir()

        else:
            print("Login gagal.")

        ulang = input("\nLogin kembali? (Y/T) : ")

        if ulang.upper() != "Y":
            print("Program selesai.")
            break


if __name__ == "__main__":
    main()