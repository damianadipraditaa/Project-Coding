import math

print("=== PROGRAM PERHITUNGAN BANGUN RUANG (LUAS & VOLUME) ===")
print("Dibuat khusus untuk Damian Adipradita D (X RPL1/16)")
print("Semua algoritma sudah diperbaiki dengan validasi (nilai >= 2)")
print("Fitur: Input → Validasi → Proses (tampil rumus + perhitungan) → Output\n")

while True:
    print("\n" + "="*50)
    print("PILIH BANGUN RUANG:")
    print("1. Segitiga (Luas)")
    print("2. Persegi (Luas)")
    print("3. Persegi Panjang (Luas)")
    print("4. Lingkaran (Luas)")
    print("5. Jajar Genjang (Luas)")
    print("6. Trapesium (Luas)")
    print("7. Belah Ketupat (Luas)")
    print("8. Layang-layang (Luas)")
    print("9. Kubus (Volume)")
    print("10. Balok (Volume)")
    print("0. Keluar Program")
    print("="*50)
    
    pilihan = input("Masukkan nomor pilihan (0-10): ").strip()
    
    if pilihan == "0":
        print("\nTerima kasih telah menggunakan program ini! 👍")
        break
    
    # ====================== 1. SEGITIGA ======================
    elif pilihan == "1":
        print("\n1) SEGITIGA (Luas)")
        print("Rumus: Luas = alas × tinggi × 0.5")
        
        while True:
            try:
                alas = float(input("Input alas      : "))
                tinggi = float(input("Input tinggi    : "))
                if alas >= 2 and tinggi >= 2:
                    break
                else:
                    print("❌ Nilai harus ≥ 2! Silakan input ulang.")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = alas * tinggi * 0.5
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = {alas} × {tinggi} × 0.5 = {luas}")
        print(f"✅ HASIL LUAS SEGITIGA = {luas:.2f} cm²")
    
    # ====================== 2. PERSEGI ======================
    elif pilihan == "2":
        print("\n2) PERSEGI (Luas)")
        print("Rumus: Luas = sisi × sisi")
        
        while True:
            try:
                sisi = float(input("Input sisi : "))
                if sisi >= 2:
                    break
                else:
                    print("❌ Nilai sisi harus ≥ 2! Silakan input ulang.")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = sisi * sisi
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = {sisi} × {sisi} = {luas}")
        print(f"✅ HASIL LUAS PERSEGI = {luas:.2f} cm²")
    
    # ====================== 3. PERSEGI PANJANG ======================
    elif pilihan == "3":
        print("\n3) PERSEGI PANJANG (Luas)")
        print("Rumus: Luas = panjang × lebar")
        
        while True:
            try:
                panjang = float(input("Input panjang : "))
                lebar = float(input("Input lebar   : "))
                if panjang >= 2 and lebar >= 2:
                    break
                else:
                    print("❌ Nilai panjang dan lebar harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = panjang * lebar
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = {panjang} × {lebar} = {luas}")
        print(f"✅ HASIL LUAS PERSEGI PANJANG = {luas:.2f} cm²")
    
    # ====================== 4. LINGKARAN ======================
    elif pilihan == "4":
        print("\n4) LINGKARAN (Luas)")
        print("Rumus: Luas = π × r × r")
        
        while True:
            try:
                r = float(input("Input jari-jari (r) : "))
                if r >= 2:
                    break
                else:
                    print("❌ Nilai jari-jari harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = math.pi * r * r
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = π × {r} × {r} ≈ {luas:.2f}")
        print(f"✅ HASIL LUAS LINGKARAN = {luas:.2f} cm²")
    
    # ====================== 5. JAJAR GENJANG ======================
    elif pilihan == "5":
        print("\n5) JAJAR GENJANG (Luas)")
        print("Rumus: Luas = alas × tinggi")
        
        while True:
            try:
                alas = float(input("Input alas   : "))
                tinggi = float(input("Input tinggi : "))
                if alas >= 2 and tinggi >= 2:
                    break
                else:
                    print("❌ Nilai alas dan tinggi harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = alas * tinggi
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = {alas} × {tinggi} = {luas}")
        print(f"✅ HASIL LUAS JAJAR GENJANG = {luas:.2f} cm²")
    
    # ====================== 6. TRAPESIUM ======================
    elif pilihan == "6":
        print("\n6) TRAPESIUM (Luas)")
        print("Rumus: Luas = (sisi atas + sisi bawah) × tinggi × 0.5")
        
        while True:
            try:
                atas = float(input("Input sisi atas   : "))
                bawah = float(input("Input sisi bawah  : "))
                tinggi = float(input("Input tinggi      : "))
                if atas >= 2 and bawah >= 2 and tinggi >= 2:
                    break
                else:
                    print("❌ Semua nilai harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = (atas + bawah) * tinggi * 0.5
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = ({atas} + {bawah}) × {tinggi} × 0.5 = {luas}")
        print(f"✅ HASIL LUAS TRAPESIUM = {luas:.2f} cm²")
    
    # ====================== 7. BELAH KETUPAT ======================
    elif pilihan == "7":
        print("\n7) BELAH KETUPAT (Luas)")
        print("Rumus: Luas = diagonal1 × diagonal2 × 0.5")
        
        while True:
            try:
                d1 = float(input("Input diagonal 1 : "))
                d2 = float(input("Input diagonal 2 : "))
                if d1 >= 2 and d2 >= 2:
                    break
                else:
                    print("❌ Kedua diagonal harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = d1 * d2 * 0.5
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = {d1} × {d2} × 0.5 = {luas}")
        print(f"✅ HASIL LUAS BELAH KETUPAT = {luas:.2f} cm²")
    
    # ====================== 8. LAYANG-LAYANG ======================
    elif pilihan == "8":
        print("\n8) LAYANG-LAYANG (Luas)")
        print("Rumus: Luas = diagonal1 × diagonal2 × 0.5")
        
        while True:
            try:
                d1 = float(input("Input diagonal 1 : "))
                d2 = float(input("Input diagonal 2 : "))
                if d1 >= 2 and d2 >= 2:
                    break
                else:
                    print("❌ Kedua diagonal harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        luas = d1 * d2 * 0.5
        print("\nPROSES PERHITUNGAN:")
        print(f"Luas = {d1} × {d2} × 0.5 = {luas}")
        print(f"✅ HASIL LUAS LAYANG-LAYANG = {luas:.2f} cm²")
    
    # ====================== 9. KUBUS ======================
    elif pilihan == "9":
        print("\n9) KUBUS (Volume)")
        print("Rumus: Volume = sisi × sisi × sisi")
        
        while True:
            try:
                sisi = float(input("Input sisi : "))
                if sisi >= 2:
                    break
                else:
                    print("❌ Nilai sisi harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        volume = sisi ** 3
        print("\nPROSES PERHITUNGAN:")
        print(f"Volume = {sisi} × {sisi} × {sisi} = {volume}")
        print(f"✅ HASIL VOLUME KUBUS = {volume:.2f} cm³")
    
    # ====================== 10. BALOK ======================
    elif pilihan == "10":
        print("\n10) BALOK (Volume)")
        print("Rumus: Volume = panjang × lebar × tinggi")
        
        while True:
            try:
                panjang = float(input("Input panjang : "))
                lebar = float(input("Input lebar   : "))
                tinggi = float(input("Input tinggi  : "))
                if panjang >= 2 and lebar >= 2 and tinggi >= 2:
                    break
                else:
                    print("❌ Semua nilai harus ≥ 2!")
            except ValueError:
                print("❌ Input harus berupa angka!")
        
        volume = panjang * lebar * tinggi
        print("\nPROSES PERHITUNGAN:")
        print(f"Volume = {panjang} × {lebar} × {tinggi} = {volume}")
        print(f"✅ HASIL VOLUME BALOK = {volume:.2f} cm³")
    
    else:
        print("❌ Pilihan tidak valid! Masukkan angka 0-10.")
    
    input("\nTekan Enter untuk kembali ke menu...")