# Program Daftar Menu Minuman

# Daftar menu
menu = {
    1: ("Es Teh", 6000),
    2: ("Kopi ", 4000),
    3: ("Jus ", 3000),
    4: ("Ayam Geprek", 12000),
    5: ("Nasi Padang", 10000)
}

print("=== Daftar Menu ===")
for nomor, (nama, harga) in menu.items():
    print(f"{nomor}. {nama} - Rp {harga}")

pesanan = []  # menyimpan pesanan

while True:
    pilihan = int(input("\nPilih menu (1-5): "))

    if pilihan in menu:
        nama, harga = menu[pilihan]
        jumlah = int(input(f"Berapa porsi {nama}? "))
        pesanan.append((nama, harga, jumlah))
    else:
        print("Pilihan tidak valid!")

    lanjut = input("Mau pesan lagi? (y/n): ").lower()
    if lanjut != "y":
        break

# Hitung total
subtotal = 0
print("\n=== Struk Pembelian ===")
for nama, harga, jumlah in pesanan:
    total_harga = harga * jumlah
    subtotal += total_harga
    print(f"{nama} x{jumlah} = Rp {total_harga}")

pajak = int(subtotal * 0.10)
total_bayar = subtotal + pajak

print("---------------------------")
print("Subtotal    : Rp", subtotal)
print("Pajak 10%   : Rp", pajak)
print("Total Bayar : Rp", total_bayar)
print("===========================")
