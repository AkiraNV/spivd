# main.py
import pygame, classes
from classes import Ship, Enemy

pygame.init()
screen = pygame.display.set_mode((classes.WIDTH, classes.HEIGHT))
clock = pygame.time.Clock()

# Create entities
player: Ship = Ship(classes.state())
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

    # Clear screen
    screen.fill((0, 0, 0))

    # Update and draw
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), player.hitbox, 1)   #Toggle hitbox

    #Collisions
    #Ship to enemy
    hits = pygame.sprite.groupcollide(ship_projectiles, all_sprites, True, False)
    for projectile, hit_list in hits.items():
        for target in hit_list:
            if isinstance(target, Enemy):
                target.take_damage(player.strength)

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


    #Clear dead enemies
    for sprite in all_sprites:
        if isinstance(sprite, Enemy) and not sprite.alive:
            all_sprites.remove(sprite)


    #shoot
    keys = pygame.key.get_pressed()
    if player.alive and keys[pygame.K_SPACE]:
        player.shoot(ship_projectiles)
        
    ship_projectiles.update()
    ship_projectiles.draw(screen)

    #Ship proj hb (green)
    for proj in ship_projectiles:
        pygame.draw.rect(screen, (0, 255, 0), proj.rect, 1)

    player_pos = None
    if player.alive:
        player_pos = (player.rect.centerx, player.rect.centery)

    
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


    # Flip the screen
    pygame.display.flip()

pygame.quit()
