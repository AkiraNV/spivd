import math, random
import pygame

#Global variables
FPS = 60
WIDTH = 720
HEIGHT = 640
MODE = 0
SOUND = 0
_BASE_HP = 1
# _BASE_STR = 10
_BASE_STR = 50
_BASE_SPD = 8

#Storage
def state():
    return [
        pygame.image.load("./imgs/ship.png").convert_alpha(),
        pygame.image.load("./imgs/ship_grace.png").convert_alpha(),
        pygame.image.load("./imgs/ship_shoot.png").convert_alpha(),
        pygame.image.load("./imgs/ship_shoot2.png").convert_alpha(),
        pygame.image.load("./imgs/ship_shoot3.png").convert_alpha(),
        ]

def sidegun():
    return [
        pygame.image.load("./imgs/leftgun.png").convert_alpha(),
        pygame.image.load("./imgs/rightgun.png").convert_alpha(),
    ]
    
def sidegun_proj():
    return [
        pygame.image.load("./imgs/supply05.png").convert_alpha(),
        pygame.image.load("./imgs/supply06.png").convert_alpha(),
    ]

def ally_proj():
    return [
        pygame.image.load("./imgs/supply01.png").convert_alpha(),
        pygame.image.load("./imgs/supply02.png").convert_alpha(),
        pygame.image.load("./imgs/supply03.png").convert_alpha(),
        pygame.image.load("./imgs/supply04.png").convert_alpha(),
    ]

def death():
    return [
        pygame.image.load("./imgs/death1.png").convert_alpha(),
        pygame.image.load("./imgs/death2.png").convert_alpha(),
        pygame.image.load("./imgs/death3.png").convert_alpha(),
        pygame.image.load("./imgs/death4.png").convert_alpha(),
        pygame.image.load("./imgs/death5.png").convert_alpha(),
        pygame.image.load("./imgs/death6.png").convert_alpha(),
        pygame.image.load("./imgs/death7.png").convert_alpha(),
        pygame.image.load("./imgs/death8.png").convert_alpha(),
        pygame.image.load("./imgs/death9.png").convert_alpha(),
        pygame.image.load("./imgs/death10.png").convert_alpha(),
        pygame.image.load("./imgs/death11.png").convert_alpha(),
        pygame.image.load("./imgs/death12.png").convert_alpha(),
        pygame.image.load("./imgs/death13.png").convert_alpha()
    ]

def enemy_img():
    return [
        ["./imgs/space11.png", "./imgs/space12.png", "./imgs/space13.png", "./imgs/space14.png", "./imgs/space15.png"],
        ["./imgs/space21.png", "./imgs/space22.png", "./imgs/space23.png", "./imgs/space24.png", "./imgs/space25.png"],
        ["./imgs/space31.png", "./imgs/space32.png", "./imgs/space33.png", "./imgs/space34.png", "./imgs/space35.png"],
        ["./imgs/space81.png", "./imgs/space82.png", "./imgs/space83.png", "./imgs/space84.png", "./imgs/space85.png"],
        ["./imgs/space71.png", "./imgs/space72.png", "./imgs/space73.png", "./imgs/space74.png", "./imgs/space75.png"],
        ["./imgs/space61.png", "./imgs/space62.png", "./imgs/space63.png", "./imgs/space64.png", "./imgs/space65.png"],
        ["./imgs/space51.png", "./imgs/space52.png", "./imgs/space53.png", "./imgs/space54.png", "./imgs/space55.png"],
        ["./imgs/space91.png", "./imgs/space92.png", "./imgs/space93.png", "./imgs/space94.png", "./imgs/space95.png"],
        ["./imgs/space41.png", "./imgs/space42.png", "./imgs/space43.png", "./imgs/space44.png", "./imgs/space45.png"],
        ["./imgs/space10.1.png", "./imgs/space10.2.png", "./imgs/space10.3.png", "./imgs/space10.4.png", "./imgs/space10.5.png"],
        ["./imgs/space11.1.png", "./imgs/space11.2.png", "./imgs/space11.3.png", "./imgs/space11.4.png", "./imgs/space11.5.png"],
        ["./imgs/space12.1.png", "./imgs/space12.2.png", "./imgs/space12.3.png", "./imgs/space12.4.png", "./imgs/space12.5.png"],
        ["./imgs/space13.1.png", "./imgs/space13.2.png", "./imgs/space13.3.png", "./imgs/space13.4.png", "./imgs/space13.5.png"],
        ["./imgs/space14.1.png", "./imgs/space14.2.png", "./imgs/space14.3.png", "./imgs/space14.4.png", "./imgs/space14.5.png"]
    ]

def enemy_proj():
    return [
        pygame.image.load("./imgs/supply10.png").convert_alpha(),
        pygame.image.load("./imgs/supply20.png").convert_alpha(),
        pygame.image.load("./imgs/supply30.png").convert_alpha(),
        pygame.image.load("./imgs/supply40.png").convert_alpha(),
        pygame.image.load("./imgs/supply50.png").convert_alpha(),
    ]

def boss():
    return [
        pygame.image.load("./graph/boss01.png").convert_alpha(),
        pygame.image.load("./graph/boss02.png").convert_alpha(),
        pygame.image.load("./graph/boss03.png").convert_alpha(),
        pygame.image.load("./graph/boss04.png").convert_alpha()
    ]

def moveset():
    return [
        "neutral", "sniper", "spiral", "zigzag", "hover", "crazy"
    ]

def loot():
    return [
        pygame.image.load("./imgs/gift.png").convert_alpha(),
        pygame.image.load("./imgs/power.png").convert_alpha(),
        pygame.image.load("./imgs/shield.png").convert_alpha(),
        pygame.image.load("./imgs/bomb.png").convert_alpha(),
        pygame.image.load("./imgs/food.png").convert_alpha(),
    ]
    
def icons():
    def resize(path, size = (16, 16)):
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
    
    return {
        "heart_full": resize("./imgs/heart_full.png"),
        "heart_empty": resize("./imgs/heart_empty.png"),
        "bomb": pygame.image.load("./imgs/bomb.png"),
    }    
    
#Classes
class Entity(pygame.sprite.Sprite):
    def __init__(self, health_point, speed, strength):
        super().__init__()
        self.health_point = health_point
        self.strength = strength
        self.speed = speed
        self.alive = True
        self.image = None
        self.rect = None

        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

    def take_damage(self, damage):
        self.health_point -= damage
        if self.health_point < 0:
            self.health_point = 0
            self.alive = False
            return

class Ship(Entity):
    def __init__(self, images):
        #Base stats
        super().__init__(_BASE_HP, _BASE_SPD, _BASE_STR)
        self.grace = 5000
        self.life = 3
        self.score = 0
        self.bomb = 3
        self.level = 2
        self.max_life = 10
        self.max_bomb = 10

        #Shootings
        self.shooting_cd = 70
        self.last_shot = 0
        self.firing = False
        self.firing_time = 0
        self.projectile_group_ref = None
        
        #Bomb
        self.last_bomb_time = 0
        self.bomb_cd = 2000

        #The ship
        self.skin = images
        self.image = self.skin[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50 + 20)

        #Hitbox
        self.hitbox = pygame.Rect(0,0,10,10)
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery + 6

        #Invincibility
        self.invincible = False
        self.invincible_time = 5000
        self.invincible_start = 0

        #Death
        self.dframes = death()
        self.death_timer = 0
        self.dying = False
        
        #Sub-guns
        sg_img = sidegun()
        sg_proj = sidegun_proj()
        self.left_gun = SideGun(-20, sg_img[0], sg_proj[0], owner="Ship", damage_factor=0.5)
        self.right_gun = SideGun(20, sg_img[1], sg_proj[1], owner="Ship", damage_factor=0.5)
        self.enemy_group_ref = None

    def grace_period(self):
        self.invincible = True
        self.invincible_start = pygame.time.get_ticks()
        self.image = self.skin[1]

    def shoot(self, projectile_group):
        proj = ally_proj()
        if pygame.time.get_ticks() - self.last_shot > self.shooting_cd:
            img = proj[int(self.level) - 1 if int(self.level) - 1 < len(proj) else len(proj) - 1]
            projectile = Projectile(
                self.rect.centerx, self.rect.centery - 20,
                img, -10, owner = "Ship")
            projectile_group.add(projectile)
            self.left_gun.shoot(projectile_group, self.enemy_group_ref)
            self.right_gun.shoot(projectile_group, self.enemy_group_ref)
            self.last_shot = pygame.time.get_ticks()

            #Shooting visuals
            self.image = self.skin[2]
            self.firing = True
            self.firing_time = pygame.time.get_ticks()
    
    def update(self):
        if self.alive:
            #Hitbox tweak
            self.hitbox.center = self.rect.center
            self.hitbox.centerx = self.rect.centerx
            self.hitbox.centery = self.rect.centery + 7
            
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            now = pygame.time.get_ticks()

            #Movements
            if mouse_buttons[0]:
                # Move the ship smoothly towards the mouse
                mx, my = mouse_pos
                dx = mx - self.rect.centerx
                dy = my - self.rect.centery
                
                self.shoot(self.projectile_group_ref)

                move_speed = self.speed

                if abs(dx) > move_speed:
                    self.rect.centerx += move_speed if dx > 0 else -move_speed
                elif dx != 0:
                    self.rect.centerx = mx

                if abs(dy) > move_speed:
                    self.rect.centery += move_speed if dy > 0 else -move_speed
                elif dy != 0:
                    self.rect.centery = my
                
                if now - self.last_shot > self.shooting_cd and self.projectile_group_ref:
                    self.shoot(self.projectile_group_ref)
            else:
                if keys[pygame.K_LEFT]:
                    if keys[pygame.K_LSHIFT]:
                        self.rect.x -= self.speed // 2
                    else:
                        self.rect.x -= self.speed
                    if self.rect.left < 0:
                        self.rect = self.rect.move(WIDTH - 32, 0)
                if keys[pygame.K_RIGHT]:
                    if keys[pygame.K_LSHIFT]:
                        self.rect.x += self.speed // 2
                    else:
                        self.rect.x += self.speed
                    if self.rect.right > WIDTH:
                        self.rect = self.rect.move(-WIDTH + 32, 0)
                if keys[pygame.K_UP]:
                    if keys[pygame.K_LSHIFT]:
                        self.rect.y -= self.speed // 2
                    else:
                        self.rect.y -= self.speed
                    if self.rect.top <= 40:
                        self.rect.top = 40
                if keys[pygame.K_DOWN]:
                    if keys[pygame.K_LSHIFT]:
                        self.rect.y += self.speed // 2
                    else:
                        self.rect.y += self.speed
                    if self.rect.bottom > HEIGHT:
                        self.rect.bottom = HEIGHT
            self.left_gun.update(self.rect)
            self.right_gun.update(self.rect)
            #Shootings
            if self.firing and pygame.time.get_ticks() - self.firing_time > 100:
                self.image = self.skin[0]
                self.firing = False

            #Invincibility
            if self.invincible:
                if (pygame.time.get_ticks() // 400) % 2 == 0:
                    self.image = self.skin[1]
                else:
                    self.image = self.skin[0] 
            if self.invincible and pygame.time.get_ticks() - self.invincible_start > self.invincible_time:
                self.invincible = False
                self.image = self.skin[0]
        else:
            self.hitbox.width = 0
            self.hitbox.height = 0
            self.hitbox.topleft = (-100, -100)
            
            tsd = pygame.time.get_ticks() - self.death_timer
            frame_dura = 200
            fridx = tsd // frame_dura
            if fridx < len(self.dframes):
                self.image = self.dframes[fridx]
            else:
                if self.life > 1:
                    self.health_point = 1
                    self.life -= 1
                    self.rect.center = (WIDTH // 2, HEIGHT - 50)
                    self.grace_period()
                    self.alive = True
                    
                    self.hitbox = pygame.Rect(0,0,10,10)
                    self.hitbox.centerx = self.rect.centerx
                    self.hitbox.centery = self.rect.centery + 6
                else:
                    self.kill()
                    print("L")
                    exit()
            return
    
    def update_strength(self):
        """Update strength based on the integer part of the level."""
        level = int(self.level)
        if level == 1:
            self.strength = 10
        elif level == 2:
            self.strength = 20
        elif level == 3:
            self.strength = 35
        elif level >= 4:
            self.strength = 60
        
    def bombs(self, enemy_proj, enemies, now):
        if self.bomb > 0:
            self.bomb -= 1
            self.last_bomb_time = now
        else:
            return
        
        # Clear all enemy bullets
        for proj in list(enemy_proj):
            proj.kill()

        # Damage all alive enemies
        for enemy in enemies:
            if enemy.alive:
                enemy.take_damage(1000)

        # Optional: invincibility
        self.invincible = True
        self.grace_period()
        

    #Override
    def take_damage(self, amount):
        if not self.invincible:
            super().take_damage(amount) #super already have self
            if self.health_point <= 0:
                self.alive = False
                self.death_timer = pygame.time.get_ticks()
                self.dying = True

class Enemy(Entity):
    def __init__(self, health_point, speed, points, behavior):
        super().__init__(health_point, speed, 10)
        self.image = pygame.Surface((32, 32))  # Placeholder for enemy image
        self.image.fill((0, 0, 255))  # Default blue
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 80)
        self.points = points
        self.spawn_time = pygame.time.get_ticks()
        self.leave = 15000
        self.behavior = behavior
        self.shoot_start = pygame.time.get_ticks()
        self.shoot_duration = 500   #Shooting duration
        self.shoot_cd = 50      #Bullet spacing
        self.shoot_interval = 6000  #Shooting cooldown
        self.last_shot = pygame.time.get_ticks()
        self.shot = False
        self.direction = random.choice([-1,1])
        self.bullet_speed = 5
        self.last_bullet_time = 0

    def check_existence(self):
        now = pygame.time.get_ticks()
        if not self.alive:
            return
        if now - self.spawn_time > self.leave:
            self.kill()
            return

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1
            
    
    def shoot(self,projectile_group, player_pos=None):
        proj = Projectile(self.rect.centerx, self.rect.centery, enemy_proj()[0], -self.bullet_speed, owner="enemy")
        projectile_group.add(proj)

class Boss(Enemy):
    def __init__(self, health_point, speed, points):
        super().__init__(health_point, speed, points, "boss")
        self.image = boss()[0]
        self.rect = self.image.get_rect(center=(WIDTH // 2, 100))
        self.max_phases = 4
        self.current_phase = 1
        self.phase_health = health_point  # HP per phase
        self.health_point = self.phase_health
        self.max_hp = self.phase_health * self.max_phases
        self.last_spiral_shot = 0
        self.last_aimed_shot = 0
        self.last_lane_shot = 0
        self.angle = 0
        self.spiral_dir = 1
        self.phase_start_time = 0

    def move_and_shoot(self, projectile_group, player_pos=None):
        now = pygame.time.get_ticks()

        if self.current_phase == 1:
            # Phase 1: Horizontal 8-lane bullets
            if now - self.last_lane_shot > 1000:
                angles = [-28, -20, -12, -4, 4, 12, 20, 28]  # narrower spacing
                for angle in angles:
                    rad = math.radians(angle)
                    dx = math.sin(rad) * 2
                    dy = math.cos(rad) * 2
                    bullet = Projectile(self.rect.centerx, self.rect.bottom,
                                        enemy_proj()[0], dy, dx, "boss")
                    projectile_group.add(bullet)
                self.last_lane_shot = now

        elif self.current_phase == 2:
            # Phase 2: Spiral
            # Direction toggle every few seconds
            if now - self.phase_start_time > 3000:  # toggle every 3 seconds
                self.spiral_dir *= -1
                self.phase_start_time = now

            # Spiral bullets
            if now - self.last_spiral_shot > 100:
                for i in range(0, 360, 60):
                    rad = math.radians(i + self.angle)
                    dx = math.cos(rad) * 3
                    dy = math.sin(rad) * 3
                    bullet = Projectile(self.rect.centerx, self.rect.centery,
                                        enemy_proj()[1], dy, dx, "boss")
                    projectile_group.add(bullet)
                self.angle += 15 * self.spiral_dir
                self.last_spiral_shot = now


        elif self.current_phase == 3:
            # Phase 3: Random aimed
            if player_pos and now - self.last_aimed_shot > 400:
                for _ in range(3):
                    # Choose a random position near the boss
                    rand_x = self.rect.centerx + random.randint(-100, 100)
                    rand_y = self.rect.centery + random.randint(-40, 40)

                    # Direction toward player
                    dx = player_pos[0] - rand_x
                    dy = player_pos[1] - rand_y
                    dist = max(1, math.hypot(dx, dy))
                    dx, dy = dx / dist, dy / dist

                    bullet = Projectile(rand_x, rand_y,
                                        enemy_proj()[2], dy * 5, dx * 5, "boss")
                    projectile_group.add(bullet)
                self.last_aimed_shot = now


        elif self.current_phase == 4:
            # Phase 4: Spiral + Aimed
            if now - self.last_spiral_shot > 100:
                for i in range(0, 360, 60):
                    rad = math.radians(i + self.angle)
                    dx = math.cos(rad) * 3
                    dy = math.sin(rad) * 3
                    bullet = Projectile(self.rect.centerx, self.rect.centery,
                                        enemy_proj()[1], dy, dx, "boss")
                    projectile_group.add(bullet)
                self.angle += 15 * self.spiral_dir
                self.last_spiral_shot = now

            if player_pos and now - self.last_aimed_shot > 300:
                for _ in range(2):
                    dx = player_pos[0] - self.rect.centerx + random.randint(-40, 40)
                    dy = player_pos[1] - self.rect.centery + random.randint(-40, 40)
                    distance = max(1, math.hypot(dx, dy))
                    dx, dy = dx / distance, dy / distance
                    bullet = Projectile(self.rect.centerx, self.rect.centery,
                                        enemy_proj()[3], dy * 5, dx * 5, "boss")
                    projectile_group.add(bullet)
                self.last_aimed_shot = now

    # Override take_damage to change phase on death
    def take_damage(self, dmg):
        print(f"Boss HP before: {self.health_point}")  # ADD THIS
        if not self.alive:
            return

        self.health_point -= dmg
        if self.health_point <= 0:
            self.current_phase += 1
            if self.current_phase > self.max_phases:
                self.alive = False
            else:
                self.health_point = self.phase_health
                self.last_lane_shot = 0
                self.last_spiral_shot = 0
                self.last_aimed_shot = 0


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, direction_y, direction_x=0, owner="enemy"):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = direction_x
        self.dy = direction_y
        self.owner = owner
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Remove if off screen
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()
            
class SideGun:
    def __init__(self, x_off, image, bullet_img, owner = "Ship", damage_factor = 0.5):
        self.x_off = x_off
        self.image = image
        self.bullet_img = bullet_img
        self.owner = owner
        self.rect = self.image.get_rect()
        self.damage_factor = damage_factor
    
    def update(self, ship_rect):
        self.rect.centerx = ship_rect.centerx + self.x_off
        self.rect.centery = ship_rect.centery
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def shoot(self, projectile_group, enemy_group, speed = -10):
        bullet = HomingProjectile(self.rect.centerx, self.rect.centery,
                                  self.bullet_img, speed, self.owner, enemy_group)
        bullet.damage_factor = self.damage_factor
        projectile_group.add(bullet)
        

class Loot(pygame.sprite.Sprite):
    def __init__(self, x, y, image, loot_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = pygame.time.get_ticks()
        self.loot_type = loot_type
    
    def update(self):
        self.rect.y += 1
        if self.rect.top > HEIGHT:
            self.kill()
    
    def generate_loot(enemy):
        """
        Generate loot drops based on enemy type.
        - Small enemies: 30% chance for shield, 30% chance for upgrade.
        - Bosses: Guaranteed bomb and life, 20% chance for gift.
        Returns a list of Loot objects.
        """
        loot_list = []
        loot_images = loot()
        x, y = enemy.rect.centerx, enemy.rect.centery

        if isinstance(enemy, Boss):
            # Guaranteed bomb and life
            loot_list.append(Loot(x + random.randint(-20, 20), y + random.randint(-20, 20), loot_images[3], 3))  # Bomb
            loot_list.append(Loot(x + random.randint(-20, 20), y + random.randint(-20, 20), loot_images[4], 4))  # Life
            # 20% chance for gift
            if random.random() < 0.2:
                loot_list.append(Loot(x + random.randint(-20, 20), y + random.randint(-20, 20), loot_images[0], 0))  # Gift
        else:
            if random.random() < 0.3:
                item = random.randint(1,3)  # 1: Power, 2: Shield, 3: Upgrade
                loot_list.append(Loot(x + random.randint(-20, 20), y + random.randint(-20, 20), loot_images[item], item))

        return loot_list
    
    def effects(self, player):
        """
        Apply the effect of the loot item to the player.
        - Gift (0): +100 score, +1 life, +1 bomb, +1 upgrade
        - Power (1): +1 level (upgrade)
        - Shield (2): Grant invincibility
        - Bomb (3): +1 bomb
        - Food (4): +1 life
        """
        prev_lvl = player.level
        if self.loot_type == 0:  # Gift
            player.score += 100
            player.life = min(player.life + 1, player.max_life)
            player.bomb = min(player.bomb + 1, player.max_bomb)
            player.level = min(player.level + 0.25, 4)
            print(f"Score: {player.score}")
        elif self.loot_type == 1:  # Power
            player.level = min(player.level + 0.25, 4)
        elif self.loot_type == 2:  # Shield
            player.invincible = True
            player.grace_period()
        elif self.loot_type == 3:  # Bomb
            player.bomb = min(player.bomb + 1, player.max_bomb)
        elif self.loot_type == 4:  # Food
            player.life = min(player.life + 1, player.max_life)
        if int(player.level) > prev_lvl:
            player.update_strength()
            
class HomingProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, owner, enemy_group):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.owner = owner
        self.enemy_group = enemy_group
        self.mask = pygame.mask.from_surface(self.image)
        self.damage_factor = 1.0

    def update(self):
        nearest_enemy = None
        min_distance = float('inf')
        
        # Find the nearest enemy
        for enemy in self.enemy_group:
            if enemy.alive:
                distance = math.hypot(
                    self.rect.centerx - enemy.rect.centerx,
                    self.rect.centery - enemy.rect.centery
                )
                if distance < min_distance:
                    min_distance = distance
                    nearest_enemy = enemy
        
        # Only home if an enemy is within 500 pixels
        if nearest_enemy and min_distance <= 500:
            dx = nearest_enemy.rect.centerx - self.rect.centerx
            dy = nearest_enemy.rect.centery - self.rect.centery
            distance = max(1, math.hypot(dx, dy))
            # Normalize and apply speed
            self.rect.x += (dx / distance) * abs(self.speed)  # Use abs to ensure consistent speed
            self.rect.y += (dy / distance) * abs(self.speed)
        else:
            self.rect.y += self.speed  # Move straight if no enemies or too far
        
        # Remove if off-screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
