class Laptop:
    def __init__(self, merk, tipe, harga):
        self.merk = merk
        self.tipe = tipe
        self.harga = harga
    def fungsi(self):
        print("laptop siap di produksi")

lenovo = Laptop("Lenovo", "Legion 5", 15000000)
print(lenovo.merk)
print(lenovo.tipe)
print(lenovo.harga)
lenovo.fungsi()