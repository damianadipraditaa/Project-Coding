# Program Deret 1 sampai 30 dengan dua aturan khusus

# Kata yang digunakan (dibuat sendiri)
kata_pertama = "Dame "
kata_kedua = "Unn Grrr"

for angka in range(1, 31):
    aturan1 = (angka % 4 == 0)  # Aturan pertama: kelipatan 4
    aturan2 = (angka % 6 == 0)  # Aturan kedua: kelipatan 6

    # Menentukan output
    if aturan1 and aturan2:
        print(kata_pertama + kata_kedua)
    elif aturan1:
        print(kata_pertama)
    elif aturan2:
        print(kata_kedua)
    else:
        print(angka)
