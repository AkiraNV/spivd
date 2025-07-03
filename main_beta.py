import pygame
import classes
from classes import Ship, Enemy
from levels import LEVEL_DATA, spawn_enemies_for_wave, spawn_boss_for_level

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((classes.WIDTH, classes.HEIGHT))
    classes.PROJ = classes.ally_proj()
    clock = pygame.time.Clock()

    # --- SETUP LEVEL/WAVE ---
    current_level = 1
    current_wave = 0
    player: Ship = Ship(classes.state())

    all_sprites = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    ship_projectiles = pygame.sprite.Group()
    enemy_proj = pygame.sprite.Group()

    # Load first wave
    spawn_enemies_for_wave(current_level, current_wave, all_sprites, enemies)
    boss_spawned = False
    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- WAVE/LEVEL PROGRESSION ---
        if not enemies:
            if not boss_spawned and current_wave + 1 < len(LEVEL_DATA[current_level]['waves']):
                current_wave += 1
                spawn_enemies_for_wave(current_level, current_wave, all_sprites, enemies)
            elif not boss_spawned:
                # End of waves, spawn boss if any
                if spawn_boss_for_level(current_level, all_sprites, enemies):
                    boss_spawned = True
                else:
                    boss_spawned = True  # No boss, mark as done
            elif boss_spawned:
                # End of boss, next level
                if current_level + 1 in LEVEL_DATA:
                    current_level += 1
                    current_wave = 0
                    boss_spawned = False
                    enemies.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    spawn_enemies_for_wave(current_level, current_wave, all_sprites, enemies)
                    ship_projectiles.empty()
                    enemy_proj.empty()
                else:
                    running = False
                    print("Chiến thắng! Trò chơi kết thúc.")

        # --- DRAW & UPDATE ---
        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 1)

        # --- COLLISIONS ---
        hits = pygame.sprite.groupcollide(ship_projectiles, enemies, True, False)
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
                player.take_damage(10)

        def pe_collision(player, enemy):
            return player.hitbox.colliderect(enemy.rect)
        collision_hits = pygame.sprite.spritecollide(player, enemies, False, collided=pe_collision)
        if collision_hits and not player.invincible:
            player.take_damage(50)

        # Remove dead enemies
        for sprite in enemies:
            if not sprite.alive:
                sprite.kill()

        # --- PLAYER SHOOT ---
        keys = pygame.key.get_pressed()
        if player.alive and keys[pygame.K_SPACE]:
            player.shoot(ship_projectiles)

        ship_projectiles.update()
        ship_projectiles.draw(screen)

        # --- ENEMY ACTIONS ---
        player_pos = None
        if player.alive:
            player_pos = (player.rect.centerx, player.rect.centery)

        for enemy in enemies:
            enemy.move_and_shoot(enemy_proj, player_pos)

        enemy_proj.update()
        enemy_proj.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    start_game()