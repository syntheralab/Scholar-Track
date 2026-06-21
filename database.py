import sqlite3

#Membuat koneksi databse
conn = sqlite3.connect("scholar_track.db")

#Membuat cursor
cursor = conn.cursor()

#Membuat tabel mahasiswa
cursor.execute("""
               CREATE TABLE IF NOT EXISTS mahasiswa (
               nim TEXT PRIMARY KEY,
               nama TEXT,
               password TEXT,
               ipk REAL,
               penghasilan INTEGER,
               tanggungan INTEGER,
               skor_akhir REAL,
               status_seleksi TEXT
               )
               """)
print("Tabel Mahasiswa Berhasil diBuat!")

#Membuat tabel admin
cursor.execute("""
               CREATE TABLE IF NOT EXISTS admin (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT,
               password TEXT
               )
               """)

print("Tabel Admin Berhasil diBuat!")

#Memasukan data admin
cursor.execute("""
               INSERT INTO admin (username, password)
               VALUES ('admin', 'admin123')
               """)


print("Admin berhasil ditambahkan!")

#Menutup Koneksi
conn.commit()
conn.close()