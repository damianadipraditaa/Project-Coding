import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ====================== DATABASE ======================
conn = sqlite3.connect('pelanggaran_sekolah.db')
c = conn.cursor()

# Tabel siswa
c.execute('''CREATE TABLE IF NOT EXISTS siswa (
                nis TEXT PRIMARY KEY,
                nama TEXT,
                kelas TEXT)''')

# Tabel pelanggaran
c.execute('''CREATE TABLE IF NOT EXISTS pelanggaran (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nis TEXT,
                tanggal TEXT,
                jenis_pelanggaran TEXT,
                keterangan TEXT,
                poin INTEGER,
                petugas TEXT,
                FOREIGN KEY(nis) REFERENCES siswa(nis))''')

conn.commit()

# ====================== DATA AWAL (contoh siswa & jenis pelanggaran) ======================
siswa_contoh = [
    ("21001", "Ahmad Zaky", "X IPA 1"),
    ("21002", "Siti Nurhaliza", "X IPS 2"),
    ("21003", "Budi Santoso", "X IPA 3"),
    ("21004", "Dewi Lestari", "XI IPA 1"),
    ("21005", "Rian Nugraha", "XI IPS 2"),
]

for nis, nama, kelas in siswa_contoh:
    c.execute("INSERT OR IGNORE INTO siswa (nis, nama, kelas) VALUES (?, ?, ?)", (nis, nama, kelas))

jenis_pelanggaran = {
    "Terlambat masuk kelas": 5,
    "Tidak memakai seragam lengkap": 10,
    "Merokok di lingkungan sekolah": 50,
    "Berkelahi": 75,
    "Bolos (membolos)": 30,
    "Menggunakan HP saat pelajaran": 15,
    "Berpakaian tidak sopan": 20,
    "Membawa/menggunakan senjata tajam": 100,
    "Vandalisme (merusak fasilitas)": 40,
    "Tidak mengerjakan PR/tugas": 10,
    "Lain-lain": 0   # akan diminta input poin manual
}

conn.commit()

# ====================== APLIKASI GUI ======================
class PelanggaranApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencatatan Pelanggaran Siswa")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f5f6fa")

        self.create_widgets()

    def create_widgets(self):
        # JUDUL
        tk.Label(self.root, text="📋 CATAT PELANGGARAN SISWA", font=("Arial", 20, "bold"), bg="#f5f6fa", fg="#2c3e50").pack(pady=15)

        # Frame Input Pelanggaran
        frame_input = tk.LabelFrame(self.root, text="Input Pelanggaran Baru", bg="#ffffff", padx=15, pady=10)
        frame_input.pack(fill="x", padx=25, pady=10)

        # Pilih siswa
        tk.Label(frame_input, text="Nama Siswa:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.nama_combo = ttk.Combobox(frame_input, width=35, state="readonly")
        self.nama_combo.grid(row=0, column=1, pady=5, padx=10, sticky="w")
        self.update_daftar_siswa()

        # Jenis pelanggaran
        tk.Label(frame_input, text="Jenis Pelanggaran:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.jenis_combo = ttk.Combobox(frame_input, width=35, values=list(jenis_pelanggaran.keys()), state="readonly")
        self.jenis_combo.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        self.jenis_combo.bind("<<ComboboxSelected>>", self.update_poin_otomatis)

        # Poin
        tk.Label(frame_input, text="Poin Sanksi:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.poin_entry = tk.Entry(frame_input, width=10)
        self.poin_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")

        # Keterangan
        tk.Label(frame_input, text="Keterangan:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
        self.ket_entry = tk.Entry(frame_input, width=60)
        self.ket_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

        # Petugas
        tk.Label(frame_input, text="Petugas:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
        self.petugas_entry = tk.Entry(frame_input, width=35)
        self.petugas_entry.grid(row=4, column=1, pady=5, padx=10, sticky="w")
        self.petugas_entry.insert(0, "BK / Wali Kelas")

        # Tombol Simpan
        tk.Button(frame_input, text="SIMPAN PELANGGARAN", font=("Arial", 11, "bold"),
                  bg="#e74c3c", fg="white", command=self.simpan_pelanggaran).grid(row=5, column=0, columnspan=2, pady=15)

        # Frame Riwayat & Pencarian
        frame_riwayat = tk.LabelFrame(self.root, text="Riwayat Pelanggaran", bg="#ffffff", padx=15, pady=10)
        frame_riwayat.pack(fill="both", expand=True, padx=25, pady=10)

        # Pencarian
        tk.Label(frame_riwayat, text="Cari Nama:", bg="white").pack(side="left", padx=5)
        self.cari_entry = tk.Entry(frame_riwayat, width=30)
        self.cari_entry.pack(side="left", padx=5)
        tk.Button(frame_riwayat, text="Cari", bg="#3498db", fg="white", command=self.cari_riwayat).pack(side="left", padx=5)
        tk.Button(frame_riwayat, text="Tampil Semua", bg="#7f8c8d", fg="white", command=self.tampil_semua).pack(side="left", padx=5)

        # Treeview Riwayat
        self.tree = ttk.Treeview(frame_riwayat, columns=("Tanggal", "NIS", "Nama", "Kelas", "Pelanggaran", "Keterangan", "Poin", "Petugas"), show="headings", height=12)
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.heading("NIS", text="NIS")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Kelas", text="Kelas")
        self.tree.heading("Pelanggaran", text="Pelanggaran")
        self.tree.heading("Keterangan", text="Keterangan")
        self.tree.heading("Poin", text="Poin")
        self.tree.heading("Petugas", text="Petugas")

        cols_width = [110, 70, 140, 80, 160, 220, 50, 110]
        for col, w in zip(self.tree["columns"], cols_width):
            self.tree.column(col, width=w, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=10)

        # Total poin
        self.total_label = tk.Label(frame_riwayat, text="Total poin siswa ini: 0", font=("Arial", 11, "bold"), bg="white", fg="#c0392b")
        self.total_label.pack(pady=5)

        # Refresh awal
        self.tampil_semua()

    def update_daftar_siswa(self):
        c.execute("SELECT nis, nama, kelas FROM siswa ORDER BY nama")
        self.siswa_data = c.fetchall()
        nama_list = [f"{nama} ({kelas})" for _, nama, kelas in self.siswa_data]
        self.nama_combo['values'] = nama_list

    def update_poin_otomatis(self, event=None):
        jenis = self.jenis_combo.get()
        if jenis in jenis_pelanggaran:
            poin = jenis_pelanggaran[jenis]
            self.poin_entry.delete(0, tk.END)
            self.poin_entry.insert(0, str(poin))

    def simpan_pelanggaran(self):
        nama_full = self.nama_combo.get()
        if not nama_full:
            messagebox.showwarning("Peringatan", "Pilih siswa terlebih dahulu!")
            return

        try:
            nis = self.siswa_data[self.nama_combo.current()][0]
        except:
            messagebox.showerror("Error", "Data siswa tidak valid")
            return

        jenis = self.jenis_combo.get()
        if not jenis:
            messagebox.showwarning("Peringatan", "Pilih jenis pelanggaran!")
            return

        try:
            poin = int(self.poin_entry.get())
        except:
            messagebox.showwarning("Peringatan", "Poin harus berupa angka!")
            return

        keterangan = self.ket_entry.get().strip()
        petugas = self.petugas_entry.get().strip()

        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")

        c.execute("""
            INSERT INTO pelanggaran (nis, tanggal, jenis_pelanggaran, keterangan, poin, petugas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nis, tanggal, jenis, keterangan, poin, petugas))

        conn.commit()
        messagebox.showinfo("Sukses", "Pelanggaran berhasil dicatat!")

        # Kosongkan form
        self.jenis_combo.set("")
        self.poin_entry.delete(0, tk.END)
        self.ket_entry.delete(0, tk.END)

        self.tampil_semua()

    def tampil_semua(self):
        self.cari_entry.delete(0, tk.END)
        self._tampil_riwayat("")

    def cari_riwayat(self):
        keyword = self.cari_entry.get().strip().lower()
        self._tampil_riwayat(keyword)

    def _tampil_riwayat(self, keyword):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = """
            SELECT p.tanggal, s.nis, s.nama, s.kelas, p.jenis_pelanggaran, p.keterangan, p.poin, p.petugas
            FROM pelanggaran p
            JOIN siswa s ON p.nis = s.nis
        """
        params = ()

        if keyword:
            query += " WHERE LOWER(s.nama) LIKE ?"
            params = (f"%{keyword}%",)

        query += " ORDER BY p.tanggal DESC"

        c.execute(query, params)
        rows = c.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        # Hitung total poin jika ada pencarian spesifik
        if keyword and rows:
            total = sum(row[6] for row in rows)
            self.total_label.config(text=f"Total poin siswa ini: {total}")
        else:
            self.total_label.config(text="Total poin siswa ini: -")

# ====================== JALANKAN ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = PelanggaranApp(root)
    root.mainloop()