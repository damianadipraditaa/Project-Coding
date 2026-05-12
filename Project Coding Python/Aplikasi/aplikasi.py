import os

# Data disimpan di list (bisa dikembangkan ke JSON nanti)
daftar_tugas = []

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def tambah_tugas():
    clear()
    print("=== Tambah Tugas Baru ===")
    tugas = input("Masukkan nama tugas: ")
    if tugas:
        daftar_tugas.append(tugas)
        print(f"Ok, '{tugas}' berhasil ditambahkan!")
    else:
        print("[X] Nama tugas tidak boleh kosong!")
    input("\nTekan Enter untuk kembali...")

def hapus_tugas():
    clear()
    print("=== Hapus Tugas ===")
    if not daftar_tugas:
        print("Daftar masih kosong.")
    else:
        for i, tugas in enumerate(daftar_tugas, 1):
            print(f"{i}. {tugas}")
        
        try:
            pilihan = int(input("\nNomor tugas yang mau dihapus: "))
            if 1 <= pilihan <= len(daftar_tugas):
                terhapus = daftar_tugas.pop(pilihan - 1)
                print(f"'{terhapus}' telah dihapus!")
            else:
                print("[X] Nomor tidak ada dalam daftar.")
        except ValueError:
            print("[X] Masukkan angka, bukan huruf!")
    input("\nTekan Enter untuk kembali...")

def tampilkan_tugas():
    clear()
    print("=== Daftar Semua Tugas ===")
    if not daftar_tugas:
        print("Belum ada tugas yang dicatat. ( -_o)")
    else:
        for i, tugas in enumerate(daftar_tugas, 1):
            print(f"{i}. [ ] {tugas}")
    input("\nTekan Enter untuk kembali...")

def menu_tugas():
    while True:
        clear()
        print("\033[36m=== Task Manager Simple ===") # Warna Cyan
        print("1. Tambah tugas")
        print("2. Hapus tugas")
        print("3. Tampilkan semua tugas")
        print("4. Keluar")

        pilihan = input("\nPilih menu (1/2/3/4): ")

        if pilihan == "1":
            tambah_tugas()
        elif pilihan == "2":
            hapus_tugas()
        elif pilihan == "3":
            tampilkan_tugas()
        elif pilihan == "4":
            print("Program selesai. Selamat istirahat! ✌︎")
            break
        else:
            print("[X] Pilihan tidak valid!")
            input("Tekan Enter untuk lanjut...")

# Menjalankan program
if __name__ == "__main__":
    menu_tugas()