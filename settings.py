import pygame, os
# Settings

SETTINGS_TXT = "settings.txt"

DEFAULT_SETTINGS_TXT = {
    "Âm lượng tổng": 100,
    "Âm lượng nhạc": 50,
    "Âm lượng âm thanh": 50,
    "Di chuyển lên": "W",
    "Di chuyển xuống": "S",
    "Di chuyển trái": "A",
    "Di chuyển phải": "D",
    "Bắn": "SPACE",
    "Bom": "Z",
    "Giảm tốc": "LEFT SHIFT"
}

def load_txt_settings():
    settings = DEFAULT_SETTINGS_TXT.copy()
    if not os.path.exists(SETTINGS_TXT):
        return settings

    with open(SETTINGS_TXT, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, val = map(str.strip, line.strip().split(":", 1))
                if key.startswith("Âm lượng"):
                    try:
                        settings[key] = int(val)
                    except:
                        settings[key] = DEFAULT_SETTINGS_TXT[key]
                else:
                    settings[key] = val.upper()
    return settings

def save_txt_settings(settings):
    with open(SETTINGS_TXT, "w", encoding="utf-8") as f:
        for key, val in settings.items():
            f.write(f"{key}: {val}\n")

def settings_menu_from_txt(screen, font):
    clock = pygame.time.Clock()
    settings = load_txt_settings()
    waiting_for_key = None

    volume_labels = ["Âm lượng tổng", "Âm lượng nhạc", "Âm lượng âm thanh"]
    key_labels = [
        "Di chuyển lên", "Di chuyển xuống", "Di chuyển trái", "Di chuyển phải",
        "Bắn", "Bom", "Giảm tốc"
    ]

    while True:
        screen.fill((30, 30, 30))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        y = 50

        title = font.render("Cài đặt", True, (255, 255, 0))
        screen.blit(title, ((720 - title.get_width()) // 2, 10))

        # Volume sliders
        for vol_key in volume_labels:
            val = settings[vol_key] / 100
            pygame.draw.rect(screen, (100, 100, 100), (50, y, 200, 20))
            pygame.draw.rect(screen, (0, 200, 0), (50, y, int(200 * val), 20))
            label = font.render(f"{vol_key}: {settings[vol_key]}%", True, (255, 255, 255))
            screen.blit(label, (270, y))

            if pygame.Rect(50, y, 200, 20).collidepoint(mouse) and click:
                rel_x = mouse[0] - 50
                settings[vol_key] = min(100, max(0, int((rel_x / 200) * 100)))
                master = settings["Âm lượng tổng"] / 100
                sfx = settings["Âm lượng âm thanh"] / 100
                bgm = settings["Âm lượng nhạc"] / 100

                pygame.mixer.music.set_volume(bgm * master)

                from classes import SFX  # Add this at top if needed
                for sound in SFX.values():
                    sound.set_volume(sfx * master)

            y += 40

        y += 30

        # Key bindings
        for label in key_labels:
            key_name = settings[label]
            text = font.render(f"{label}: {key_name}", True, (255, 255, 255))
            rect = text.get_rect(topleft=(50, y))
            screen.blit(text, rect)

            if rect.collidepoint(mouse) and click and not waiting_for_key:
                waiting_for_key = label
            y += 40

        # Prompt for rebinding
        if waiting_for_key:
            prompt = font.render(f"Nhấn phím cho: {waiting_for_key}", True, (255, 100, 100))
            screen.blit(prompt, (50, y + 20))

        back_text = font.render("Nhấn để quay lại", True, (200, 200, 200))
        back_rect = back_text.get_rect(topleft=(50, 600))
        screen.blit(back_text, back_rect)

        if click and back_rect.collidepoint(mouse):
            save_txt_settings(settings)
            return
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_txt_settings(settings)
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if waiting_for_key:
                    settings[waiting_for_key] = pygame.key.name(event.key).upper()
                    waiting_for_key = None
                elif event.key == pygame.K_ESCAPE:
                    save_txt_settings(settings)
                    return
                
        clock.tick(60)