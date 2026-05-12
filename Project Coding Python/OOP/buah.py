class Buah:
    def __init__(self,harga,warna,rasa):
        self.harga = harga
        self.warna = warna
        self.rasa = rasa
    
    def fungsi(self):
        print("Dijual")
        
buah_naga = Buah("9000","merah","manis")

print(buah_naga.harga)
print(buah_naga.rasa)
print(buah_naga.warna)
buah_naga.fungsi()