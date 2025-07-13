import pygame, sys, os
import game
from classes import SFX, load_bgm, BGM
from settings import load_txt_settings, settings_menu_from_txt
# === Screen and Settings ===
WIDTH, HEIGHT = 720, 640
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)

# === Font & Menu ===
font_path = './Audiowide,Orbitron,Press_Start_2P,VT323/VT323/VT323-Regular.ttf'
font_size = 35
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
font = pygame.font.Font(font_path, font_size)
font_large = pygame.font.Font(font_path, font_size + 10)
line_height = int(font.get_height() * 1.2)
padding_from_bottom = int(line_height * 0.5)
COLOR_NORMAL_TEXT = (255, 255, 255)
COLOR_NORMAL_OUTLINE = (40, 40, 40)
COLOR_HOVER_TEXT = (169, 169, 169)
COLOR_HOVER_OUTLINE = (255, 255, 0)
outline_thickness_normal = max(1, font_size // 20)
outline_thickness_hover = max(2, font_size // 15)

# === Helper function to load guide ===
def load_guide(filepath, lines_per_page=12):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    sections = []
    current_section = {"title": None, "lines": []}
    for line in lines:
        if line.startswith("#"):
            if current_section["title"]:
                sections.append(current_section)
            current_section = {"title": line[1:].strip(), "lines": []}
        else:
            current_section["lines"].append(line)
    if current_section["title"]:
        sections.append(current_section)

    pages = []
    for section in sections:
        lines = section["lines"]
        for i in range(0, len(lines), lines_per_page):
            page = {
                "title": section["title"],
                "lines": lines[i:i+lines_per_page]
            }
            pages.append(page)
    return pages


def input_player_name(screen, font, background_surface):
    name = ""
    active = True
    clock = pygame.time.Clock()

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode

        # Dừng background động — chỉ vẽ background tĩnh đã có sẵn
        screen.blit(background_surface, (0, 0))

        # Render nội dung
        prompt_text = "Nhập tên (Enter để xác nhận):"
        prompt_surf = font.render(prompt_text, True, (255, 255, 255))
        name_surf = font.render(name, True, (255, 255, 0))

        # Vị trí hiển thị — cùng hàng
        base_x = 50
        base_y = HEIGHT // 2
        screen.blit(prompt_surf, (base_x, base_y))
        screen.blit(name_surf, (base_x + prompt_surf.get_width() + 10, base_y))

        pygame.display.flip()
        clock.tick(30)

    return name if name else "NoName"
def save_score(name, score, filename="score.txt"):
    new_line = f"{name}: {score}\n"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["#Điểm cao nhất\n"]

    if not lines or not lines[0].startswith("#"):
        lines.insert(0, "#Điểm cao nhất\n")

    lines.insert(1, new_line)

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)

def generate_display_scores(input_file="score.txt", output_file="score_display.txt"):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if ":" in line]
    except FileNotFoundError:
        lines = []

    scores = sorted(lines, key=lambda x: int(x.split(":")[1]), reverse=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#Điểm cao nhất\n")
        if scores:
            for line in scores:
                f.write(line + "\n")
        else:
            f.write("Chưa có điểm nào.\n")

def clear_scores_but_keep_header(filename="score.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if lines and lines[0].startswith("#"):
            header = lines[0]
        else:
            header = "#Điểm cao nhất\n"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(header)
    except FileNotFoundError:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#Điểm cao nhất\n")

# === Sounds ===
pygame.mixer.init()
pygame.mixer.music.load(BGM["menu"])
pygame.mixer.music.play(-1)

def update_sfx_volume(sfx_dict, volume_value):
    for sound in sfx_dict.values():
        sound.set_volume(volume_value)

# === Backgrounds ===
def load_background(path, fallback_color=(30, 30, 30)):
    try:
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    except:
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(fallback_color)
        return surface
menu_background = load_background('./imgs/menu.png')
alt_background = load_background('./imgs/altmenu.png')
# === Background Scroll ===
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./imgs/super.png").convert()
        self.image = pygame.transform.scale(self.image, (720, 1080))
        self.rect = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.rect2.y = -self.rect.height
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        self.rect2.y += self.speed
        if self.rect.y > self.rect.height:
            self.rect.y = -self.rect.height
        if self.rect2.y > self.rect.height:
            self.rect2.y = -self.rect.height

# === Game State ===
def draw_text_with_outline(text, font, text_color, outline_color, x, y, outline_thickness):
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:
                outline_surf = font.render(text, True, outline_color)
                screen.blit(outline_surf, (x + dx, y + dy))
    text_surf = font.render(text, True, text_color)
    screen.blit(text_surf, (x, y))

# === Load màn hình ===
def load_screen(file):
    guide_pages = load_guide(file)
    if not guide_pages:
        print(f"⚠ File '{file}' không có nội dung hợp lệ.")
        return

    is_score_screen = (file == "score_display.txt")
    total_pages = len(guide_pages)
    current_page = 0
    clock = pygame.time.Clock()

    while True:
        screen.blit(alt_background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RIGHT and current_page < total_pages - 1:
                    current_page += 1
                elif event.key == pygame.K_LEFT and current_page > 0:
                    current_page -= 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                SFX["select"].play()
                mouse_click = True

        section_title = guide_pages[current_page]["title"]
        title_surf = font_large.render(section_title, True, YELLOW)
        screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, 30))

        page_lines = guide_pages[current_page]["lines"]
        for i, line in enumerate(page_lines):
            line_surf = font.render(line, True, COLOR_NORMAL_TEXT)
            screen.blit(line_surf, (50, 100 + i * line_height))

        prev_rect = next_rect = delete_rect = None
        if current_page > 0:
            prev_surf = font.render("<", True, COLOR_NORMAL_TEXT)
            prev_rect = prev_surf.get_rect(topleft=(50, HEIGHT - 60))
            screen.blit(prev_surf, prev_rect)
        if current_page < total_pages - 1:
            next_surf = font.render(">", True, COLOR_NORMAL_TEXT)
            next_rect = next_surf.get_rect(topright=(WIDTH - 50, HEIGHT - 60))
            screen.blit(next_surf, next_rect)

        # Vẽ nút Delete nếu là màn điểm số
        if is_score_screen:
            delete_surf = font.render("Delete", True, (255, 0, 0))
            delete_rect = delete_surf.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            screen.blit(delete_surf, delete_rect)

        if mouse_click:
            if prev_rect and prev_rect.collidepoint(mouse_pos):
                current_page -= 1
            if next_rect and next_rect.collidepoint(mouse_pos):
                current_page += 1
            if is_score_screen and delete_rect and delete_rect.collidepoint(mouse_pos):
                clear_scores_but_keep_header("score.txt")
                generate_display_scores()
                guide_pages = load_guide("score_display.txt")
                total_pages = len(guide_pages)
                current_page = 0
                continue

        pygame.display.flip()
        clock.tick(60)


# === Menu ===
def run_menu():
    menu_options = ["Chơi", "Điểm cao nhất", "Hướng dẫn tân thủ", "Cài đặt", "Thoát"]
    current_screen = "menu"
    menu_rects = []
    clock = pygame.time.Clock()
    running = True
    
    

    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_screen == "menu":
                    for i, rect in enumerate(menu_rects):
                        if rect.collidepoint(mouse_pos):
                            SFX["select"].play()
                            option = menu_options[i]
                            if option == "Chơi":
                                pygame.mixer.music.stop()
                                game.start_game()
                            elif option == "Thoát":
                                running = False
                            elif option == "Điểm cao nhất":
                                generate_display_scores()
                                load_screen("score_display.txt")
                            elif option == "Lời cảm ơn":
                                current_screen = "thanks"
                            elif option == "Hướng dẫn tân thủ":
                                load_screen("guide.txt")
                            elif option == "Cài đặt":
                                current_screen = "settings"

        screen.blit(menu_background if current_screen == "menu" else alt_background, (0, 0))
        if current_screen == "menu":
            menu_rects.clear()
            total_menu_height = len(menu_options) * line_height
            start_y = HEIGHT - total_menu_height - padding_from_bottom
            for i, option in enumerate(menu_options):
                text_surface = font.render(option, True, (0, 0, 0))
                x = (WIDTH - text_surface.get_width()) // 2
                y = start_y + (i * line_height)
                rect = text_surface.get_rect(topleft=(x, y))
                menu_rects.append(rect)
                if rect.collidepoint(mouse_pos):
                    draw_text_with_outline(option, font, COLOR_HOVER_TEXT, COLOR_HOVER_OUTLINE, x, y, outline_thickness_hover)
                else:
                    draw_text_with_outline(option, font, COLOR_NORMAL_TEXT, COLOR_NORMAL_OUTLINE, x, y, outline_thickness_normal)
        else:
            text = ""
            if current_screen == "high_score":
                text = "Điểm cao nhất: 1000"
            elif current_screen == "thanks":
                text = "Cảm ơn bạn đã chơi!"
            elif current_screen == "settings":
                settings_menu_from_txt(screen, font)
                settings = load_txt_settings()
                sfx_vol = settings["Âm lượng âm thanh"] / 100
                update_sfx_volume(SFX, sfx_vol)
                current_screen = "menu"
            if text:
                draw_text_with_outline(text, font, COLOR_NORMAL_TEXT, COLOR_NORMAL_OUTLINE,
                                       (WIDTH - font.size(text)[0]) // 2, 50, outline_thickness_normal)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# === Run ===
if __name__ == '__main__':
    run_menu()
