import pymysql

try:
    # Hubungkan langsung
    db = pymysql.connect(
        host='localhost', 
        user='root', 
        password='', 
        database='dbberita'
    )
    print("✅ Koneksi Berhasil!")
    
    # Tutup jika sudah selesai cek
    db.close()

except Exception as e:
    print(f"❌ Gagal: {e}")