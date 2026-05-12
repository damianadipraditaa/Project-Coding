import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ====================== DATABASE ======================
conn = sqlite3.connect('absensi_sekolah.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS siswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nis TEXT UNIQUE,
                nama TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS absensi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                mapel TEXT,
                nis TEXT,
                nama TEXT,
                status TEXT,
                keterangan TEXT)''')   # Kolom baru untuk Alfa/Izin/Sakit/Dispen

conn.commit()

# ====================== DATA SISWA CONTOH ======================
siswa_list = [
    ("12345", "Ahmad Fauzi"),
    ("12346", "Siti Aisyah"),
    ("12347", "Budi Santoso"),
    ("12348", "Dewi Lestari"),
    ("12349", "Eko Prasetyo"),
    ("12350", "Fina Nurhaliza"),
    ("12351", "Guntur Rahardjo"),
    ("12352", "Hana Melati")
]

for nis, nama in siswa_list:
    c.execute("INSERT OR IGNORE INTO siswa (nis, nama) VALUES (?, ?)", (nis, nama))
conn.commit()

# ====================== GUI APLIKASI ======================
class AbsensiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Absensi Siswa per Mata Pelajaran - Solution App")
        self.root.geometry("1000x680")
        self.root.configure(bg="#f0f4f8")

        self.mapel_var = tk.StringVar(value="Pilih Mata Pelajaran")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="📅 ABSENSI SISWA PER MATA PELAJARAN", 
                 font=("Arial", 20, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=20)

        # Pilih Mata Pelajaran
        frame_mapel = tk.Frame(self.root, bg="#f0f4f8")
        frame_mapel.pack(pady=10)

        tk.Label(frame_mapel, text="Mata Pelajaran:", font=("Arial", 12), bg="#f0f4f8").pack(side="left", padx=10)
        self.mapel_combo = ttk.Combobox(frame_mapel, textvariable=self.mapel_var, state="readonly", width=35,
                                        values=["Matematika", "Bahasa Indonesia", "Bahasa Inggris", "IPA", "IPS", 
                                                "Pendidikan Agama", "Olahraga", "Seni Budaya", "PKN", "Informatika"])
        self.mapel_combo.pack(side="left", padx=10)

        tk.Button(frame_mapel, text="Mulai Absensi", font=("Arial", 11, "bold"), bg="#27ae60", fg="white",
                  command=self.mulai_absensi).pack(side="left", padx=25)

        # Frame untuk daftar siswa
        self.frame_siswa = tk.Frame(self.root, bg="white", bd=2, relief="solid")
        self.frame_siswa.pack(pady=20, fill="both", expand=True, padx=40)

        # Tombol bawah
        btn_frame = tk.Frame(self.root, bg="#f0f4f8")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="📋 Lihat Riwayat Absensi", font=("Arial", 11), bg="#3498db", fg="white",
                  command=self.lihat_riwayat).pack(side="left", padx=15)

        tk.Button(btn_frame, text="+ Tambah Siswa Baru", font=("Arial", 11), bg="#f39c12", fg="white",
                  command=self.tambah_siswa).pack(side="left", padx=15)

    def mulai_absensi(self):
        mapel = self.mapel_var.get()
        if mapel == "Pilih Mata Pelajaran":
            messagebox.showwarning("Peringatan", "Silakan pilih mata pelajaran terlebih dahulu!")
            return

        # Bersihkan frame sebelumnya
        for widget in self.frame_siswa.winfo_children():
            widget.destroy()

        # Judul absensi
        tk.Label(self.frame_siswa, text=f"Absensi {mapel} - {datetime.now().strftime('%d %B %Y %H:%M')}",
                 font=("Arial", 14, "bold"), bg="#34495e", fg="white", pady=12).pack(fill="x")

        # Header tabel
        header = tk.Frame(self.frame_siswa, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text="NIS", width=15, fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Label(header, text="Nama Siswa", width=40, fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Label(header, text="Status Kehadiran", width=25, fg="white", bg="#2c3e50", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Ambil data siswa
        c.execute("SELECT nis, nama FROM siswa ORDER BY nama")
        siswa = c.fetchall()

        self.absensi_data = []   # Untuk menyimpan data absensi

        for nis, nama in siswa:
            row = tk.Frame(self.frame_siswa, bg="white")
            row.pack(fill="x", pady=3, padx=5)

            tk.Label(row, text=nis, width=15, bg="white", anchor="w", font=("Arial", 10)).pack(side="left", padx=5)
            tk.Label(row, text=nama, width=40, bg="white", anchor="w", font=("Arial", 10)).pack(side="left", padx=5)

            # Combobox untuk status
            status_var = tk.StringVar(value="Hadir")
            combo = ttk.Combobox(row, textvariable=status_var, state="readonly", width=20,
                                 values=["Hadir", "Alfa", "Izin", "Sakit", "Dispen"])
            combo.pack(side="left", padx=20)

            self.absensi_data.append((nis, nama, status_var))

        # Tombol Simpan
        tk.Button(self.frame_siswa, text="💾 SIMPAN ABSENSI", font=("Arial", 13, "bold"),
                  bg="#27ae60", fg="white", height=2,
                  command=lambda: self.simpan_absensi(mapel)).pack(pady=25, fill="x", padx=40)

    def simpan_absensi(self, mapel):
        if not self.absensi_data:
            messagebox.showwarning("Error", "Tidak ada data absensi!")
            return

        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for nis, nama, status_var in self.absensi_data:
            status = status_var.get()
            keterangan = status if status != "Hadir" else None

            c.execute("""
                INSERT INTO absensi (tanggal, mapel, nis, nama, status, keterangan)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tanggal, mapel, nis, nama, status, keterangan))

        conn.commit()
        messagebox.showinfo("Sukses", f"Absensi {mapel} berhasil disimpan!\nTanggal: {tanggal}")
        
        # Refresh tampilan absensi
        self.mulai_absensi()

    def lihat_riwayat(self):
        RiwayatWindow(self.root)

    def tambah_siswa(self):
        TambahSiswaWindow(self.root, self)


class RiwayatWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Riwayat Absensi Lengkap")
        self.top.geometry("950x600")

        tk.Label(self.top, text="RIWAYAT ABSENSI SEMUA MATA PELAJARAN", 
                 font=("Arial", 16, "bold")).pack(pady=10)

        tree = ttk.Treeview(self.top, columns=("Tanggal", "Mapel", "NIS", "Nama", "Status", "Keterangan"), show="headings")
        tree.heading("Tanggal", text="Tanggal & Waktu")
        tree.heading("Mapel", text="Mata Pelajaran")
        tree.heading("NIS", text="NIS")
        tree.heading("Nama", text="Nama Siswa")
        tree.heading("Status", text="Status")
        tree.heading("Keterangan", text="Keterangan")

        tree.column("Tanggal", width=160)
        tree.column("Mapel", width=140)
        tree.column("NIS", width=80)
        tree.column("Nama", width=180)
        tree.column("Status", width=100)
        tree.column("Keterangan", width=150)

        tree.pack(fill="both", expand=True, padx=20, pady=10)

        c.execute("""
            SELECT tanggal, mapel, nis, nama, status, keterangan 
            FROM absensi ORDER BY tanggal DESC
        """)
        for row in c.fetchall():
            tree.insert("", "end", values=row)


class TambahSiswaWindow:
    def __init__(self, parent, app):
        self.top = tk.Toplevel(parent)
        self.top.title("Tambah Siswa Baru")
        self.top.geometry("420x280")
        self.app = app

        tk.Label(self.top, text="NIS", font=("Arial", 12)).pack(pady=10)
        self.nis_entry = tk.Entry(self.top, font=("Arial", 12), width=35)
        self.nis_entry.pack()

        tk.Label(self.top, text="Nama Lengkap", font=("Arial", 12)).pack(pady=10)
        self.nama_entry = tk.Entry(self.top, font=("Arial", 12), width=35)
        self.nama_entry.pack()

        tk.Button(self.top, text="Tambahkan Siswa", font=("Arial", 12, "bold"), bg="#27ae60", fg="white",
                  command=self.tambah).pack(pady=30)

    def tambah(self):
        nis = self.nis_entry.get().strip()
        nama = self.nama_entry.get().strip()

        if nis and nama:
            try:
                c.execute("INSERT INTO siswa (nis, nama) VALUES (?, ?)", (nis, nama))
                conn.commit()
                messagebox.showinfo("Sukses", "Siswa berhasil ditambahkan!")
                self.top.destroy()
                # Refresh jika sedang di halaman absensi (opsional)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "NIS sudah terdaftar!")
        else:
            messagebox.showwarning("Error", "NIS dan Nama tidak boleh kosong!")


# ====================== JALANKAN APLIKASI ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = AbsensiApp(root)
    root.mainloop()