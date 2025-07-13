import math, random, os
import pygame
from settings import load_txt_settings

#Global variables
FPS = 60
WIDTH = 720
HEIGHT = 640
MODE = 0
SOUND = 0
_BASE_HP = 1
_BASE_STR = 20
_BASE_SPD = 8

pygame.mixer.init()
settings = load_txt_settings()
# Raw values (0–100)
master_vol_raw = settings.get("Âm lượng tổng", 100) / 100
sfx_vol_raw = settings.get("Âm lượng âm thanh", 100) / 100
bgm_vol_raw = settings.get("Âm lượng nhạc", 100) / 100

# Final volumes scaled by master volume
sfx_vol = sfx_vol_raw * master_vol_raw
bgm_vol = bgm_vol_raw * master_vol_raw

BGM = None
SFX = None


def load_sfx():
    global SFX
    SFX = sfx(sfx_vol)

def load_bgm():
    global BGM
    BGM = bgms(bgm_vol)

#Keystrokes
def load_controls_from_txt(txt_path="settings.txt"):
    defaults = {
        "Di chuyển lên": "W",
        "Di chuyển xuống": "S",
        "Di chuyển trái": "A",
        "Di chuyển phải": "D",
        "Bắn": "SPACE",
        "Bom": "Z",
        "Giảm tốc": "LEFT SHIFT"
    }

    bindings = {}
    if not os.path.exists(txt_path):
        return {k: pygame.key.key_code(v.lower()) for k, v in defaults.items()}

    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, val = map(str.strip, line.strip().split(":", 1))
                val = val.upper()
                if key in defaults:
                    try:
                        bindings[key] = pygame.key.key_code(val.lower())
                    except:
                        bindings[key] = pygame.key.key_code(defaults[key].lower())
    return bindings


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
        pygame.image.load("./graph/boss04.png").convert_alpha(),
        pygame.Surface((1, 1), pygame.SRCALPHA)
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

def sfx(volume = 1.0):
    sounds = {
        "life" : pygame.mixer.Sound('./sound/extralife.ogg'),
        "power" : pygame.mixer.Sound('./sound/vie.ogg'),
        "phase_change" : pygame.mixer.Sound('./sound/alert_attack.ogg'),
        "select" : pygame.mixer.Sound('./sound/spring.ogg'),
        "upgrade1" : pygame.mixer.Sound('./sound/level_up1.mp3'),
        "upgrade2" : pygame.mixer.Sound('./sound/level_up2.mp3'),
        "enemy_explode" : pygame.mixer.Sound('./sound/explode.ogg'),
        "tp1" : pygame.mixer.Sound('./sound/tp1.mp3'),
        "tp2" : pygame.mixer.Sound('./sound/tp2.mp3'),
        "death1" : pygame.mixer.Sound('./sound/death1.mp3'),
        "death2" : pygame.mixer.Sound('./sound/death2.mp3'),
        "death3" : pygame.mixer.Sound('./sound/death3.mp3'),
        "death4" : pygame.mixer.Sound('./sound/death4.mp3'),
        "turret" : pygame.mixer.Sound('./sound/bow.mp3'),
        "pause" : pygame.mixer.Sound('./sound/pause.mp3'),
        "burst" : pygame.mixer.Sound('./sound/burst.mp3'),
        "bomb_get" : pygame.mixer.Sound('./sound/bomb.mp3'),
        "bomb_use" : pygame.mixer.Sound('./sound/bomb-expl.mp3'),
        "victory1" : pygame.mixer.Sound('./sound/victory.mp3'),
        "victory2" : pygame.mixer.Sound('./sound/victory2.mp3'),
        "defeat" : pygame.mixer.Sound('./sound/defeat.mp3'),
    }
    
    for sound in sounds.values():
        sound.set_volume(volume)
        
    return sounds

def bgms(volume = 1.0):
    bgm = {
        "menu" : "./bgms/background.ogg",
        "lv1" : "./bgms/lv1.ogg",
        "lv2" : "./bgms/lv2.ogg",
        "lv3" : "./bgms/lv3.ogg",
        "lv4" : "./bgms/lv4.ogg",
        "lv5" : "./bgms/lv5.ogg",
        "lv6" : "./bgms/lv6.ogg",
        "lv7" : "./bgms/lv7.ogg",
        "lv8" : "./bgms/lv8.ogg",
        "lv9" : "./bgms/lv9.ogg",
        "lv10" : "./bgms/lv10.ogg",
    }
    pygame.mixer.music.set_volume(volume)
    return bgm

load_sfx()
load_bgm()
    
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
        
        def shoot(self, projectile_group, enemy_group, speed = -10, target_filter = None):
            bullet = HomingProjectile(self.rect.centerx, self.rect.centery,
                                    self.bullet_img, speed, self.owner, enemy_group, target_filter=target_filter)
            bullet.damage_factor = self.damage_factor
            projectile_group.add(bullet)
    def __init__(self, images):
        #Base stats
        super().__init__(_BASE_HP, _BASE_SPD, _BASE_STR)
        self.grace = 5000
        self.life = 3
        self.score = 0
        self.bomb = 3
        self.level = 1
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
        self.death_sound_played = False
        
        #Sub-guns
        sg_img = sidegun()
        sg_proj = sidegun_proj()
        self.left_gun = Ship.SideGun(-20, sg_img[0], sg_proj[0], owner="Ship", damage_factor=0.25)
        self.right_gun = Ship.SideGun(20, sg_img[1], sg_proj[1], owner="Ship", damage_factor=0.25)
        self.enemy_group_ref = None
        
        #Controls
        self.controls = load_controls_from_txt()

    def grace_period(self):
        self.invincible = True
        self.invincible_start = pygame.time.get_ticks()
        self.image = self.skin[1]

    def shoot(self, projectile_group):
        proj = ally_proj()
        lvl = int(self.level)
        if lvl > 4:
            lvl = 4
        img_idx = min(lvl - 1, len(proj) - 1)
        img = proj[img_idx]
        filter = None
        if pygame.time.get_ticks() - self.last_shot > self.shooting_cd:
            if lvl == 1:
                projectile = Projectile(
                    self.rect.centerx, self.rect.centery - 20,
                    img, -10, owner = "Ship")
                projectile_group.add(projectile)
            elif lvl == 2:
                projectile = Projectile(
                self.rect.centerx, self.rect.centery - 20,
                img, -10, owner="Ship")
                projectile_group.add(projectile)
                
                if random.random() < 0.5:  # 50% chance
                    projectile_left = Projectile(
                        self.rect.centerx - 15, self.rect.centery - 20,
                        img, -10, owner="Ship")
                    projectile_right = Projectile(
                        self.rect.centerx + 15, self.rect.centery - 20,
                        img, -10, owner="Ship")
                    projectile_group.add(projectile_left, projectile_right)
            elif lvl >= 3:
                projectile_center = Projectile(
                    self.rect.centerx, self.rect.centery - 20,
                    img, -10, owner="Ship")
                projectile_left = Projectile(
                    self.rect.centerx - 15, self.rect.centery - 20,
                    img, -10, owner="Ship")
                projectile_right = Projectile(
                    self.rect.centerx + 15, self.rect.centery - 20,
                    img, -10, owner="Ship")
                projectile_group.add(projectile_center, projectile_left, projectile_right)
            
            if self.enemy_group_ref and any(isinstance(e, Boss) and e.alive for e in self.enemy_group_ref):
                def boss_filter(enemy):
                    return isinstance(enemy, Boss)
                filter = boss_filter
            else:
                filter = None
                # self.left_gun.shoot(projectile_group, self.enemy_group_ref, target_filter=boss_filter)
                # self.right_gun.shoot(projectile_group, self.enemy_group_ref, target_filter=boss_filter)
            # else:
                # self.left_gun.shoot(projectile_group, self.enemy_group_ref)
                # self.right_gun.shoot(projectile_group, self.enemy_group_ref)
            if lvl == 4:
                #Left gun
                self.left_gun.shoot(projectile_group, self.enemy_group_ref, target_filter=filter)
                # Add angled bullet for left gun
                angled_bullet_left = Projectile(
                    self.left_gun.rect.centerx, self.left_gun.rect.centery,
                    sidegun_proj()[0], -10, -2, owner="Ship")
                projectile_group.add(angled_bullet_left)
                
                #Right gun:
                self.right_gun.shoot(projectile_group, self.enemy_group_ref, target_filter=filter)
                # Add angled bullet for right gun
                angled_bullet = Projectile(
                    self.right_gun.rect.centerx, self.right_gun.rect.centery,
                    sidegun_proj()[1], -10, 2, owner="Ship")
                projectile_group.add(angled_bullet)
                
            else:
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
                if keys[self.controls["Di chuyển trái"]]:
                    if keys[self.controls["Giảm tốc"]]:
                        self.rect.x -= self.speed // 2
                    else:
                        self.rect.x -= self.speed
                    if self.rect.left < 0:
                        self.rect = self.rect.move(WIDTH - 32, 0)
                if keys[self.controls["Di chuyển phải"]]:
                    if keys[self.controls["Giảm tốc"]]:
                        self.rect.x += self.speed // 2
                    else:
                        self.rect.x += self.speed
                    if self.rect.right > WIDTH:
                        self.rect = self.rect.move(-WIDTH + 32, 0)
                if keys[self.controls["Di chuyển lên"]]:
                    if keys[self.controls["Giảm tốc"]]:
                        self.rect.y -= self.speed // 2
                    else:
                        self.rect.y -= self.speed
                    if self.rect.top <= 40:
                        self.rect.top = 40
                if keys[self.controls["Di chuyển xuống"]]:
                    if keys[self.controls["Giảm tốc"]]:
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

            if not self.death_sound_played:
                d_r = random.choice(["death1", "death2", "death3", "death4"])
                if SFX and d_r in SFX:
                    SFX[d_r].play()
                self.death_sound_played = True
            
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
                    self.death_sound_played = False
                    
                    self.hitbox = pygame.Rect(0,0,10,10)
                    self.hitbox.centerx = self.rect.centerx
                    self.hitbox.centery = self.rect.centery + 6
                else:
                    self.kill()
                    print("L")
                    self.death_animation_done = True
            return
    
    def update_strength(self):
        """Update strength based on the integer part of the level."""
        level = int(self.level)
        if level == 1:
            self.strength = 20
        elif level == 2:
            self.strength = 30
        elif level == 3:
            self.strength = 45
        elif level >= 4:
            self.strength = 60
        
    def bombs(self, enemy_proj, enemies, now):
        if self.bomb > 0:
            SFX["bomb_use"].play()
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
    IMAGE_MAP = {
        "sniper": 9,
        "neutral": 10,
        "zigzag": 11,
        "spiral": 12,
        "crazy": 2
    }
    def __init__(self, health_point, speed, points, behavior):
        super().__init__(health_point, speed, 10)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, 80)
        self.points = points
        self.spawn_time = pygame.time.get_ticks()
        self.leave = 20000
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
        
        if self.behavior != "boss":
            all_enemy_images = enemy_img()
            behavior_index = Enemy.IMAGE_MAP.get(self.behavior, 10)
            image_path = all_enemy_images[behavior_index][0]
            self.image = pygame.image.load(image_path).convert_alpha()

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
            
    def take_damage(self, dmg):
        self.health_point -= dmg
        if self.health_point <= 0 and self.alive:
            self.alive = False
            SFX["enemy_explode"].play()
    
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
        
        #Phase 1 parameters:
        self.last_spiral_shot = 0
        self.last_lane_shot = 0
        self.angle = 0
        self.spiral_dir = 1
        self.phase_start_time = 0
        
        #Phase 2 parameters:
        self.phase2_state = "spiral"
        self.phase2_timer = 0
        self.phase2_target = self.rect.center  # target pos for moving
        self.wobble_direction = 1  # in __init__
        self.spin_count = 0        # number of times we complete a spin
        
        #Phase 3 parameters:
        self.invincible = False
        self.turret_group = pygame.sprite.Group()
        self.turret_respawn_cooldown = 0
        
        #Phase 4 parameters:
        self.shadow_mode = False
        self.shadow_visible = False
        self.shadow_timer = 0
        self.shadow_anim_index = 0
        self.shadow_anim_time = 0
        self.shadow_anim_delay = 100  # ms per frame
        self.shadow_frames = boss()  # From classes.py boss() function
        self.shadow_burst_fired = False



    def move_and_shoot(self, projectile_group, player_pos=None, player = None):
        now = pygame.time.get_ticks()
          
        if self.current_phase == 1:
            
            #Movement
            x_speed = 2
            y_wave_amplitude = 20
            y_wave_frequency = 0.002  # smaller = slower wave

            self.rect.x += x_speed * self.direction  # self.direction = 1 or -1

            # Bounce off screen edges
            if self.rect.right >= WIDTH or self.rect.left <= 0:
                self.direction *= -1
            # Vertical wave (sinusoidal)
            self.rect.y = 100 + y_wave_amplitude * math.sin(pygame.time.get_ticks() * y_wave_frequency)
            
            #Shootings
            if now - self.last_lane_shot > 1000:
                bspeed = 4
                spread = 10
                for angle in range(0, 360, spread):
                    rad = math.radians(angle)
                    dx = math.cos(rad) * bspeed
                    dy = math.sin(rad) * bspeed
                    bullet = Projectile(self.rect.centerx, self.rect.centery,  # center of boss
                                        enemy_proj()[0], dy, dx, "boss")
                    projectile_group.add(bullet)
                self.last_lane_shot = now

        elif self.current_phase == 2:
            #Shootings
            if self.phase2_state == "spiral":
                # Spiral duration
                if now - self.phase2_timer > 3000:
                    self.phase2_state = "move"
                    self.phase2_timer = now
                    # Pick a new random target position
                    margin = 80
                    self.phase2_target = (random.randint(margin, WIDTH - margin),
                                        random.randint(margin, HEIGHT // 2))
                else:
                    # Spiral bullets
                    if now - self.last_spiral_shot > 5:
                        speed = 5
                        rad = math.radians(self.angle)
                        dx = math.cos(rad) * speed
                        dy = math.sin(rad) * speed
                        bullet = Projectile(self.rect.centerx, self.rect.centery,
                                            enemy_proj()[1], dy, dx, "boss", wobble_dir=self.wobble_direction)
                        projectile_group.add(bullet)

                        # Opposite spiral bullet
                        rad_opposite = math.radians(self.angle + 180)
                        dx2 = math.cos(rad_opposite) * speed
                        dy2 = math.sin(rad_opposite) * speed
                        bullet2 = Projectile(self.rect.centerx, self.rect.centery,
                                            enemy_proj()[1], dy2, dx2, "boss", wobble_dir=self.wobble_direction)
                        projectile_group.add(bullet2)

                        self.angle += 10 * self.spiral_dir
                        self.last_spiral_shot = now

                        # Check if a full spin completed (360°)
                        if self.angle % 360 == 0:
                            self.wobble_direction *= -1  # flip direction

                    # Switch spiral direction every 3 seconds
                    if now - self.phase_start_time > 3000:
                        self.spiral_dir *= -1
                        self.phase_start_time = now
            #Movement
            elif self.phase2_state == "move":
                # Move toward the target
                target_x, target_y = self.phase2_target
                speed = 6
                dx = target_x - self.rect.centerx
                dy = target_y - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist > speed:
                    move_x = speed * dx / dist
                    move_y = speed * dy / dist
                    self.rect.centerx += int(move_x)
                    self.rect.centery += int(move_y)
                else:
                    self.rect.center = self.phase2_target
                    self.phase2_state = "spiral"
                    self.phase2_timer = now

        elif self.current_phase == 3:
            class Turret(Enemy):
                def __init__(self, x, y, health, target_ref, projectile_group):
                    super().__init__(health_point=health, speed=0, points=0, behavior="turret")
                    self.image = pygame.transform.scale(pygame.image.load("./imgs/space14.png").convert_alpha(), (32, 32))
                    self.rect = self.image.get_rect(center=(x, y))

                    self.target_ref = target_ref  # Player reference
                    self.projectile_group = projectile_group

                    # Overwrite Enemy's shooting values for turret-specific timing
                    self.shoot_cd = 3000  # 1 bullet per 3 second
                    self.last_shot = pygame.time.get_ticks()

                def update(self):
                    # No movement — but if needed, add idle floating/wobble here
                    self.shoot(self.projectile_group)

                def shoot(self, projectile_group, player_pos=None):
                    now = pygame.time.get_ticks()
                    if now - self.last_shot > self.shoot_cd:
                        # Aim at the player
                        if self.target_ref and self.target_ref.alive:
                            px, py = self.target_ref.rect.center
                            dx = px - self.rect.centerx
                            dy = py - self.rect.centery
                            dist = math.hypot(dx, dy)
                            dx /= dist
                            dy /= dist

                            bullet = HomingProjectile(self.rect.centerx, self.rect.centery, 
                                                      enemy_proj()[1], 3, "turret", [player])
                            projectile_group.add(bullet)
                            SFX["turret"].play()
                        self.last_shot = now
                        
            # If all turrets destroyed → make boss vulnerable, start cooldown
            if not self.turret_group and self.invincible:
                self.invincible = False
                self.turret_respawn_cooldown = now + 20000  # 20 seconds of vulnerability

            if not self.turret_group and now > self.turret_respawn_cooldown:
                self.invincible = True
                self.rect = self.image.get_rect(center=(WIDTH // 2, 100))
                turret_y = self.rect.centery + 20
                turret_positions = [
                    (self.rect.centerx + 80, turret_y),
                    (self.rect.centerx + 160, turret_y),
                    (self.rect.centerx - 80, turret_y),
                    (self.rect.centerx - 160, turret_y),
                ]
                for pos in turret_positions:
                    turret = Turret(pos[0], pos[1], self.max_hp * 0.1, player, projectile_group)
                    self.turret_group.add(turret)

            # Update turrets
            self.turret_group.update()
            
        elif self.current_phase == 4:
            now = pygame.time.get_ticks()
            
            # Trigger Shadow Mode if not already started
            if not self.shadow_mode and self.health_point <= self.max_hp / 2:
                self.shadow_mode = True
                self.shadow_visible = False
                self.shadow_timer = now
                self.shadow_anim_index = 0
                self.image = self.shadow_frames[0]  # disappear frame

            # Shadow Mode active
            if self.shadow_mode:
                # CASE 1: Disappear → wait 3s → reappear near player
                if not self.shadow_visible and now - self.shadow_timer > 3000:
                    px, py = player.rect.center
                    angle = random.uniform(0, 2 * math.pi)
                    radius = random.randint(60, 90)
                    offset_x = int(math.cos(angle) * radius)
                    offset_y = int(math.sin(angle) * radius)
                    self.rect.center = (px + offset_x, py + offset_y)
                    self.shadow_visible = True
                    self.shadow_burst_fired = False
                    self.shadow_timer = now
                    self.shadow_anim_index = len(self.shadow_frames) - 1

                if self.shadow_visible and not self.shadow_burst_fired and now - self.shadow_timer > 500:
                    self.fire_burst(projectile_group)
                    self.shadow_burst_fired = True

                # CASE 2: Visible → burst → vanish again
                elif self.shadow_visible and now - self.shadow_timer > 3000:
                    self.fire_burst(projectile_group)
                    self.shadow_visible = False
                    self.shadow_timer = now
                    self.shadow_anim_index = 0
                    self.image = self.shadow_frames[0]  # disappear

                # Animate appearance/disappearance
                if now - self.shadow_anim_time > self.shadow_anim_delay:
                    self.shadow_anim_time = now
                    if not self.shadow_visible:
                        if self.shadow_anim_index < len(self.shadow_frames) - 1:
                            self.shadow_anim_index += 1
                        self.image = self.shadow_frames[self.shadow_anim_index]
                    else:
                        if self.shadow_anim_index > 0:
                            self.shadow_anim_index -= 1
                        self.image = self.shadow_frames[self.shadow_anim_index]
                        
    def fire_burst(self, projectile_group):
        num_bullets = 36
        speed = 4
        for i in range(num_bullets):
            angle = i * (360 / num_bullets)
            rad = math.radians(angle)
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            bullet = Projectile(self.rect.centerx, self.rect.centery,
                                enemy_proj()[0], dy, dx, "boss")
            projectile_group.add(bullet)
        SFX["burst"].play()

    # Override take_damage to change phase on death
    def take_damage(self, dmg):
        if not self.alive or self.shadow_mode and not self.shadow_visible:
            return
        if not self.invincible:
            self.health_point -= dmg
            if self.health_point <= 0:
                self.current_phase += 1
                if self.current_phase > self.max_phases:
                    self.alive = False
                else:
                    SFX["phase_change"].play()
                    self.health_point = self.phase_health

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, direction_y, direction_x=0, owner="enemy", wobble_dir=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = direction_x
        self.dy = direction_y
        self.owner = owner
        self.mask = pygame.mask.from_surface(self.image)
        self.wobble_dir = wobble_dir
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        time_alive = (pygame.time.get_ticks() - self.spawn_time) / 1000  # seconds

        # Wobble: sin wave left/right movement
        wobble_amplitude = 1.5  # adjust wave strength
        if self.wobble_dir != 0:
            offset = math.sin(time_alive * 10) * self.wobble_dir * wobble_amplitude
            self.rect.x += offset
        
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Remove if off screen
        if (self.rect.bottom < 0 or self.rect.top > HEIGHT or
            self.rect.right < 0 or self.rect.left > WIDTH):
            self.kill()

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
    
    def generate_loot(enemy, player):
        """
        Generate loot drops based on enemy type.
        - Small enemies: 30% chance for shield, 30% chance for upgrade.
        - Bosses: Guaranteed bomb and life, 20% chance for gift.
        Returns a list of Loot objects.
        """
        loot_list = []
        loot_images = loot()
        x, y = enemy.rect.centerx, enemy.rect.centery
        r = random.random()

        if isinstance(enemy, Boss):
            # Guaranteed bomb and life
            loot_list.append(Loot(x + random.randint(-20, 20), y + random.randint(-20, 20), loot_images[3], 3))  # Bomb
            loot_list.append(Loot(x + random.randint(-20, 20), y + random.randint(-20, 20), loot_images[4], 4))  # Life
            # 20% chance for gift
            if random.random() < 0.2:
                loot_list.append(Loot(x + random.randint(-20, 20), y + random.randint(-20, 20), loot_images[0], 0))  # Gift
        else:
            if player.level >= 4:
                if r < 0.2:
                    loot_list.append(Loot(x, y, loot_images[2], 2))  # Shield
                elif r < 0.4:
                    loot_list.append(Loot(x, y, loot_images[3], 3))  # Bomb
                elif r < 0.55:
                    loot_list.append(Loot(x, y, loot_images[4], 4))  # Life
            else:
                if r < 0.5:
                    loot_list.append(Loot(x, y, loot_images[1], 1))  # Power
                elif r < 0.7:
                    loot_list.append(Loot(x, y, loot_images[2], 2))  # Shield
                elif r < 0.9:
                    loot_list.append(Loot(x, y, loot_images[3], 3))  # Bomb
                else:
                    loot_list.append(Loot(x, y, loot_images[4], 4))  # Life
                
                

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
            SFX["power"].play()
            player.level = min(player.level + 0.25, 4)
        elif self.loot_type == 2:  # Shield
            player.invincible = True
            player.grace_period()
        elif self.loot_type == 3:  # Bomb
            SFX["bomb_get"].play()
            player.bomb = min(player.bomb + 1, player.max_bomb)
        elif self.loot_type == 4:  # Food
            SFX["life"].play()
            player.life = min(player.life + 1, player.max_life)
        if int(player.level) > prev_lvl:
            SFX[random.choice(["upgrade1", "upgrade2"])].play()
            player.update_strength()
            
class HomingProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, owner, enemy_group, target_filter = None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.owner = owner
        self.enemy_group = enemy_group
        self.mask = pygame.mask.from_surface(self.image)
        self.damage_factor = 1.0
        self.target_filter = target_filter

    def update(self):
        nearest_enemy = None
        min_distance = float('inf')
        
        # Find the nearest enemy
        for enemy in self.enemy_group:
            if not enemy.alive:
                continue
            if self.target_filter and not self.target_filter(enemy):
                continue  # Skip if filter says "no"

            distance = math.hypot(
                self.rect.centerx - enemy.rect.centerx,
                self.rect.centery - enemy.rect.centery
            )
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        
        # Only home if an enemy is within 300 pixels
        if nearest_enemy and min_distance <= 300:
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