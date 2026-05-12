# contoh ke 1

sekolah = "Tidak Belajar dan mengerjakan tugas"
if sekolah == "Belajar dan mengerjakan tugas":
    print("Selamat kamu lulus dari SMK")
else:
    print("Coba lagi tahun depan yaaa")
    
    
    
# contoh ke 2

penjara = "Tidak berbuat mencuri uang di bank"
if penjara == "Berbuat mencuri uang di bank":
    print("Selamat kamu bebas dari penjara")
else:
    print("Coba di lain waktu yaaa")
    
    
 
 
 # contoh ke 3
 
hari_ini = "kadhefiwehiwhg"   
 
if(hari_ini == "senin"):
    print("saya akan ke dokter")
elif(hari_ini == "Selasa"):
    print("saya akan ke dokter")
elif(hari_ini == "Rabu"):
    print("saya akan ke dokter")
elif(hari_ini == "Kamis"):
    print("saya akan ke dokter")
elif(hari_ini == "Jum'at"):
    print("saya akan ke dokter")
elif(hari_ini == "Sabtu"):
    print("saya akan ke dokter")
elif(hari_ini == "Minggu"):
    print("saya akan ke dokter")
else:
    print("hari salah")
    
    
# contoh ke 4
hari_ini = "Manggo"

if(hari_ini == "Senin"):
    print("saya akan pergi ke cafe")
elif(hari_ini == "Selasa"):
    print("saya akan pergi ke cafe")
elif(hari_ini == "Rabu"):
    print("saya akan pergi ke cafe")
elif(hari_ini == "Kamis"):
    print("saya akan pergi ke cafe")
elif(hari_ini == "Jum'at"):
    print("saya akan pergi ke cafe")
elif(hari_ini == "Sabtu"):
    print("saya akan pergi ke cafe")
elif(hari_ini == "Minggu"):
    print("saya akan pergi ke cafe")
else:
    print("Hari yang anda masukkan kurang tepat")
    
# contoh ke 5

hari_ini = " woejwo3j"

match hari_ini:
    case "Senin" | "Selasa" | "Rabu" | "Kamis" | "Jum'at" | "Sabtu" | "Minggu":
        print("Saya akan pergi ke mall untuk berbelanja")
    case "Rabu":
        print("Saya akan pergi les musik")
    case "Kamis":
        print("Saya akan pergi berenang")
    case _:
        print("Hari yang kurang memungkinkan")
