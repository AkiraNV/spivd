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

        #Shootings
        self.shooting_cd = 70
        self.last_shot = 0
        self.firing = False
        self.firing_time = 0

        #The ship
        self.skin = images
        self.image = self.skin[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

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

    def grace_period(self):
        self.invincible = True
        self.invincible_start = pygame.time.get_ticks()
        self.image = self.skin[1]

    def shoot(self, projectile_group):
        proj = ally_proj()
        if pygame.time.get_ticks() - self.last_shot > self.shooting_cd:
            img = proj[self.level - 1 if self.level - 1 < len(proj) else len(proj) - 1]
            projectile = Projectile(
                self.rect.centerx, self.rect.top,
                img, -10, owner = "Ship")
            projectile_group.add(projectile)
            self.left_gun.shoot(projectile_group)
            self.right_gun.shoot(projectile_group)
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
            #Movements
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
                if self.rect.top <= 0:
                    self.rect.top = 0
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
        self.rect.center = (WIDTH // 2, 50)
        self.points = points
        self.spawn_time = pygame.time.get_ticks()
        self.leave = 15000
        self.behavior = behavior
        self.shoot_start = pygame.time.get_ticks()
        self.shoot_duration = 500
        self.shoot_cd = 20
        self.last_shot = 0
        self.shot = False

        #Sniper boy
        self.direction = random.choice([-1,1])
        self.last_aim = 0
        self.aim_cd = random.randint(1000, 2000)
        self.sniper_burst_size = 10
        self.sniper_burst_count = 0
        self.sniper_bullet_delay = 30
        self.sniper_last_bullet_time = 0

        #Spiral boy
        self.phase = 0 
        self.angle = 0

        #Zigzag boy 
        self.vertical = 1
        self.horizontal = 1
        self.zigzag_counter = 0

        #Hover boy
        self.hover_start_x = self.rect.x

        #Crazy boy
        self.crazy_counter = 0

    def move_and_shoot(self, projectile_group, player_pos = None):
        now = pygame.time.get_ticks()
        bspd = 2
        if not self.alive:
            return
        if now - self.spawn_time > self.leave:
            self.kill()
            return
        if self.behavior == "neutral":
            self.rect.x += int(10 * math.sin(now / 300))
            if not self.shot:
                if now - self.shoot_start < self.shoot_duration:
                    if now - self.last_shot > self.shoot_cd:
                        angles = [-15, 0, 15]
                        for angle in angles:
                            rad = math.radians(angle)
                            dx = bspd * math.sin(rad)
                            dy = bspd * math.cos(rad)
                            proj = enemy_proj()[0]
                            bullet = Projectile(self.rect.centerx, self.rect.centery,
                                                proj, dy, dx, owner = "enemy")
                            projectile_group.add(bullet)
                        self.last_shot = now
                else:
                    self.shot = True

        elif self.behavior == "sniper":
            self.rect.x += self.speed * self.direction // 1.5

            if self.rect.left < 0:
                self.rect.left = 0
                self.direction *= -1
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.direction *= -1
            
            if not self.shot:
                if now - self.last_aim > self.aim_cd and player_pos:
                    
                    # If we have bullets left in the burst and it's time to shoot
                    if now - self.sniper_last_bullet_time > self.sniper_bullet_delay:
                        # Calculate direction to player
                        dx = player_pos[0] - self.rect.centerx
                        dy = player_pos[1] - self.rect.centery
                        
                        # Normalize direction vector
                        distance = max(1, math.sqrt(dx*dx + dy*dy))
                        dx = dx / distance
                        dy = dy / distance
                        
                        # Create bullet aimed at player
                        proj = enemy_proj()[1]
                        bullet = Projectile(
                            self.rect.centerx, self.rect.centery,
                            proj, dy * 8, dx * 8, owner="enemy"
                        )
                        projectile_group.add(bullet)
                        self.sniper_last_bullet_time = now
                        
                        self.shot = True
                        self.last_aim = now
                        self.aim_cd = random.randint(1000, 3000)
            

        elif self.behavior == "spiral":
            self.angle += 0.1
            radius = 50
            self.rect.x = WIDTH // 2 + math.cos(self.angle) * radius
            self.rect.y = 100 + math.sin(self.angle) * radius
            
            # Shoot circle pattern
            if now - self.shoot_start < self.shoot_duration:
                if now - self.last_shot > 100:
                    for i in range(0, 360, 30):
                        rad = math.radians(i)
                        dx = bspd * math.cos(rad)
                        dy = bspd * math.sin(rad)
                        proj = enemy_proj()[2]
                        bullet = Projectile(self.rect.centerx, self.rect.centery,
                                            proj, dy, dx, owner="enemy")
                        projectile_group.add(bullet)
                    self.last_shot = now
            else:
                self.shot = True
        
        elif self.behavior == "zigzag":
            self.rect.y += (self.speed * self.horizontal) // 1.5

            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT // 5:
                self.horizontal *= -1

            self.rect.x += (self.speed * self.vertical) // 1.5

            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.vertical *= -1
            
            if not self.shot:
                if now - self.shoot_start < 3000:
                    if now - self.last_shot > 100:
                        proj = enemy_proj()[3]
                        dy = bspd
                        bullet = Projectile(self.rect.centerx, self.rect.centery,
                                            proj, dy, owner="enemy")
                        projectile_group.add(bullet)
                        self.last_shot = now
                else:
                    self.shot = True
        
        elif self.behavior == "crazy":
            self.crazy_counter += 1
            if self.crazy_counter % 30 == 0:
                self.rect.x += random.randint(-self.speed * 2, self.speed * 2)
                self.rect.y += random.randint(-self.speed, self.speed)
                
                # Keep in bounds
                if self.rect.left < 0: self.rect.left = 0
                if self.rect.right > WIDTH: self.rect.right = WIDTH
                if self.rect.top < 0: self.rect.top = 0
                if self.rect.bottom > HEIGHT // 2: self.rect.bottom = HEIGHT // 2
            
            # Unpredictable shooting
            if now - self.last_shot > random.randint(50, 300):
                pattern = random.choice(["spray", "burst", "targeted"])
                
                if pattern == "spray":
                    # Spray bullets in wide arc
                    for angle in range(-45, 46, 15):
                        rad = math.radians(angle)
                        dx = bspd * math.sin(rad)
                        dy = bspd * math.cos(rad)
                        proj = enemy_proj()[random.randint(0, 4)]
                        bullet = Projectile(self.rect.centerx, self.rect.centery,
                                            proj, dy, dx, owner="enemy")
                        projectile_group.add(bullet)
                
                elif pattern == "burst":
                    # Quick burst of bullets
                    for _ in range(5):
                        angle = random.randint(-30, 30)
                        rad = math.radians(angle)
                        dx = bspd * math.sin(rad)
                        dy = bspd * math.cos(rad)
                        proj = enemy_proj()[random.randint(0, 4)]
                        bullet = Projectile(self.rect.centerx, self.rect.centery,
                                            proj, dy, dx, owner="enemy")
                        projectile_group.add(bullet)
                
                elif pattern == "targeted":
                    # Aimed shots in player's general direction
                    if player_pos:
                        for _ in range(3):
                            # Calculate approximate direction to player
                            dx = player_pos[0] - self.rect.centerx + random.randint(-50, 50)
                            dy = player_pos[1] - self.rect.centery + random.randint(-50, 50)
                            
                            # Normalize direction vector
                            distance = max(1, math.sqrt(dx*dx + dy*dy))
                            dx = dx / distance
                            dy = dy / distance
                            
                            proj = enemy_proj()[random.randint(0, 4)]
                            bullet = Projectile(self.rect.centerx, self.rect.centery,
                                                proj, dy * 4, dx * 4, owner="enemy")
                            projectile_group.add(bullet)
                
                self.last_shot = now


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
                self.kill()
                print("Boss defeated!")
            else:
                self.health_point = self.phase_health
                print(f"Boss Phase {self.current_phase}")
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
    
    def shoot(self, projectile_group, speed = -10):
        bullet = Projectile(self.rect.centerx, self.rect.top,
                            self.bullet_img, speed, owner=self.owner)
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
