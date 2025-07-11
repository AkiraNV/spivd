# enemy.py
import pygame
import math
import random
from classes import Enemy, Projectile, WIDTH, HEIGHT, enemy_proj

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
    def __init__(self, hp, speed, points):
        super().__init__(hp, speed, points, "spiral")
        self.angle = 0
        self.last_bullet_time = 0  # Add this!

    def move(self):
        self.angle += 0.1
        radius = 50
        self.rect.x = WIDTH // 2 + math.cos(self.angle) * radius
        self.rect.y = 100 + math.sin(self.angle) * radius

    def shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()

        # Trigger a new shooting window
        if now - self.last_shot > self.shoot_interval:
            self.last_shot = now
            self.shoot_start = now

        # Fire bullets during the shooting window
        if now - self.shoot_start < self.shoot_duration * 2:
            if now - self.last_bullet_time > self.shoot_cd:
                for i in range(0, 360, 20):
                    rad = math.radians(i)
                    dx = self.bullet_speed * math.cos(rad)
                    dy = self.bullet_speed * math.sin(rad)
                    proj = enemy_proj()[2]
                    bullet = Projectile(self.rect.centerx, self.rect.centery,
                                        proj, dy, dx, owner="enemy")
                    projectile_group.add(bullet)
                self.last_bullet_time = now


class CrazyEnemy(Enemy):
    def __init__(self, hp, speed, points):
        super().__init__(hp, speed, points, "crazy")
        self.crazy_counter = 0

    def shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()
        self.crazy_counter += 1
        if self.crazy_counter % 30 == 0:
            self.rect.x += random.randint(-self.speed * 2, self.speed * 2)
            self.rect.y += random.randint(-self.speed, self.speed)
            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT // 2))

        if now - self.last_shot > self.shoot_interval:
            self.last_shot = now
            self.shoot_start = now

        if now - self.shoot_start < self.shoot_duration:
            if now - self.shoot_start % 100 < 20:
                pattern = random.choice(["spray", "burst", "targeted"])
                for _ in range(3 if pattern != "burst" else 5):
                    angle = random.randint(-45, 45) if pattern != "targeted" else 0
                    dx = math.sin(math.radians(angle)) * self.bullet_speed
                    dy = math.cos(math.radians(angle)) * self.bullet_speed

                    if pattern == "targeted" and player_pos:
                        px, py = player_pos
                        dx = px - self.rect.centerx + random.randint(-50, 50)
                        dy = py - self.rect.centery + random.randint(-50, 50)
                        dist = max(1, math.hypot(dx, dy))
                        dx /= dist
                        dy /= dist
                        dx *= 4
                        dy *= 4

                    proj = enemy_proj()[random.randint(0, 4)]
                    bullet = Projectile(self.rect.centerx, self.rect.centery, proj, dy, dx, owner="enemy")
                    projectile_group.add(bullet)
