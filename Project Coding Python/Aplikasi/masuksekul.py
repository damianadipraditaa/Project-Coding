import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, time

# ====================== KONFIGURASI ======================
JAM_MASUK = time(7, 0)       # 07:00 = tepat waktu
TERLAMBAT = time(7, 31)      # mulai 07:31 = terlambat

BATAS_BLACKLIST = 3          # jumlah pelanggaran keterlambatan untuk blacklist

# ====================== DATABASE ======================
conn = sqlite3.connect('absensi_masuk_sekolah.db')
c = conn.cursor()

# Tabel siswa
c.execute('''CREATE TABLE IF NOT EXISTS siswa (
                nis TEXT PRIMARY KEY,
                nama TEXT,
                kelas TEXT)''')

# Tabel kedatangan (absensi harian)
c.execute('''CREATE TABLE IF NOT EXISTS kedatangan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nis TEXT,
                nama TEXT,
                kelas TEXT,
                tanggal TEXT,
                jam_masuk TEXT,
                status TEXT,
                FOREIGN KEY(nis) REFERENCES siswa(nis))''')

# Tabel blacklist
c.execute('''CREATE TABLE IF NOT EXISTS blacklist (
                nis TEXT PRIMARY KEY,
                nama TEXT,
                kelas TEXT,
                tanggal_blacklist TEXT,
                jumlah_pelanggaran INTEGER,
                alasan TEXT,
                FOREIGN KEY(nis) REFERENCES siswa(nis))''')

# Tabel pelanggaran (riwayat detail)
c.execute('''CREATE TABLE IF NOT EXISTS pelanggaran (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nis TEXT,
                nama TEXT,
                kelas TEXT,
                tanggal TEXT,
                jenis TEXT,              -- misal: 'Terlambat', 'Seragam Tidak Lengkap', dll
                keterangan TEXT,
                FOREIGN KEY(nis) REFERENCES siswa(nis))''')

conn.commit()

# ====================== DATA SISWA CONTOH ======================
siswa_contoh = [
    ("21001", "Ahmad Zaky", "X IPA 1"),
    ("21002", "Siti Nurhaliza", "X IPS 2"),
    ("21003", "Budi Santoso", "X IPA 3"),
    ("21004", "Dewi Lestari", "XI IPA 1"),
    ("21005", "Rian Nugraha", "XI IPS 2"),
    ("21006", "Fajar Pratama", "XII IPA 1"),
    ("21007", "Nadia Putri", "XII IPS 3"),
]

for nis, nama, kelas in siswa_contoh:
    c.execute("INSERT OR IGNORE INTO siswa (nis, nama, kelas) VALUES (?, ?, ?)", (nis, nama, kelas))
conn.commit()

# ====================== APLIKASI GUI ======================
class AbsensiMasukApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Absensi & Pelanggaran Siswa - Solution App")
        self.root.geometry("1000x680")
        self.root.configure(bg="#e8f4f8")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="ABSENSI MASUK & PELANGGARAN SISWA", font=("Arial", 24, "bold"), bg="#e8f4f8", fg="#1e40af").pack(pady=15)

        frame_input = tk.LabelFrame(self.root, text="Input Kedatangan Siswa", bg="#ffffff", padx=25, pady=20)
        frame_input.pack(fill="x", padx=50, pady=10)

        tk.Label(frame_input, text="NIS atau Nama:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        self.cari_entry = tk.Entry(frame_input, font=("Arial", 13), width=38)
        self.cari_entry.grid(row=0, column=1, padx=12, pady=10, sticky="w")
        self.cari_entry.focus()

        tk.Label(frame_input, text="atau pilih:", font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.nama_combo = ttk.Combobox(frame_input, width=45, state="readonly", font=("Arial", 11))
        self.nama_combo.grid(row=1, column=1, padx=12, pady=10, sticky="w")
        self.update_daftar_siswa()

        tk.Button(frame_input, text="ABSEN SEKARANG", font=("Arial", 14, "bold"),
                  bg="#10b981", fg="white", width=25, height=2,
                  command=self.proses_absen).grid(row=2, column=0, columnspan=2, pady=25)

        frame_bottom = tk.Frame(self.root, bg="#e8f4f8")
        frame_bottom.pack(fill="both", expand=True, padx=50, pady=10)

        frame_riwayat = tk.LabelFrame(frame_bottom, text=f"Riwayat Kedatangan Hari Ini - {datetime.now().strftime('%d %B %Y')}", bg="#ffffff", padx=20, pady=15)
        frame_riwayat.pack(side="left", fill="both", expand=True)

        self.tree = ttk.Treeview(frame_riwayat, columns=("Jam", "NIS", "Nama", "Kelas", "Status"), show="headings", height=18)
        self.tree.heading("Jam", text="Jam Masuk")
        self.tree.heading("NIS", text="NIS")
        self.tree.heading("Nama", text="Nama Siswa")
        self.tree.heading("Kelas", text="Kelas")
        self.tree.heading("Status", text="Status")

        cols_width = [100, 90, 200, 110, 160]
        for col, w in zip(self.tree["columns"], cols_width):
            self.tree.column(col, width=w, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Tombol kanan
        frame_btn = tk.Frame(frame_bottom, bg="#e8f4f8")
        frame_btn.pack(side="right", padx=20, pady=10, fill="y")

        tk.Button(frame_btn, text="KELOLA BLACKLIST", font=("Arial", 12, "bold"),
                  bg="#ef4444", fg="white", width=18, height=2,
                  command=self.buka_window_blacklist).pack(pady=8)

        tk.Button(frame_btn, text="LIHAT SEMUA PELANGGARAN", font=("Arial", 11, "bold"),
                  bg="#d97706", fg="white", width=18, height=2,
                  command=self.buka_window_pelanggaran).pack(pady=8)

        self.cari_entry.bind("<Return>", lambda e: self.proses_absen())
        self.refresh_riwayat()

    def update_daftar_siswa(self):
        c.execute("SELECT nis, nama, kelas FROM siswa ORDER BY nama")
        self.siswa_list = c.fetchall()
        values = [f"{nama} - {kelas} ({nis})" for _, nama, kelas, nis in [(s[0], s[1], s[2], s[0]) for s in self.siswa_list]]
        self.nama_combo['values'] = values

    def siswa_sudah_blacklist(self, nis):
        c.execute("SELECT nis FROM blacklist WHERE nis = ?", (nis,))
        return c.fetchone() is not None

    def hitung_jumlah_pelanggaran(self, nis):
        c.execute("SELECT COUNT(*) FROM pelanggaran WHERE nis = ?", (nis,))
        return c.fetchone()[0]

    def catat_pelanggaran(self, nis, nama, kelas, jenis, keterangan=""):
        hari_ini = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("""
            INSERT INTO pelanggaran (nis, nama, kelas, tanggal, jenis, keterangan)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nis, nama, kelas, hari_ini, jenis, keterangan))
        conn.commit()

    def proses_absen(self):
        nis = nama = kelas = None

        input_text = self.cari_entry.get().strip()
        if input_text:
            c.execute("SELECT nis, nama, kelas FROM siswa WHERE nis = ?", (input_text,))
            row = c.fetchone()
            if row:
                nis, nama, kelas = row
            else:
                c.execute("SELECT nis, nama, kelas FROM siswa WHERE nama LIKE ?", (f"%{input_text}%",))
                row = c.fetchone()
                if row:
                    nis, nama, kelas = row

        if not nis:
            combo_val = self.nama_combo.get()
            if combo_val:
                for s in self.siswa_list:
                    if combo_val.startswith(f"{s[1]} - {s[2]}"):
                        nis, nama, kelas = s
                        break

        if not nis:
            messagebox.showwarning("Peringatan", "Siswa tidak ditemukan!")
            self.cari_entry.focus()
            return

        if self.siswa_sudah_blacklist(nis):
            messagebox.showerror("DITOLAK", f"{nama} ({kelas})\n\nStatus: BLACKLIST\nSudah melanggar ≥ {BATAS_BLACKLIST} kali!")
            self.cari_entry.delete(0, tk.END)
            return

        hari_ini = datetime.now().strftime("%Y-%m-%d")
        c.execute("SELECT id FROM kedatangan WHERE nis = ? AND tanggal = ?", (nis, hari_ini))
        if c.fetchone():
            messagebox.showinfo("Info", f"{nama} sudah absen hari ini.")
            self.cari_entry.delete(0, tk.END)
            return

        sekarang = datetime.now()
        jam = sekarang.time()
        status = "Tepat Waktu"
        if jam >= TERLAMBAT:
            status = "Terlambat"
        elif jam > JAM_MASUK:
            status = "Terlambat Sedikit"

        tanggal = sekarang.strftime("%Y-%m-%d")
        jam_masuk = sekarang.strftime("%H:%M:%S")

        c.execute("""
            INSERT INTO kedatangan (nis, nama, kelas, tanggal, jam_masuk, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nis, nama, kelas, tanggal, jam_masuk, status))
        conn.commit()

        # Catat pelanggaran jika terlambat
        if status in ("Terlambat", "Terlambat Sedikit"):
            self.catat_pelanggaran(nis, nama, kelas, "Keterlambatan", f"Masuk jam {jam_masuk}")
            jumlah_pelanggaran = self.hitung_jumlah_pelanggaran(nis)

            if jumlah_pelanggaran >= BATAS_BLACKLIST:
                hari_ini_full = datetime.now().strftime("%Y-%m-%d %H:%M")
                c.execute("""
                    INSERT OR REPLACE INTO blacklist 
                    (nis, nama, kelas, tanggal_blacklist, jumlah_pelanggaran, alasan)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nis, nama, kelas, hari_ini_full, jumlah_pelanggaran, f"Terlambat {jumlah_pelanggaran} kali"))
                conn.commit()
                messagebox.showwarning("BLACKLIST!", f"{nama} masuk BLACKLIST!\nTotal pelanggaran: {jumlah_pelanggaran}")
            else:
                messagebox.showinfo("Sukses", f"Absen OK\n\n{nama} ({kelas})\nJam: {jam_masuk}\nStatus: {status}\nPelanggaran ke-{jumlah_pelanggaran}")
        else:
            messagebox.showinfo("Sukses", f"Absen berhasil!\n\n{nama} ({kelas})\nJam: {jam_masuk}\nStatus: {status}")

        self.cari_entry.delete(0, tk.END)
        self.nama_combo.set("")
        self.refresh_riwayat()

    def refresh_riwayat(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        hari_ini = datetime.now().strftime("%Y-%m-%d")
        c.execute("SELECT jam_masuk, nis, nama, kelas, status FROM kedatangan WHERE tanggal = ? ORDER BY jam_masuk DESC", (hari_ini,))
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)

    def buka_window_blacklist(self):
        win = tk.Toplevel(self.root)
        win.title("Kelola Blacklist")
        win.geometry("900x550")
        win.configure(bg="#fef2f2")

        tk.Label(win, text="DAFTAR SISWA BLACKLIST", font=("Arial", 18, "bold"), bg="#fef2f2", fg="#991b1b").pack(pady=15)

        tree = ttk.Treeview(win, columns=("NIS", "Nama", "Kelas", "Tgl Blacklist", "Jml Pelanggaran", "Alasan"), show="headings")
        tree.heading("NIS", text="NIS")
        tree.heading("Nama", text="Nama")
        tree.heading("Kelas", text="Kelas")
        tree.heading("Tgl Blacklist", text="Tgl Blacklist")
        tree.heading("Jml Pelanggaran", text="Jml Pelanggaran")
        tree.heading("Alasan", text="Alasan")

        widths = [80, 180, 100, 140, 110, 220]
        for col, w in zip(tree["columns"], widths):
            tree.column(col, width=w, anchor="center")

        tree.pack(fill="both", expand=True, padx=20, pady=10)

        c.execute("SELECT nis, nama, kelas, tanggal_blacklist, jumlah_pelanggaran, alasan FROM blacklist ORDER BY tanggal_blacklist DESC")
        for row in c.fetchall():
            tree.insert("", "end", values=row)

        def hapus_selected():
            selected = tree.selection()
            if not selected:
                return
            nis = tree.item(selected)["values"][0]
            nama = tree.item(selected)["values"][1]
            if messagebox.askyesno("Konfirmasi", f"Hapus {nama} dari blacklist?"):
                c.execute("DELETE FROM blacklist WHERE nis = ?", (nis,))
                conn.commit()
                tree.delete(selected)
                messagebox.showinfo("Sukses", f"{nama} dihapus dari blacklist.")

        tk.Button(win, text="HAPUS DARI BLACKLIST", font=("Arial", 12, "bold"), bg="#dc2626", fg="white", command=hapus_selected).pack(pady=15)

    def buka_window_pelanggaran(self):
        win = tk.Toplevel(self.root)
        win.title("Riwayat Semua Pelanggaran")
        win.geometry("950x600")
        win.configure(bg="#fffbeb")

        tk.Label(win, text="RIWAYAT PELANGGARAN SISWA", font=("Arial", 18, "bold"), bg="#fffbeb", fg="#92400e").pack(pady=15)

        tree = ttk.Treeview(win, columns=("Tgl", "NIS", "Nama", "Kelas", "Jenis", "Keterangan"), show="headings")
        tree.heading("Tgl", text="Tanggal & Waktu")
        tree.heading("NIS", text="NIS")
        tree.heading("Nama", text="Nama")
        tree.heading("Kelas", text="Kelas")
        tree.heading("Jenis", text="Jenis Pelanggaran")
        tree.heading("Keterangan", text="Keterangan")

        widths = [160, 80, 180, 100, 140, 240]
        for col, w in zip(tree["columns"], widths):
            tree.column(col, width=w, anchor="center")

        tree.pack(fill="both", expand=True, padx=20, pady=10)

        c.execute("SELECT tanggal, nis, nama, kelas, jenis, keterangan FROM pelanggaran ORDER BY tanggal DESC")
        for row in c.fetchall():
            tree.insert("", "end", values=row)

# ====================== JALANKAN APLIKASI ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = AbsensiMasukApp(root)
    root.mainloop()