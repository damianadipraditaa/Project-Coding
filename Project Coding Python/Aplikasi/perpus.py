import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

# ====================== DATABASE ======================
conn = sqlite3.connect('perpustakaan_sekolah.db')
c = conn.cursor()

# Tabel buku
c.execute('''CREATE TABLE IF NOT EXISTS buku (
                kode TEXT PRIMARY KEY,
                judul TEXT,
                pengarang TEXT,
                tahun INTEGER,
                status TEXT DEFAULT 'Tersedia')''')

# Tabel siswa
c.execute('''CREATE TABLE IF NOT EXISTS siswa (
                nis TEXT PRIMARY KEY,
                nama TEXT,
                kelas TEXT)''')

# Tabel peminjaman
c.execute('''CREATE TABLE IF NOT EXISTS peminjaman (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode_buku TEXT,
                judul_buku TEXT,
                nis_siswa TEXT,
                nama_siswa TEXT,
                tanggal_pinjam TEXT,
                tanggal_kembali TEXT,
                tanggal_aktual_kembali TEXT,
                status TEXT DEFAULT 'Dipinjam',
                terlambat INTEGER DEFAULT 0,
                FOREIGN KEY(kode_buku) REFERENCES buku(kode),
                FOREIGN KEY(nis_siswa) REFERENCES siswa(nis))''')

# Tabel blacklist
c.execute('''CREATE TABLE IF NOT EXISTS blacklist (
                nis TEXT PRIMARY KEY,
                nama TEXT,
                kelas TEXT,
                tanggal_blacklist TEXT,
                jumlah_terlambat INTEGER,
                alasan TEXT)''')

conn.commit()

# ====================== DATA CONTOH (jalankan sekali saja) ======================
buku_contoh = [
    ("B001", "Laskar Pelangi", "Andrea Hirata", 2005),
    ("B002", "Bumi Manusia", "Pramoedya Ananta Toer", 1980),
    ("B003", "Dilan 1990", "Pidi Baiq", 2014),
]

for kode, judul, pengarang, tahun in buku_contoh:
    c.execute("INSERT OR IGNORE INTO buku (kode, judul, pengarang, tahun) VALUES (?, ?, ?, ?)", 
              (kode, judul, pengarang, tahun))

siswa_contoh = [
    ("21001", "Ahmad Zaky", "X IPA 1"),
    ("21002", "Siti Nurhaliza", "X IPS 2"),
    ("21003", "Budi Santoso", "XI IPA 3"),
]

for nis, nama, kelas in siswa_contoh:
    c.execute("INSERT OR IGNORE INTO siswa (nis, nama, kelas) VALUES (?, ?, ?)", (nis, nama, kelas))

conn.commit()

# ====================== APLIKASI GUI ======================
class PerpustakaanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Perpustakaan Sekolah - Solution App")
        self.root.geometry("1150x750")
        self.root.configure(bg="#f0f9ff")

        self.BATAS_TERLAMBAT_BLACKLIST = 3
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="📚 SISTEM PERPUSTAKAAN SEKOLAH", 
                 font=("Arial", 20, "bold"), bg="#f0f9ff", fg="#1e40af").pack(pady=15)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_buku = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_buku, text="Daftar Buku")
        self.buat_tab_daftar_buku()

        self.tab_pinjam = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_pinjam, text="Pinjam Buku")
        self.buat_tab_pinjam()

        self.tab_kembali = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_kembali, text="Pengembalian")
        self.buat_tab_kembali()

        self.tab_riwayat = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_riwayat, text="Riwayat & Blacklist")
        self.buat_tab_riwayat()

    def buat_tab_daftar_buku(self):
        frame_atas = tk.Frame(self.tab_buku, bg="#f0f9ff")
        frame_atas.pack(fill="x", pady=10, padx=10)

        tk.Label(frame_atas, text="Cari Judul / Kode:", bg="#f0f9ff").pack(side="left", padx=5)
        self.cari_buku_entry = tk.Entry(frame_atas, width=35)
        self.cari_buku_entry.pack(side="left", padx=5)
        tk.Button(frame_atas, text="Cari", bg="#3b82f6", fg="white", command=self.cari_buku).pack(side="left", padx=5)

        tk.Button(frame_atas, text="+ Tambah Buku", bg="#10b981", fg="white", 
                  command=self.tambah_buku_window).pack(side="right", padx=10)

        self.tree_buku = ttk.Treeview(self.tab_buku, columns=("Kode", "Judul", "Pengarang", "Tahun", "Status"), show="headings")
        self.tree_buku.heading("Kode", text="Kode")
        self.tree_buku.heading("Judul", text="Judul")
        self.tree_buku.heading("Pengarang", text="Pengarang")
        self.tree_buku.heading("Tahun", text="Tahun")
        self.tree_buku.heading("Status", text="Status")

        widths = [80, 300, 200, 80, 120]
        for col, w in zip(self.tree_buku["columns"], widths):
            self.tree_buku.column(col, width=w, anchor="center" if col in ["Kode","Tahun","Status"] else "w")

        self.tree_buku.pack(fill="both", expand=True, padx=10, pady=10)
        self.refresh_daftar_buku()

    def refresh_daftar_buku(self, keyword=""):
        for item in self.tree_buku.get_children():
            self.tree_buku.delete(item)

        query = "SELECT kode, judul, pengarang, tahun, status FROM buku"
        params = ()
        if keyword:
            query += " WHERE judul LIKE ? OR kode LIKE ?"
            params = (f"%{keyword}%", f"%{keyword}%")

        c.execute(query, params)
        for row in c.fetchall():
            self.tree_buku.insert("", "end", values=row)

    def cari_buku(self):
        self.refresh_daftar_buku(self.cari_buku_entry.get().strip())

    def tambah_buku_window(self):
        win = tk.Toplevel(self.root)
        win.title("Tambah Buku Baru")
        win.geometry("500x400")
        win.configure(bg="#f0f9ff")

        labels = ["Kode Buku:", "Judul Buku:", "Pengarang:", "Tahun Terbit:"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(win, text=label, bg="#f0f9ff").pack(pady=8)
            ent = tk.Entry(win, width=40)
            ent.pack()
            entries.append(ent)

        def simpan():
            try:
                kode, judul, pengarang, tahun_str = [e.get().strip() for e in entries]
                tahun = int(tahun_str)
                if not all([kode, judul, pengarang]):
                    raise ValueError("Isi semua field!")
                c.execute("INSERT INTO buku (kode, judul, pengarang, tahun) VALUES (?, ?, ?, ?)", 
                          (kode.upper(), judul, pengarang, tahun))
                conn.commit()
                messagebox.showinfo("Sukses", "Buku ditambahkan!")
                win.destroy()
                self.refresh_daftar_buku()
            except ValueError as e:
                messagebox.showwarning("Error", str(e))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Kode buku sudah ada!")

        tk.Button(win, text="SIMPAN", bg="#10b981", fg="white", font=("Arial", 12, "bold"),
                  command=simpan).pack(pady=30)

    def buat_tab_pinjam(self):
        frame = tk.Frame(self.tab_pinjam, bg="#f0f9ff")
        frame.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(frame, text="Peminjaman Buku", font=("Arial", 16, "bold"), bg="#f0f9ff").pack(pady=10)

        self.label_warning_pinjam = tk.Label(frame, text="", fg="red", bg="#f0f9ff", font=("Arial", 11))
        self.label_warning_pinjam.pack(pady=5)

        tk.Label(frame, text="Pilih Siswa:", bg="#f0f9ff").pack(anchor="w")
        self.siswa_combo = ttk.Combobox(frame, width=50, state="readonly")
        self.siswa_combo.pack(pady=5, fill="x")
        self.siswa_combo.bind("<<ComboboxSelected>>", self.cek_blacklist_saat_pilih)
        self.update_combo_siswa()

        tk.Label(frame, text="Pilih Buku (Tersedia):", bg="#f0f9ff").pack(anchor="w", pady=15)
        self.buku_combo = ttk.Combobox(frame, width=50, state="readonly")
        self.buku_combo.pack(pady=5, fill="x")
        self.update_combo_buku()

        tk.Button(frame, text="PINJAM SEKARANG", bg="#ea580c", fg="white", font=("Arial", 13, "bold"),
                  command=self.proses_pinjam).pack(pady=40, ipadx=30, ipady=12)

    def cek_blacklist_saat_pilih(self, event):
        if not self.siswa_combo.get():
            self.label_warning_pinjam.config(text="")
            return
        idx = self.siswa_combo.current()
        nis = self.siswa_list[idx][0]
        if self.is_blacklisted(nis):
            nama = self.siswa_list[idx][1]
            self.label_warning_pinjam.config(text=f"!!! {nama} sedang BLACKLIST - tidak bisa pinjam !!!")
        else:
            self.label_warning_pinjam.config(text="")

    def is_blacklisted(self, nis):
        c.execute("SELECT nis FROM blacklist WHERE nis = ?", (nis,))
        return bool(c.fetchone())

    def update_combo_siswa(self):
        c.execute("SELECT nis, nama, kelas FROM siswa ORDER BY nama")
        self.siswa_list = c.fetchall()
        self.siswa_combo['values'] = [f"{nis} - {nama} ({kelas})" for nis, nama, kelas in self.siswa_list]

    def update_combo_buku(self):
        c.execute("SELECT kode, judul FROM buku WHERE status = 'Tersedia' ORDER BY judul")
        self.buku_list = c.fetchall()
        self.buku_combo['values'] = [f"{kode} - {judul}" for kode, judul in self.buku_list]

    def proses_pinjam(self):
        if not self.siswa_combo.get() or not self.buku_combo.get():
            messagebox.showwarning("Peringatan", "Pilih siswa dan buku terlebih dahulu!")
            return

        idx_s = self.siswa_combo.current()
        nis, nama_s, kelas = self.siswa_list[idx_s]

        if self.is_blacklisted(nis):
            messagebox.showerror("DITOLAK", f"{nama_s} sedang BLACKLIST!\nSudah terlambat ≥ {self.BATAS_TERLAMBAT_BLACKLIST} kali.")
            return

        idx_b = self.buku_combo.current()
        kode, judul = self.buku_list[idx_b]

        t_pinjam = datetime.now().strftime("%Y-%m-%d")
        t_kembali = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        try:
            c.execute("UPDATE buku SET status = 'Dipinjam' WHERE kode = ?", (kode,))
            c.execute("""
                INSERT INTO peminjaman 
                (kode_buku, judul_buku, nis_siswa, nama_siswa, tanggal_pinjam, tanggal_kembali)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (kode, judul, nis, nama_s, t_pinjam, t_kembali))
            conn.commit()
            messagebox.showinfo("Sukses", f"Peminjaman berhasil!\n\n{judul}\nOleh: {nama_s}\nKembali paling lambat: {t_kembali}")
            self.update_combo_buku()
            self.refresh_riwayat()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal meminjam: {str(e)}")

    # (lanjutan kode untuk tab Pengembalian dan Riwayat bisa disalin dari versi sebelumnya)
    # Jika masih error di bagian tertentu, beri tahu pesan error lengkapnya ya

    def buat_tab_kembali(self):
        # ... (kode proses_kembali, catat_keterlambatan, dll dari versi sebelumnya)
        pass  # ganti dengan kode asli + perbaikan jika perlu

    def buat_tab_riwayat(self):
        # ... (kode treeview riwayat + blacklist dari versi sebelumnya)
        pass

    def refresh_riwayat(self):
        # ... 
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PerpustakaanApp(root)
    root.mainloop()