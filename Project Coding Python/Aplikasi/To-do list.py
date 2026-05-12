import json
import os

# ====== DATA ======
tasks = []
player = {
    "level": 1,
    "exp": 0
}

FILE_NAME = "save_game.json"

# ====== FUNCTION ======
def save_game():
    data = {
        "tasks": tasks,
        "player": player
    }
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)
    print("💾 Game berhasil disimpan!")

def load_game():
    global tasks, player
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
            tasks = data["tasks"]
            player = data["player"]
        print("📂 Game berhasil dimuat!")
    else:
        print("❌ Tidak ada data game.")

def add_task():
    title = input("Masukkan nama tugas: ")
    tasks.append({
        "title": title,
        "done": False
    })
    print("✅ Tugas berhasil ditambahkan!")

def show_tasks():
    if not tasks:
        print("📭 Tidak ada tugas.")
        return
    print("\n📋 DAFTAR TUGAS:")
    for i, task in enumerate(tasks):
        status = "✔️" if task["done"] else "❌"
        print(f"{i+1}. {task['title']} [{status}]")

def complete_task():
    show_tasks()
    if not tasks:
        return
    try:
        choice = int(input("Pilih nomor tugas: ")) - 1
        if tasks[choice]["done"]:
            print("⚠️ Tugas sudah diselesaikan.")
        else:
            tasks[choice]["done"] = True
            gain_exp(10)
            print("🎉 Tugas selesai! +10 EXP")
    except:
        print("❌ Input tidak valid.")

def gain_exp(amount):
    player["exp"] += amount
    while player["exp"] >= 50:
        player["exp"] -= 50
        player["level"] += 1
        print(f"🔥 LEVEL UP! Sekarang level {player['level']}")

def delete_task():
    show_tasks()
    try:
        choice = int(input("Hapus nomor tugas: ")) - 1
        tasks.pop(choice)
        print("🗑️ Tugas dihapus.")
    except:
        print("❌ Gagal menghapus tugas.")

def show_status():
    print("\n🎮 STATUS PEMAIN")
    print(f"Level : {player['level']}")
    print(f"EXP   : {player['exp']}/50")

def menu():
    print("""
========================
🎮 TASK HERO 🎮
========================
1. Tambah Tugas
2. Lihat Tugas
3. Selesaikan Tugas
4. Hapus Tugas
5. Status Pemain
6. Simpan Game
7. Load Game
0. Keluar
========================
""")

# ====== MAIN LOOP ======
load_game()
while True:
    menu()
    pilih = input("Pilih menu: ")

    if pilih == "1":
        add_task()
    elif pilih == "2":
        show_tasks()
    elif pilih == "3":
        complete_task()
    elif pilih == "4":
        delete_task()
    elif pilih == "5":
        show_status()
    elif pilih == "6":
        save_game()
    elif pilih == "7":
        load_game()
    elif pilih == "0":
        save_game()
        print("👋 Terima kasih sudah bermain!")
        break
    else:
        print("❌ Menu tidak tersedia.")
        save_game()
        print("👋 Terima kasih sudah bermain!")