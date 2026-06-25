from Modules.database import koneksi_db

def login():
    conn, cursor = koneksi_db()

    print("\n===== LOGIN SMART RETAIL =====")

    username = input("Username : ").strip()
    password = input("Password : ").strip()

    if not username or not password:
         print("Username dan password tidak boleh kosong!")
         return None

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )

    hasil = cursor.fetchone()

    conn.close()

    if hasil:
        role = hasil[0]
        print("Login berhasil sebagai", role)
        return role
    else:
        print("Username atau password salah!")
        return None