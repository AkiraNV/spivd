# main.py
import pygame, classes, random
from classes import Ship, Enemy, Loot, Boss, SFX, load_bgm, BGM, bgm_vol
from levels import LEVEL_DATA, spawn_enemies_for_wave, spawn_boss_for_level
from main import save_score, input_player_name
from settings import load_txt_settings

settings = load_txt_settings()

def draw_bossbar(screen, boss, width=500, height=20):
    x = (classes.WIDTH - width) // 2
    y = 60

    if boss.current_phase >= boss.max_phases and boss.health_point <= 0:
        return

    ratio = (boss.health_point / boss.max_hp) * boss.max_phases
    fill = int(width * ratio)

    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))              # background
    pygame.draw.rect(screen, (255, 0, 0), (x, y, fill, height))            # health fill
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)    # border

def draw_interface(screen, player, icons, level, wave):
    bar_height = 60
    screen_width = classes.WIDTH
    padding = 10
    spacing = 26
    icon_offset_x = 65
    icon_offset_y = 2
    font = pygame.font.SysFont("Arial", 20)

    # Background bar
    pygame.draw.rect(screen, (20, 20, 20), (0, 0, screen_width, bar_height))

    # Lives
    screen.blit(font.render("Lives:", True, (255, 255, 255)), (padding, padding))
    for i in range(player.max_life):
        icon = icons["heart_full"] if i < player.life else icons["heart_empty"]
        screen.blit(icon, (padding + icon_offset_x + i * spacing, padding + icon_offset_y))

    # Bombs
    screen.blit(font.render("Bombs:", True, (255, 255, 255)), (padding, padding + 24))
    for i in range(min(player.bomb, player.max_bomb)):
        screen.blit(icons["bomb"], (padding + icon_offset_x + i * spacing, padding + 30))

    # Score (center top)
    score_text = font.render(f"Score: {player.score}", True, (0, 255, 255))
    score_rect = score_text.get_rect(centerx=screen_width // 2, top=padding)
    screen.blit(score_text, score_rect)

    # Level (top right)
    player_level_text = font.render(f"Ship level: {player.level:.2f}", True, (0, 200, 255))
    level_text = font.render(f"Game level - Wave: {level} - {wave + 1}", True, (0, 200, 255))

    level_rect = player_level_text.get_rect(topright=(screen_width - padding, padding))
    wave_rect = level_text.get_rect(topright=(screen_width - padding, padding + 20))

    screen.blit(player_level_text, level_rect)
    screen.blit(level_text, wave_rect)

    # === Về menu button ===
    menu_font = pygame.font.SysFont("Arial", 18)
    menu_text = menu_font.render("Về menu", True, (255, 100, 100))
    menu_rect = menu_text.get_rect(center=(screen_width // 2, score_rect.bottom + 16))
    screen.blit(menu_text, menu_rect)

    return menu_rect

def show_pause_menu(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)
    big_font = pygame.font.SysFont("Arial", 36)

    background = screen.copy()
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # translucent black overlay

    # Buttons
    continue_text = font.render("Tiếp tục", True, (255, 255, 255))
    quit_text = font.render("Trở về menu", True, (255, 100, 100))
    warning = big_font.render("Tiến trình hiện tại sẽ không được lưu!", True, (255, 255, 0))

    continue_rect = continue_text.get_rect(center=(classes.WIDTH // 2, 300))
    quit_rect = quit_text.get_rect(center=(classes.WIDTH // 2, 350))
    warning_rect = warning.get_rect(center=(classes.WIDTH // 2, 200))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_rect.collidepoint(event.pos):
                    return False  # Continue game
                elif quit_rect.collidepoint(event.pos):
                    return True   # Return to menu

        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(warning, warning_rect)
        screen.blit(continue_text, continue_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        clock.tick(60)

def start_game():
    pygame.init()
    pygame.mixer.init()  
    screen = pygame.display.set_mode((classes.WIDTH, classes.HEIGHT))
    clock = pygame.time.Clock()
    icons = classes.icons()
    
    current_level = 1
    current_wave = 0
    boss_spawned = False

    load_bgm()
    current_bgm_key = f"lv{current_level}"
    pygame.mixer.music.load(BGM.get(current_bgm_key, BGM["lv1"]))
    pygame.mixer.music.set_volume(bgm_vol)
    pygame.mixer.music.play(-1)
    
    # Create entities
    player: Ship = Ship(classes.state())
    enemies = pygame.sprite.Group()
    # enemies = pygame.sprite.Group(Boss(1000, 8, 1000))
    all_sprites = pygame.sprite.Group(player)
    ship_projectiles = pygame.sprite.Group()
    player.projectile_group_ref = ship_projectiles
    player.enemy_group_ref = enemies
    enemy_proj = pygame.sprite.Group()
    loot_group = pygame.sprite.Group()
    
    # all_sprites.add(*enemies)
    
    spawn_enemies_for_wave(current_level, current_wave, all_sprites, enemies, player = player)
    
    bomb_button_img = pygame.transform.scale(pygame.image.load("./imgs/bomb.png").convert_alpha(), (48, 48))
    bomb_button_rect = bomb_button_img.get_rect(topright=(classes.WIDTH - 10, classes.HEIGHT - 60))


    running = True
    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if (bomb_button_rect.collidepoint(event.pos) 
                    and now - player.last_bomb_time > player.bomb_cd):
                        player.bombs(enemy_proj, enemies, now)
                elif intf_rect.collidepoint(event.pos):
                    if show_pause_menu(screen):
                        return  # Player chose to return to menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if show_pause_menu(screen):
                        return
        # Clear screen
        screen.fill((0, 0, 0))

        # Update and draw
        all_sprites.update()
        all_sprites.draw(screen)
        # pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 1)   #Toggle hitbox

        #Enemy spawning logic
        if not enemies:
            if not boss_spawned and current_wave + 1 < len(LEVEL_DATA[current_level]['waves']):
                current_wave += 1
                spawn_enemies_for_wave(current_level, current_wave, all_sprites, enemies, player = player)
            elif not boss_spawned:
                if spawn_boss_for_level(current_level, all_sprites, enemies):
                    boss_spawned = True
                else:
                    boss_spawned = True
            elif boss_spawned:
                if current_level + 1 in LEVEL_DATA:
                    current_level += 1
                    current_wave = 0
                    boss_spawned = False
                    enemies.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    spawn_enemies_for_wave(current_level, current_wave, all_sprites, enemies, player = player)
                    ship_projectiles.empty()
                    enemy_proj.empty()
                    current_bgm_key = f"lv{current_level}"
                    if current_bgm_key in BGM:
                        pygame.mixer.music.load(BGM[current_bgm_key])
                        pygame.mixer.music.set_volume(bgm_vol)
                        pygame.mixer.music.play(-1)
                else:
                    running = False
                    try:
                        player_score = getattr(player, "score", 0)
                    except Exception:
                        player_score = 0
                    background_surface = screen.copy()
                    SFX[random.choice(["victory1", "victory2"])].play()
                    pygame.mixer.music.stop()
                    player_name = input_player_name(screen, font, background_surface)
                    save_score(player_name, player_score)
                    # print(f"Đã lưu: {player_name} - {player_score}")
                    break

        #Collisions
        #Ship to enemy
        hits = pygame.sprite.groupcollide(ship_projectiles, enemies, True, False)
        for projectile, hit_list in hits.items():
            for target in hit_list:
                if isinstance(target, Enemy):
                    damage = getattr(projectile, 'damage_factor', 1.0) * player.strength
                    target.take_damage(damage)

        #Enemy to ship

        def player_hitbox_collision(player, projectile):
            if not hasattr(projectile, "mask"):
                return False

            # Calculate offset between player's hitbox and projectile's rect
            offset = (player.hitbox.left - projectile.rect.left, player.hitbox.top - projectile.rect.top)

            # Create a solid mask matching the size of the player's hitbox
            player_mask = pygame.Mask(player.hitbox.size, fill=True)

            # Check for overlap
            return projectile.mask.overlap(player_mask, offset) is not None

        #Enemy bullets hit
        enemy_hits = pygame.sprite.spritecollide(player, enemy_proj, True, collided=player_hitbox_collision)
        for proj in enemy_hits:
            if not player.invincible:
                player.take_damage(enemy.strength)

        #Ship collides with enemy
        def pe_collision(player, enemy):
            return player.hitbox.colliderect(enemy.rect)
        collision_hits = pygame.sprite.spritecollide(player, all_sprites, False, collided=pe_collision)

        #Clear dead enemies and spawn loot
        dead_enemies = [e for e in all_sprites if isinstance(e, Enemy) and not e.alive]
        for enemy in dead_enemies:
            # Generate loot using Loot class method
            new_loot_items = Loot.generate_loot(enemy, player)
            for new_loot in new_loot_items:
                loot_group.add(new_loot)
            
            player.score += enemy.points

            all_sprites.remove(enemy)
            if enemy in enemies:
                enemies.remove(enemy)
            enemy.kill()
        
        loot_group.update()
        loot_group.draw(screen)
        
        def player_loot_collision(player, loot):
            return player.hitbox.colliderect(loot.rect)

        collected = pygame.sprite.spritecollide(player, loot_group, True, collided=player_loot_collision)
        for item in collected:
            item.effects(player)

        #shoot
        keys = pygame.key.get_pressed()
        if player.alive and keys[player.controls["Bắn"]] and not pygame.mouse.get_pressed()[0]:
            player.shoot(ship_projectiles)
        if player.alive and keys[player.controls["Bom"]] and now - player.last_bomb_time > player.bomb_cd:
            player.bombs(enemy_proj, enemies, now)
            
        ship_projectiles.update()
        ship_projectiles.draw(screen)


        player_pos = None
        if player.alive:
            player_pos = (player.rect.centerx, player.rect.centery)
            player.left_gun.draw(screen)
            player.right_gun.draw(screen)

        for enemy in enemies:
            if isinstance(enemy, Boss) and enemy.alive:
                draw_bossbar(screen, enemy)
                enemy.move_and_shoot(enemy_proj, player_pos, player)
                if enemy.turret_group:
                    enemy.turret_group.draw(screen) 
                    all_sprites.add(*enemy.turret_group)
                    enemies.add(*enemy.turret_group)
            else:
                enemy.move()
                enemy.shoot(enemy_proj, player_pos)
                enemy.check_existence()
            
        enemy_proj.update()
        enemy_proj.draw(screen)
                
        screen.blit(bomb_button_img, bomb_button_rect)
        intf_rect = draw_interface(screen, player, icons, current_level, current_wave)
        
        # Flip the screen
        pygame.display.flip()
        clock.tick(60)
        
        font_path = './Audiowide,Orbitron,Press_Start_2P,VT323/VT323/VT323-Regular.ttf'
        font_size = 35
        font = pygame.font.Font(font_path, font_size)
        if not player.alive:
            if hasattr(player, "death_animation_done"):
                if player.death_animation_done:
                    try:
                        player_score = getattr(player, "score", 0)
                    except Exception:
                        player_score = 0
                    background_surface = screen.copy()
                    SFX["defeat"].play()
                    player_name = input_player_name(screen, font, background_surface)
                    save_score(player_name, player_score)
                    # print(f"Đã lưu: {player_name} - {player_score}")
                    pygame.mixer.music.stop()
                    break

    pygame.mixer.music.stop()
    # pygame.quit()

if __name__ == "__main__":
    start_game()
