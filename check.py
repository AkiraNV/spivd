import pygame, random, sys

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
font_size = 30
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Max")
font = pygame.font.Font(font_path, font_size)
line_height = int(font.get_height() * 1.2)
padding_from_bottom = int(line_height * 0.5)
COLOR_NORMAL_TEXT = (255, 255, 255)
COLOR_NORMAL_OUTLINE = (40, 40, 40)
COLOR_HOVER_TEXT = (169, 169, 169)
COLOR_HOVER_OUTLINE = (255, 255, 0)
outline_thickness_normal = max(1, font_size // 20)
outline_thickness_hover = max(2, font_size // 15)

# === Background Scroll ===
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./imgs/scroll.png").convert()
        self.image = pygame.transform.scale(self.image, (720, 6480))
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

class Polygon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        n = random.randint(3, 12)
        r = random.randint(10, 50)
        self.points = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(n)]
        self.rect = pygame.Rect(random.randint(0, WIDTH), random.randint(-100, -10), r * 2, r * 2)
        self.image = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        color = random.choice([RED, GREEN, BLUE, YELLOW, PINK])
        pygame.draw.polygon(self.image, color, [(x + r, y + r) for x, y in self.points], random.randint(1, 2))
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-100, -10)
            self.rect.x = random.randint(0, WIDTH)

def create_polygons(group):
    group.empty()
    for _ in range(20):
        group.add(Polygon())

# === Game State ===
def draw_text_with_outline(text, font, text_color, outline_color, x, y, outline_thickness):
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:
                outline_surf = font.render(text, True, outline_color)
                screen.blit(outline_surf, (x + dx, y + dy))
    text_surf = font.render(text, True, text_color)
    screen.blit(text_surf, (x, y))

def start_game():
    import classes
    from classes import Ship, Enemy
    screen = pygame.display.set_mode((classes.WIDTH, classes.HEIGHT))
    clock = pygame.time.Clock()

    bg = Background()
    all_polygons = pygame.sprite.RenderUpdates()
    create_polygons(all_polygons)
    option_scroll = 0

    player = Ship(classes.state())
    enemies = [Enemy(100, 10, 10, "neutral")]
    all_sprites = pygame.sprite.Group(player, *enemies)
    ship_projectiles = pygame.sprite.Group()
    enemy_proj = pygame.sprite.Group()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_s:
                    option_scroll = 1 - option_scroll
                    if option_scroll == 1:
                        create_polygons(all_polygons)

        # Background
        if option_scroll == 0:
            bg.update()
            screen.blit(bg.image, bg.rect)
            screen.blit(bg.image, bg.rect2)
        else:
            screen.fill(BLACK)
            all_polygons.update()
            all_polygons.draw(screen)

        # Gameplay
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.draw.rect(screen, RED, player.hitbox, 1)

        hits = pygame.sprite.groupcollide(ship_projectiles, all_sprites, True, False)
        for projectile, hit_list in hits.items():
            for target in hit_list:
                if isinstance(target, Enemy):
                    target.take_damage(player.strength)

        def player_hitbox_collision(player, projectile):
            if not hasattr(projectile, "mask"):
                return False
            offset = (player.hitbox.left - projectile.rect.left, player.hitbox.top - projectile.rect.top)
            player_mask = pygame.Mask(player.hitbox.size, fill=True)
            return projectile.mask.overlap(player_mask, offset) is not None

        enemy_hits = pygame.sprite.spritecollide(player, enemy_proj, True, collided=player_hitbox_collision)
        for proj in enemy_hits:
            if not player.invincible:
                player.take_damage(enemies[0].strength)
                if not player.alive:
                    death_start = pygame.time.get_ticks()
                    while True:
                        clock.tick(60)
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                        # Background redraw
                        if option_scroll == 0:
                            bg.update()
                            screen.blit(bg.image, bg.rect)
                            screen.blit(bg.image, bg.rect2)
                        else:
                            screen.fill(BLACK)
                            all_polygons.update()
                            all_polygons.draw(screen)

                        all_sprites.update()
                        all_sprites.draw(screen)
                        ship_projectiles.update()
                        ship_projectiles.draw(screen)
                        enemy_proj.update()
                        enemy_proj.draw(screen)

                        pygame.display.flip()

                        # Check if death animation is done
                        if not player.alive and player not in all_sprites:
                            break

                    return

        def pe_collision(player, enemy):
            return player.hitbox.colliderect(enemy.rect)
        collision_hits = pygame.sprite.spritecollide(player, all_sprites, False, collided=pe_collision)

        for sprite in all_sprites:
            if isinstance(sprite, Enemy) and not sprite.alive:
                all_sprites.remove(sprite)

        keys = pygame.key.get_pressed()
        if player.alive and keys[pygame.K_SPACE]:
            player.shoot(ship_projectiles)

        ship_projectiles.update()
        ship_projectiles.draw(screen)
        for proj in ship_projectiles:
            pygame.draw.rect(screen, GREEN, proj.rect, 1)

        player_pos = (player.rect.centerx, player.rect.centery) if player.alive else None
        for enemy in enemies:
            enemy.move_and_shoot(enemy_proj, player_pos)

        enemy_proj.update()
        enemy_proj.draw(screen)
        for proj in enemy_proj:
            if hasattr(proj, "mask"):
                offset = proj.rect.topleft
                outline = proj.mask.outline()
                for point in outline:
                    screen.set_at((point[0] + offset[0], point[1] + offset[1]), RED)

        pygame.display.flip()

# === Menu ===
def run_menu():
    try:
        background_image = pygame.image.load('better1.png').convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    except:
        background_image = pygame.Surface((WIDTH, HEIGHT))
        background_image.fill((30, 30, 30))

    menu_options = [
        "Chơi",
        "Điểm cao nhất",
        "Tốc độ",
        "Lời cảm ơn",
        # "Ngôn ngữ",
        "Scrolling",
        "Thoát"
    ]
    current_screen = "menu"
    menu_rects = []
    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if current_screen == "menu":
                    for i, rect in enumerate(menu_rects):
                        if rect.collidepoint(mouse_pos):
                            option = menu_options[i]
                            if option == "Chơi":
                                start_game()
                            elif option == "Thoát":
                                running = False
                            elif option == "Điểm cao nhất":
                                current_screen = "high_score"
                            elif option == "Tốc độ":
                                current_screen = "speed"
                            elif option == "Lời cảm ơn":
                                current_screen = "thanks"
                            elif option == "Ngôn ngữ":
                                current_screen = "language"
                            elif option == "Scrolling":
                                current_screen = "scrolling"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = "menu"

        screen.blit(background_image, (0, 0))
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
            elif current_screen == "speed":
                text = "Tốc độ: 60 FPS"
            elif current_screen == "thanks":
                text = "Cảm ơn bạn đã chơi!"
            elif current_screen == "language":
                text = "Ngôn ngữ: Tiếng Việt"
            elif current_screen == "scrolling":
                text = "Scrolling: Không gian"

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
