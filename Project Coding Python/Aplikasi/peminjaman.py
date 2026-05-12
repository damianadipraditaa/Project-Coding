# Solution App - Sistem Peminjaman Buku Perpustakaan
# Dibuat untuk Damian Adipradita Daniswara
# Fitur: pinjam, kembali, cek status, blacklist otomatis jika telat, data tersimpan permanen

import datetime
import json
import os
from typing import Dict

# Lokasi file penyimpanan data
DATA_FOLDER = "perpustakaan_data"
BORROW_FILE = os.path.join(DATA_FOLDER, "peminjaman.json")
BLACKLIST_FILE = os.path.join(DATA_FOLDER, "blacklist.json")
BUKU_FILE = os.path.join(DATA_FOLDER, "daftar_buku.json")

# Durasi pinjam default (dalam hari)
MAKS_HARI_PINJAM = 7

def buat_folder_jika_belum_ada():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

def load_json(file_path: str, default: dict = None) -> dict:
    if default is None:
        default = {}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(data: dict, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Inisialisasi data
buat_folder_jika_belum_ada()

daftar_buku: Dict[str, dict] = load_json(BUKU_FILE, {
    "Matematika SMA": {"jumlah": 5, "tersedia": 5},
    "Fisika Kelas X": {"jumlah": 3, "tersedia": 3},
    "Bahasa Indonesia": {"jumlah": 10, "tersedia": 8},
    "Sejarah Indonesia": {"jumlah": 4, "tersedia": 4},
    "Kimia Dasar": {"jumlah": 6, "tersedia": 5},
})

peminjaman: Dict[str, dict] = load_json(BORROW_FILE)        # key: judul_buku
blacklist: Dict[str, dict] = load_json(BLACKLIST_FILE)      # key: nama_peminjam

def simpan_semua_data():
    save_json(daftar_buku, BUKU_FILE)
    save_json(peminjaman, BORROW_FILE)
    save_json(blacklist, BLACKLIST_FILE)

def tambah_buku_baru():
    judul = input("Masukkan judul buku baru: ").strip()
    if judul in daftar_buku:
        print("Buku sudah ada di daftar!")
        return
    try:
        jumlah = int(input("Jumlah buku: "))
        if jumlah < 1:
            print("Jumlah harus lebih dari 0!")
            return
        daftar_buku[judul] = {"jumlah": jumlah, "tersedia": jumlah}
        simpan_semua_data()
        print(f"Buku '{judul}' berhasil ditambahkan.")
    except ValueError:
        print("Masukkan angka yang valid!")

def pinjam_buku():
    nama = input("Nama peminjam (lengkap): ").strip()
    if not nama:
        print("Nama tidak boleh kosong!")
        return

    if nama in blacklist:
        info = blacklist[nama]
        print(f"\n{nama} sedang BLACKLIST!")
        print(f"Alasan : {info.get('alasan', 'Tidak diketahui')}")
        print(f"Sejak  : {info.get('tanggal_blacklist', '-')}")
        return

    print("\nDaftar buku yang tersedia:")
    for judul, info in daftar_buku.items():
        if info["tersedia"] > 0:
            print(f"- {judul} (tersedia: {info['tersedia']})")

    judul = input("\nJudul buku yang ingin dipinjam: ").strip()
    if judul not in daftar_buku:
        print("Buku tidak ditemukan!")
        return
    if daftar_buku[judul]["tersedia"] < 1:
        print("Maaf, buku sedang habis dipinjam semua.")
        return

    hari_ini = datetime.date.today()
    batas_kembali = hari_ini + datetime.timedelta(days=MAKS_HARI_PINJAM)

    peminjaman[judul] = {
        "peminjam": nama,
        "tanggal_pinjam": str(hari_ini),
        "batas_kembali": str(batas_kembali),
    }

    daftar_buku[judul]["tersedia"] -= 1
    simpan_semua_data()

    print(f"\nSUKSES!")
    print(f"Buku     : {judul}")
    print(f"Peminjam : {nama}")
    print(f"Pinjam   : {hari_ini}")
    print(f"Kembali  : {batas_kembali} (maks {MAKS_HARI_PINJAM} hari)")

def kembalikan_buku():
    judul = input("Judul buku yang dikembalikan: ").strip()
    if judul not in peminjaman:
        print("Buku tersebut tidak sedang dipinjam.")
        return

    data = peminjaman[judul]
    nama = data["peminjam"]
    batas = datetime.date.fromisoformat(data["batas_kembali"])
    hari_ini = datetime.date.today()

    del peminjaman[judul]
    daftar_buku[judul]["tersedia"] += 1

    if hari_ini > batas:
        telat_hari = (hari_ini - batas).days
        print(f"\nPERINGATAN: TELAT {telat_hari} hari!")
        blacklist[nama] = {
            "alasan": f"Terlambat mengembalikan buku '{judul}' ({telat_hari} hari)",
            "tanggal_blacklist": str(hari_ini),
            "buku_penyebab": judul
        }
        print(f"{nama} telah dimasukkan ke BLACKLIST.")
    else:
        print(f"Buku '{judul}' dikembalikan tepat waktu oleh {nama}. Terima kasih!")

    simpan_semua_data()

def lihat_status():
    print("\n=== STATUS PEMINJAMAN ===")
    if not peminjaman:
        print("Belum ada buku yang dipinjam.")
    else:
        for judul, data in peminjaman.items():
            batas = datetime.date.fromisoformat(data["batas_kembali"])
            sisa = (batas - datetime.date.today()).days
            status = f"telat {abs(sisa)} hari" if sisa < 0 else f"sisa {sisa} hari"
            print(f"- {judul:20} | {data['peminjam']:20} | {status}")

def lihat_blacklist():
    print("\n=== DAFTAR BLACKLIST ===")
    if not blacklist:
        print("Tidak ada anggota yang di-blacklist.")
    else:
        for nama, info in blacklist.items():
            print(f"- {nama}")
            print(f"  Alasan : {info['alasan']}")
            print(f"  Sejak  : {info['tanggal_blacklist']}")
            print()

def hapus_blacklist():
    nama = input("Nama yang ingin dihapus dari blacklist: ").strip()
    if nama in blacklist:
        del blacklist[nama]
        simpan_semua_data()
        print(f"{nama} telah dihapus dari blacklist.")
    else:
        print("Nama tidak ditemukan di blacklist.")

def menu_utama():
    while True:
        print("\n" + "="*45)
        print("  SOLUTION APP - PERPUSTAKAAN SEKOLAH  ")
        print("="*45)
        print("1. Pinjam Buku")
        print("2. Kembalikan Buku")
        print("3. Lihat Status Peminjaman")
        print("4. Lihat Daftar Blacklist")
        print("5. Hapus Orang dari Blacklist (admin)")
        print("6. Tambah Buku Baru (admin)")
        print("0. Keluar")
        print("-"*45)

        pilihan = input("Pilih menu (0-6): ").strip()

        if pilihan == "1":
            pinjam_buku()
        elif pilihan == "2":
            kembalikan_buku()
        elif pilihan == "3":
            lihat_status()
        elif pilihan == "4":
            lihat_blacklist()
        elif pilihan == "5":
            hapus_blacklist()
        elif pilihan == "6":
            tambah_buku_baru()
        elif pilihan == "0":
            print("Terima kasih telah menggunakan Solution App!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    print("Selamat datang di Solution App Perpustakaan!")
    menu_utama()