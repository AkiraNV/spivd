# enemy.py
import pygame
import math
import random
from classes import Enemy, Projectile, WIDTH, HEIGHT, enemy_proj, HomingProjectile, SFX

class NeutralEnemy(Enemy):
    def __init__(self, hp, speed, points):
        super().__init__(hp, speed, points, "neutral")
        self.shoot_cd = 100
        self.shoot_duration = 500
        self.shoot_interval = 3000

    def shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()
        self.rect.x += int(5 * math.sin(now / 200))

        if now - self.last_shot > self.shoot_interval:
            self.last_shot = now
            self.shoot_start = now

        if now - self.shoot_start < self.shoot_duration:
            if now - self.last_bullet_time > self.shoot_cd:
                angles = [-15, 0, 15]
                for angle in angles:
                    rad = math.radians(angle)
                    dx = self.bullet_speed * math.sin(rad)
                    dy = self.bullet_speed * math.cos(rad)
                    proj = Projectile(self.rect.centerx, self.rect.centery, enemy_proj()[0], dy, dx, owner="enemy")
                    projectile_group.add(proj)


class SniperEnemy(Enemy):
    def __init__(self, hp, speed, points):
        super().__init__(hp, speed, points, "sniper")
        self.aim_cd = random.randint(1000, 3000)
        self.last_aim = 0

    def shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()

        if now - self.last_aim > self.aim_cd and player_pos:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            dist = max(1, math.hypot(dx, dy))
            dx /= dist
            dy /= dist

            proj = Projectile(self.rect.centerx, self.rect.centery, enemy_proj()[1], dy * 8, dx * 8, owner="enemy")
            projectile_group.add(proj)
            self.last_aim = now
            self.aim_cd = random.randint(1000, 3000)


class ZigZagEnemy(Enemy):
    def __init__(self, hp, speed, points):
        super().__init__(hp, speed, points, "zigzag")
        self.horizontal = 1
        self.vertical = 1
        self.shoot_start = pygame.time.get_ticks()
        self.shooting = True
        self.last_bullet_time = 0
        
    def move(self):
        # Movement
        self.rect.y += (self.speed * self.horizontal) // 1.5
        if self.rect.top <= 60 or self.rect.bottom >= HEIGHT // 4:
            self.horizontal *= -1

        self.rect.x += (self.speed * self.vertical) // 1.5
        if self.rect.left <= 5 or self.rect.right >= WIDTH - 5:
            self.vertical *= -1

    def shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()
        if not self.shot:
                if now - self.shoot_start < 3000:
                    if now - self.last_shot > 100:
                        proj = enemy_proj()[3]
                        dy = self.bullet_speed
                        bullet = Projectile(self.rect.centerx, self.rect.centery,
                                            proj, dy, owner="enemy")
                        projectile_group.add(bullet)
                        self.last_shot = now
                else:
                    self.shot = True



class SpiralEnemy(Enemy):
    @staticmethod
    def _calculate_vectors():
        vectors = []
        bullet_speed = 4  #Bullet speed
        for i in range(0, 360, 20):
            rad = math.radians(i)
            dx = bullet_speed * math.cos(rad)
            dy = bullet_speed * math.sin(rad)
            vectors.append((dx, dy))
        return vectors
    PRECALCULATED_VECTORS = _calculate_vectors()

    def __init__(self, hp, speed, points):
        super().__init__(hp, speed, points, "spiral")
        self.angle = 0
        self.last_bullet_time = 0  # Add this!

    def move(self):
        self.angle += 0.1
        radius = 50
        self.rect.x = WIDTH // 2 + math.cos(self.angle) * radius
        self.rect.y = 100 + math.sin(self.angle) * radius
        self.rect.clamp_ip(pygame.Rect(0, 65, WIDTH, HEIGHT))

    def shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()

        # Trigger a new shooting window
        if now - self.last_shot > self.shoot_interval:
            self.last_shot = now
            self.shoot_start = now

        # Fire bullets during the shooting window
        if now - self.shoot_start < self.shoot_duration:
            if now - self.last_bullet_time > self.shoot_cd:
                proj_img = enemy_proj()[2]
                
                # Vẫn sử dụng thuộc tính của lớp đã được tính toán sẵn
                for dx, dy in SpiralEnemy.PRECALCULATED_VECTORS:
                    bullet = Projectile(self.rect.centerx, self.rect.centery,
                                        proj_img, dy, dx, owner="enemy")
                    projectile_group.add(bullet)
                
                self.last_bullet_time = now

class CrazyEnemy(Enemy):
    def __init__(self, hp, speed, points, target = None):
        super().__init__(hp, speed, points, "crazy")
        self.shoot_cd = 2000  # Shoot every 500ms
        self.last_bullet_time = 0
        self.target = target  # To store reference to player for homing

    def shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()
        if now - self.last_bullet_time > self.shoot_cd and self.target and self.target.alive:
            # Shoot homing bullet toward player
            bullet = HomingProjectile(
                self.rect.centerx, self.rect.centery,
                enemy_proj()[4],
                speed=8,
                owner="enemy",
                enemy_group=[self.target]  # No enemy group needed for enemy projectiles
            )
            projectile_group.add(bullet)
            self.last_bullet_time = now

    def take_damage(self, damage):
        # 30% chance to teleport and avoid damage
        if random.random() < 0.3:
            # Teleport to a new random position within screen bounds
            margin = 80
            self.rect.center = (
                random.randint(margin, WIDTH - margin),
                random.randint(margin, HEIGHT // 3)
            )
            if SFX:
                tp_sound = random.choice(["tp1", "tp2"])
                if tp_sound in SFX:
                    SFX[tp_sound].play()
            return  # No damage taken
        # Otherwise, take damage normally
        super().take_damage(damage)
