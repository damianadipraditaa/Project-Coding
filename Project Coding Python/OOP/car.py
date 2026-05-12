class Car:
    def __init__(self, merek, model, tahun, harga):
        self.merek = merek
        self.model = model
        self.tahun = tahun
        self.harga = harga

    def fungsi(self):
        print("Mobil siap dikendarai")

lamborghini = Car("Lamborghini", "Aventador", 2020, 500000000)
print(lamborghini.merek)
print(lamborghini.model)
print(lamborghini.tahun)
print(lamborghini.harga)
lamborghini.fungsi()
