# main.py
import pygame, classes, random
from classes import Ship, Enemy, Boss


def draw_bossbar(screen, boss, width=400, height=30):
    x = (classes.WIDTH - width) // 2
    y = 20

    if boss.current_phase >= boss.max_phases and boss.health_point <= 0:
        return

    ratio = (boss.health_point / boss.max_hp) * boss.max_phases
    fill = int(width * ratio)

    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))              # background
    pygame.draw.rect(screen, (255, 0, 0), (x, y, fill, height))            # health fill
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)    # border


def start_game():
    pygame.init()
    # pygame.mixer.init() 
    # pygame.mixer.music.load('n-Dimensions (Main Theme - Retro Ver (mp3cut.net) (1).ogg')
    # pygame.mixer.music.play(-1)  
    screen = pygame.display.set_mode((classes.WIDTH, classes.HEIGHT))
    clock = pygame.time.Clock()

    # Create entities
    player: Ship = Ship(classes.state())
    enemies = [Boss(500, 10, 300)]
    # enemies = [Enemy(200, 10, 100, 'neutral')]
    all_sprites = pygame.sprite.Group(player, *enemies)
    ship_projectiles = pygame.sprite.Group()
    enemy_proj = pygame.sprite.Group()
    loot_group = pygame.sprite.Group()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill((0, 0, 0))

        # Update and draw
        all_sprites.update()
        all_sprites.draw(screen)
        # pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 1)   #Toggle hitbox



        #Collisions
        #Ship to enemy
        hits = pygame.sprite.groupcollide(ship_projectiles, all_sprites, True, False)
        for projectile, hit_list in hits.items():
            for target in hit_list:
                if isinstance(target, Enemy):
                    damage = getattr(projectile, 'damage_factor', 1.0) * player.strength
                    print(f"Hit {target.__class__.__name__} for {damage} damage")  # ADD THIS
                    target.take_damage(damage)

        #Enemy to ship
        #Hitbox shrink
        # def player_hitbox_collision(player, projectile):
        #     return player.hitbox.colliderect(projectile.rect)

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
            loot_type = random.randint(0, 4)
            print(f"Loot dropped at ({enemy.rect.centerx}, {enemy.rect.centery})")
            new_loot = classes.Loot(
                enemy.rect.centerx,
                enemy.rect.centery,
                classes.loot()[loot_type],
                loot_type
            )
            loot_group.add(new_loot)
            enemy.kill()
            all_sprites.remove(enemy)
            if enemy in enemies:
                enemies.remove(enemy)
        
        loot_group.update()
        loot_group.draw(screen)
        
        def player_loot_collision(player, loot):
            return player.hitbox.colliderect(loot.rect)

        collected = pygame.sprite.spritecollide(player, loot_group, True, collided=player_loot_collision)
        for item in collected:
            if item.loot_type == 0: #Gift
                player.score += 100
                print(f"Score: {player.score}")
            elif item.loot_type == 1: #Power
                player.level = min(player.level + 1, 4)
            elif item.loot_type == 2: #Shield
                player.invincible = True
                player.grace_period()
                print("Shield collected!")
            elif item.loot_type == 3:  # Bomb
                player.bomb += 1
                print(f"Bombs: {player.bomb}")
            elif item.loot_type == 4:  # Food
                player.health_point = min(player.health_point + 1, 10)
                print(f"Health: {player.health_point}")

        #shoot
        keys = pygame.key.get_pressed()
        if player.alive and keys[pygame.K_SPACE]:
            player.shoot(ship_projectiles)
            
        ship_projectiles.update()
        ship_projectiles.draw(screen)

        #Ship proj hb (green)
        # for proj in ship_projectiles:
        #     pygame.draw.rect(screen, (0, 255, 0), proj.rect, 1)

        player_pos = None
        if player.alive:
            player_pos = (player.rect.centerx, player.rect.centery)
            player.left_gun.draw(screen)
            player.right_gun.draw(screen)

        for enemy in enemies:
            enemy.move_and_shoot(enemy_proj, player_pos)

        enemy_proj.update()
        enemy_proj.draw(screen)

        #Enemy proj hb
        for proj in enemy_proj:
            if hasattr(proj, "mask"):
                offset = proj.rect.topleft
                outline = proj.mask.outline()
                for point in outline:
                    screen.set_at((point[0] + offset[0], point[1] + offset[1]), (255, 0, 0))
                    
        for enemy in enemies:
            if isinstance(enemy, Boss) and enemy.alive:
                draw_bossbar(screen, enemy)


        # Flip the screen
        pygame.display.flip()
        if not player.alive:
            if hasattr(player, "death_animation_done"):
                if player.death_animation_done:
                    running = False

    pygame.mixer.music.stop()
    # pygame.quit()

if __name__ == "__main__":
    start_game()
