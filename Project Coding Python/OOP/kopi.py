class Kopi:
    def __init__(self, jenis, rasa, harga):
        self.jenis = jenis
        self.rasa = rasa
        self.harga = harga

    def fungsi(self):
        print("Kopi siap diseduh")

kopi_robusta = Kopi("Robusta", "Pahit", 15000)

print(kopi_robusta.jenis)
print(kopi_robusta.rasa)
print(kopi_robusta.harga)
kopi_robusta.fungsi()