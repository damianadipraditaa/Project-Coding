# Studi Kasus: Manajemen Inventaris Tokoh

inventaris = [
    {"Nama": "Iphone 16 Pro Max", "Stock": 10, "Harga": 21999000},
    {"Nama": "Case Iphone 16 Pro Max", "Stock": 15, "Harga": 2085000},
]

def tampilkan_produk():
    print("\n=== Daftar Produk===")
    for produk in inventaris:
        print(f"{produk['Nama']}- Stok: {produk['Stock']}- harga: Rp{produk['Harga']}")
tampilkan_produk()

def tambah_produk(nama, stok, harga):
    inventaris.append({"Nama": nama, "Stock": stok, "Harga": harga})
    print(f"\nProduk '{nama}' berhasil ditambahkan!")

tambah_produk("Earphone", 20, 4800000),
   
tampilkan_produk()