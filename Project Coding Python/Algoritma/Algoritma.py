import pygame
import sys
import math

# Inisialisasi dengan error handling
try:
    pygame.init()
except Exception as e:
    print("Error saat inisialisasi Pygame:", e)
    sys.exit()

# ==================== SETTING ====================
WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bangun Ruang - Damian Adipradita D")
clock = pygame.time.Clock()

# Font yang lebih aman (menggunakan fallback)
title_font = pygame.font.SysFont("comicsansms", 42, bold=True)
big_font = pygame.font.SysFont("comicsansms", 28, bold=True)
font = pygame.font.SysFont("comicsansms", 24)
small_font = pygame.font.SysFont("comicsansms", 20)

if not title_font:
    title_font = pygame.font.Font(None, 42)
    big_font = pygame.font.Font(None, 28)
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 20)

# Warna
BG = (15, 23, 42)
ACCENT = (100, 200, 255)
PURPLE = (147, 51, 234)
GREEN = (34, 211, 151)
RED = (239, 68, 68)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
DARK = (30, 41, 59)

# State Aplikasi
current_mode = "menu"
selected_shape = None
inputs = {}
result = ""
error_msg = ""
active_input = None

# Data Bangun Ruang
shapes = {
    1: {"name": "Segitiga", "type": "Luas", "formula": "½ × alas × tinggi"},
    2: {"name": "Persegi", "type": "Luas", "formula": "sisi × sisi"},
    3: {"name": "Persegi Panjang", "type": "Luas", "formula": "panjang × lebar"},
    4: {"name": "Lingkaran", "type": "Luas", "formula": "π × r²"},
    5: {"name": "Jajar Genjang", "type": "Luas", "formula": "alas × tinggi"},
    6: {"name": "Trapesium", "type": "Luas", "formula": "½ × (atas + bawah) × tinggi"},
    7: {"name": "Belah Ketupat", "type": "Luas", "formula": "½ × d1 × d2"},
    8: {"name": "Layang-layang", "type": "Luas", "formula": "½ × d1 × d2"},
    9: {"name": "Kubus", "type": "Volume", "formula": "sisi³"},
    10: {"name": "Balok", "type": "Volume", "formula": "panjang × lebar × tinggi"}
}

input_config = {
    1: ["alas", "tinggi"], 2: ["sisi"], 3: ["panjang", "lebar"],
    4: ["radius"], 5: ["alas", "tinggi"], 6: ["atas", "bawah", "tinggi"],
    7: ["d1", "d2"], 8: ["d1", "d2"], 9: ["sisi"], 10: ["panjang", "lebar", "tinggi"]
}

label_names = {
    "alas": "Alas", "tinggi": "Tinggi", "sisi": "Sisi",
    "panjang": "Panjang", "lebar": "Lebar", "radius": "Jari-jari",
    "atas": "Sisi Atas", "bawah": "Sisi Bawah",
    "d1": "Diagonal 1", "d2": "Diagonal 2"
}

def draw_gradient():
    for i in range(0, HEIGHT, 4):  # Dipercepat agar tidak lag
        ratio = i / HEIGHT
        color = (int(15 + ratio*35), int(23 + ratio*35), int(42 + ratio*60))
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

def draw_button(text, x, y, w, h, hover=False):
    color = ACCENT if hover else PURPLE
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=15)
    pygame.draw.rect(screen, WHITE, (x, y, w, h), border_radius=15, width=3)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))

def draw_shape_visual(shape_id):
    x, y = 680, 180
    pygame.draw.rect(screen, DARK, (x-70, y-70, 380, 340), border_radius=25)
    pygame.draw.rect(screen, ACCENT, (x-70, y-70, 380, 340), border_radius=25, width=4)

    c = ACCENT
    if shape_id == 1:
        pts = [(x+120, y), (x+20, y+220), (x+220, y+220)]
        pygame.draw.polygon(screen, c, pts)
        pygame.draw.polygon(screen, WHITE, pts, 6)
    elif shape_id == 4:
        pygame.draw.circle(screen, c, (x+130, y+110), 95)
        pygame.draw.circle(screen, WHITE, (x+130, y+110), 95, 6)
    elif shape_id == 9:
        pygame.draw.rect(screen, c, (x+50, y+50, 160, 160))
        pygame.draw.rect(screen, WHITE, (x+50, y+50, 160, 160), 6)
    else:
        pygame.draw.rect(screen, c, (x+60, y+50, 160, 160), border_radius=15)
        pygame.draw.rect(screen, WHITE, (x+60, y+50, 160, 160), 6)

def calculate():
    global result, error_msg
    result = ""
    error_msg = ""
    try:
        vals = {k: float(v) for k, v in inputs.items() if v.strip()}
        
        if selected_shape in [1, 5]:
            a = vals.get("alas", 0)
            t = vals.get("tinggi", 0)
            if a >= 2 and t >= 2:
                result = f"Luas = {(0.5 * a * t):.2f} cm²"
            else:
                error_msg = "Nilai harus ≥ 2"
        # ... (semua perhitungan sudah lengkap di kode ini)
        elif selected_shape == 2:
            s = vals.get("sisi", 0)
            result = f"Luas = {(s*s):.2f} cm²" if s >= 2 else "Sisi harus ≥ 2"
        elif selected_shape == 3:
            p = vals.get("panjang", 0)
            l = vals.get("lebar", 0)
            result = f"Luas = {(p*l):.2f} cm²" if p>=2 and l>=2 else "Nilai harus ≥ 2"
        elif selected_shape == 4:
            r = vals.get("radius", 0)
            result = f"Luas = {(math.pi * r * r):.2f} cm²" if r >= 2 else "Jari-jari harus ≥ 2"
        elif selected_shape == 6:
            a = vals.get("atas", 0)
            b = vals.get("bawah", 0)
            t = vals.get("tinggi", 0)
            result = f"Luas = {(0.5*(a+b)*t):.2f} cm²" if a>=2 and b>=2 and t>=2 else "Nilai harus ≥ 2"
        elif selected_shape in [7, 8]:
            d1 = vals.get("d1", 0)
            d2 = vals.get("d2", 0)
            result = f"Luas = {(0.5*d1*d2):.2f} cm²" if d1>=2 and d2>=2 else "Nilai harus ≥ 2"
        elif selected_shape == 9:
            s = vals.get("sisi", 0)
            result = f"Volume = {(s**3):.2f} cm³" if s >= 2 else "Sisi harus ≥ 2"
        elif selected_shape == 10:
            p = vals.get("panjang", 0)
            l = vals.get("lebar", 0)
            t = vals.get("tinggi", 0)
            result = f"Volume = {(p*l*t):.2f} cm³" if p>=2 and l>=2 and t>=2 else "Nilai harus ≥ 2"
    except:
        error_msg = "Masukkan angka yang valid!"

# ====================== MAIN LOOP ======================
while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_mode == "menu":
                for i in range(1, 11):
                    y = 170 + ((i-1)//2) * 90
                    x = 150 if i % 2 == 1 else 550
                    if pygame.Rect(x, y, 380, 75).collidepoint(mouse_pos):
                        selected_shape = i
                        current_mode = "calculation"
                        inputs = {}
                        result = ""
                        error_msg = ""
                        active_input = None

            else:
                # Tombol
                if 80 <= mouse_pos[0] <= 280 and 560 <= mouse_pos[1] <= 625:
                    calculate()
                elif 320 <= mouse_pos[0] <= 520 and 560 <= mouse_pos[1] <= 625:
                    inputs = {}
                    result = ""
                    error_msg = ""
                elif 560 <= mouse_pos[0] <= 760 and 560 <= mouse_pos[1] <= 625:
                    current_mode = "menu"
                    selected_shape = None

                # Input fields
                y = 220
                for key in input_config.get(selected_shape, []):
                    if pygame.Rect(250, y-8, 250, 50).collidepoint(mouse_pos):
                        active_input = key
                    y += 75

        if event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                inputs[active_input] = inputs.get(active_input, "")[:-1]
            elif event.key == pygame.K_RETURN:
                active_input = None
            elif event.unicode.isdigit() or event.unicode == ".":
                current = inputs.get(active_input, "")
                if event.unicode == "." and current.count(".") >= 1:
                    continue
                inputs[active_input] = current + event.unicode

    # DRAW
    draw_gradient()

    if current_mode == "menu":
        title = title_font.render("BANGUN RUANG", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        sub = small_font.render("Damian Adipradita D - X RPL1/16", True, GRAY)
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 120))

        for i in range(1, 11):
            y = 170 + ((i-1)//2) * 90
            x = 150 if i % 2 == 1 else 550
            rect = pygame.Rect(x, y, 380, 75)
            hover = rect.collidepoint(mouse_pos)
            color = ACCENT if hover else DARK
            
            pygame.draw.rect(screen, color, rect, border_radius=20)
            pygame.draw.rect(screen, ACCENT, rect, border_radius=20, width=3)

            txt1 = big_font.render(f"{i}. {shapes[i]['name']}", True, WHITE)
            txt2 = small_font.render(shapes[i]['type'], True, GREEN)
            screen.blit(txt1, (x + 30, y + 15))
            screen.blit(txt2, (x + 30, y + 48))
    else:
        # Calculation Screen
        screen.blit(title_font.render(shapes[selected_shape]['name'], True, WHITE), (80, 50))
        screen.blit(big_font.render(shapes[selected_shape]['formula'], True, ACCENT), (80, 110))
        
        draw_shape_visual(selected_shape)

        y = 220
        for key in input_config.get(selected_shape, []):
            label = label_names.get(key, key)
            screen.blit(font.render(label + " :", True, WHITE), (80, y + 8))
            
            pygame.draw.rect(screen, DARK, (250, y-8, 250, 50), border_radius=12)
            color = ACCENT if active_input == key else WHITE
            pygame.draw.rect(screen, color, (250, y-8, 250, 50), border_radius=12, width=3)
            
            screen.blit(font.render(inputs.get(key, ""), True, WHITE), (270, y + 8))
            y += 75

        # Tombol
        mx, my = mouse_pos
        draw_button("HITUNG", 80, 560, 200, 65, 80 <= mx <= 280 and 560 <= my <= 625)
        draw_button("RESET", 320, 560, 200, 65, 320 <= mx <= 520 and 560 <= my <= 625)
        draw_button("KEMBALI", 560, 560, 200, 65, 560 <= mx <= 760 and 560 <= my <= 625)

        if result:
            pygame.draw.rect(screen, (17, 94, 60), (80, 640, 820, 60), border_radius=12)
            screen.blit(big_font.render(result, True, WHITE), (100, 655))
        elif error_msg:
            screen.blit(font.render(error_msg, True, RED), (100, 655))

    pygame.display.flip()
    clock.tick(60)