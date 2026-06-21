import sqlite3
import csv

def registrasi():
    print("Selamat Datang di Scholar-Track")


    nim = input("Masukan NIM  : ")
    nama = input("Masukan Nama  : ")
    password = input("Masukan Password  : ")

    ipk = float(input("Masukan IPK  : "))
    penghasilan = int(input("Masukan Penghasilan  :"))
    tanggungan = int(input("Masukan Jumlah Tanggungan  :"))

    if ipk < 3.00:
        print("Maaf.")
        print("Anda tidak memenuhi syarat minimum IPK.")

    elif penghasilan < 0:
        print("Penghasilan tidak boleh negatif.")

    elif tanggungan < 1:
        print("Jumlah tanggungan minimal 1.")

    else:
        conn = sqlite3.connect("scholar_track.db")
        cursor = conn.cursor()

        cursor.execute("""
                   INSERT INTO mahasiswa
                   (nim, nama, password, ipk, penghasilan, tanggungan)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (nim, nama, password, ipk, penghasilan, tanggungan))
        conn.commit()
        conn.close()
        print("Registrasi berhasil!")

        print("\n===== DATA MAHASISWA =====")
        print("NIM  :", nim)
        print("Nama  :", nama)
        print("Password  :", password)
        print("IPK  :", ipk)
        print("Penghasilan  :", penghasilan)
        print("Tanggungan  :", tanggungan)

def login_mahasiswa():

    nim = input("Masukan NIM  : ")
    password = input("Masukan Password  : ")

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM mahasiswa
    WHERE nim = ? AND password = ?
    """, (nim, password))

    hasil = cursor.fetchone()

    conn.close()

    if hasil:
        print("Login Berhasil!")
        menu_mahasiswa(nim)
    else:
        print("NIM atau Password Salah! ")

def menu_utama():
    while True:

        print("\n===== SCHOLAR TRACK =====")
        print("1. Registrasi Mahasiswa")
        print("2. Login Mahasiswa")
        print("3. Login Admin")
        print("4. Keluar")

        pilihan = input("Pilih Menu  : ")

        if pilihan == "1":
            registrasi()

        elif pilihan == "2":
            login_mahasiswa()

        elif pilihan == "3":
            login_admin()

        elif pilihan == "4":
            print("Terima Kasih")
            break

        else:
            print("Pilihan tidak tersedia")

def login_admin():
    username = input("Masukan Username  : ")
    password = input("Masuka Password  : ")

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM admin
    WHERE username = ? AND password = ?
    """, (username, password))

    hasil = cursor.fetchone()

    conn.close()

    if hasil:
        print("Login Admin Berhasil!")
        menu_admin()
    else:
        print("Username atau Password Salah!")

def lihat_mahasiswa():

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM mahasiswa
    """)

    data_mahasiswa = cursor.fetchall()

    conn.close()

    print("\n===== DAFTAR MAHASISWA =====")

    for mahasiswa in data_mahasiswa:
        print(mahasiswa)

def menu_admin():
    while True:
        print("\n=====MENU ADMIN =====")
        print("1. Lihat Pendaftar")
        print("2. Sorting Berdasarkan IPK")
        print("3. Sorting Berdasarkan Penghasilan")
        print("4. Hitung Skor Beasiswa")
        print("5. Tentukan Kelulusan")
        print("6. Lihat Penerima Beasiswa")
        print("7. Ranking Mahasiswa")
        print("8. Hapus Mahasiswa")
        print("9. Cari Mahasiswa")
        print("10. Statistik Beasiswa")
        print("11. Export CSV")
        print("12. Logout")

        pilihan = input("Pilih Menu  : ")

        if pilihan == "1":
            lihat_mahasiswa()
        
        elif pilihan == "2":
            sorting_ipk()

        elif pilihan == "3":
            sorting_penghasilan()

        elif pilihan == "4":
            hitung_skor()

        elif pilihan == "5":
            tentukan_kelulusan()

        elif pilihan == "6":
            lihat_penerima_beasiswa()
        
        elif pilihan == "7":
            ranking_mahasiswa()

        elif pilihan == "8":
            hapus_mahasiswa()

        elif pilihan == "9":
            cari_mahasiswa()

        elif pilihan == "10":
            statistik_beasiswa()

        elif pilihan == "11":
            export_csv()

        elif pilihan == "12":
            print("Logout Berhasil")
            break
            

        else:
            print("Pilihan tidak tersedia")

def hitung_skor():

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nim, ipk, penghasilan, tanggungan
    FROM mahasiswa
    """)

    data_mahasiswa = cursor.fetchall()

    for mahasiswa in data_mahasiswa:

        nim = mahasiswa[0]
        ipk = mahasiswa[1]
        penghasilan = mahasiswa[2]
        tanggungan = mahasiswa[3]

        if penghasilan <= 2000000:
            nilai_ekonomi = 100
        
        elif penghasilan <=4000000:
            nilai_ekonomi = 80
        
        elif penghasilan <=6000000:
            nilai_ekonomi = 60

        else:
            nilai_ekonomi = 40

        skor = (ipk * 40) + (nilai_ekonomi * 60)


        cursor.execute("""
        UPDATE mahasiswa
        SET skor_akhir = ?
        WHERE nim = ?
        """, (skor, nim))
    conn.commit()
    conn.close()

    print("Perhitungan skor berhasil!")

def tentukan_kelulusan():

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nim, skor_akhir
    FROM mahasiswa
    """)
    data_mahasiswa = cursor.fetchall()
    ranking = 1

    for mahasiswa in data_mahasiswa:

        nim = mahasiswa[0]

        if ranking <= 50:
            status = "DITERIMA"
        else:
            status = "DITOLAK"

        cursor.execute("""
        UPDATE mahasiswa
        SET skor_akhir = ?
        WHERE nim = ?
        """, (status, nim))
        
        print(nim, "=", status)

        ranking += 1


    
    conn.commit()
    conn.close()

    print("Penentuan Kelulusan Berhasil!")

def lihat_penerima_beasiswa():

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nim, nama, skor_akhir
    FROM mahasiswa
    WHERE status_seleksi = ?
    """, ("DITERIMA",))

    data_mahasiswa = cursor.fetchall()

    for mahasiswa in data_mahasiswa:

        nim = mahasiswa[0]
        nama = mahasiswa[1]
        skor = mahasiswa[2]

        print("\n===== PENERIMA BEASISWA =====")

        print("NIM :", nim)
        print("Nama :", nama)
        print("Skor :", skor)
        print("------------------")

def ranking_mahasiswa():
    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nama, skor_akhir
    FROM mahasiswa
    ORDER BY skor_akhir DESC
    """)

    data_mahasiswa = cursor.fetchall()

    conn.close()

    print("\n===== RANKING MAHASISWA =====")

    ranking = 1

    for mahasiswa in data_mahasiswa:

        nama = mahasiswa[0]
        skor = mahasiswa[1]

        print("Ranking", ranking)
        print("Nama :", nama)
        print("Skor :", skor)
        print("-----------------")

        ranking += 1

def hapus_mahasiswa():

    nim = input("Masukan NIM yang akan dihapus :")

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM mahasiswa
    WHERE nim = ?
    """, (nim,))

    conn.commit()
    conn.close()

    print("Mahasiswa berhasil dihapus!")

def cari_mahasiswa():
    nim = input("Masukan NIM yang dicari  :")

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""               
    SELECT *
    From mahasiswa
    WHERE nim = ?
    """,(nim,))

    hasil = cursor.fetchone()

    conn.close()

    if hasil:
        print("\n===== DATA MAHASISWA =====")

        print("NIM  :", hasil[0])
        print("Nama  :", hasil[1])
        print("Password  :", hasil[2])
        print("IPK  :", hasil[3])
        print("Penghasilan  :", hasil[4])
        print("Tanggungan  :", hasil[5])
        print("Skor Akhir  :", hasil[6])
        print("Status  :", hasil[7])

    else:
        print("Mahasiswa tidak ditemukan!")

def statistik_beasiswa():
    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM mahasiswa
    """)

    jumlah_mahasiswa = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM mahasiswa
    WHERE status_seleksi = "DITERIMA"
    """)

    jumlah_lolos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM mahasiswa
    WHERE status_seleksi = "DITOLAK"
    """)

    jumlah_tidak_lolos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT AVG(skor_akhir)
    FROM mahasiswa
    """)

    rata_rata = cursor.fetchone()[0]

    cursor.execute("""
    SELECT MAX(skor_akhir)
    FROM mahasiswa
    """)

    skor_tertinggi = cursor.fetchone()[0]

    cursor.execute("""
    SELECT MIN(skor_akhir)
    FROM mahasiswa
    """)

    skor_terrendah = cursor.fetchone()[0]

    conn.close

    print("\n===== STATISTIK BEASISWA =====")

    print("Jumlah Mahasiswa  :", jumlah_mahasiswa)
    print("Jumlah Lolos  :", jumlah_lolos)
    print("Jumlah Tidak Lolos  :", jumlah_tidak_lolos)
    print("Rata-rata Skor  :", rata_rata)
    print("Skor Tertinggi  :", skor_tertinggi)
    print("Skor terrendah  :", skor_terrendah)

def menu_mahasiswa(nim):
    while True:

        print("\n===== MENU MAHASISWA =====")
        print("1. Profil Saya")
        print("2. Lihat Skor Seleksi")
        print("3. Lihat Status Seleksi")
        print("4. Logout")

        pilihan = input("Pilih Menu :")

        if pilihan == "1":
            profil_saya(nim)
        elif pilihan == "2":
            lihat_skor(nim)
        elif pilihan == "3":
            lihat_status(nim)
        elif pilihan == "4":
            print("Berhasil Logout")
            break
        else:
            print("Pilihan tidak tersedia")

def profil_saya(nim):

    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nim, nama, ipk, penghasilan, tanggungan
    FROM mahasiswa
    WHERE nim = ?
    """, (nim,))

    hasil = cursor.fetchone()

    conn.close()

    print("\n===== PROFIL SAYA =====")
    print("NIM  :", hasil[0])
    print("Nama  :", hasil[1])
    print("IPK  :", hasil[2])
    print("Penghasilan  :", hasil[3])
    print("Tanggungan  :", hasil[4])

def lihat_skor(nim):
    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT skor_akhir
    FROM mahasiswa
    WHERE nim = ?
    """, (nim,))

    hasil = cursor.fetchone()

    conn.close()

    print("Skor Akhir  :", hasil[0])

def lihat_status(nim):
    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT status_seleksi
    FROM mahasiswa
    WHERE nim = ?
    """, (nim,))

    hasil = cursor.fetchone()

    conn.close()

    print("Status_seleksi  :", hasil[0])

def sorting_ipk():
    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nama, ipk
    FROM mahasiswa
    ORDER BY ipk DESC
    """)

    data_mahasiswa = cursor.fetchall()

    conn.close()

    print("\n===== SORTING IPK =====")
    ranking = 1
    
    for mahasiswa in data_mahasiswa:
        nama = mahasiswa[0]
        ipk = mahasiswa[1]

        print("Ranking  :", ranking)
        print("Nama  :", nama)
        print("IPK  :", ipk)
        print("--------------------")

        ranking += 1

def sorting_penghasilan():
    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nama, penghasilan
    FROM mahasiswa
    ORDER BY penghasilan ASC
    """)

    data_mahasiswa = cursor.fetchall()

    conn.close()

    print("\n===== SORTING PENGHASILAN =====")
    ranking = 1
    
    for mahasiswa in data_mahasiswa:
        nama = mahasiswa[0]
        penghasilan = mahasiswa[1]

        print("Ranking  :", ranking)
        print("Nama  :", nama)
        print("Penghasilan  :", penghasilan)
        print("--------------------")

        ranking += 1

def export_csv():
    conn = sqlite3.connect("scholar_track.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nim, nama, ipk, skor_akhir, status_seleksi
    FROM mahasiswa
    """)

    data_mahasiswa = cursor.fetchall()

    with open("hasil_seleksi.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "NIM",
            "Nama",
            "IPK",
            "Skor Akhir",
            "Status Seleksi"
        ])
        writer.writerows(data_mahasiswa)
    conn.close()
    print("Export CSV berhasil!")

menu_utama()
