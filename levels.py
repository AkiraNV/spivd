import pygame
import random
from classes import WIDTH, Enemy
from enemy import NeutralEnemy, SniperEnemy, ZigZagEnemy, SpiralEnemy, CrazyEnemy


LEVEL_DATA = {
    1: {
        'waves': [
            [{'behavior': 'spiral', 'count': 1, 'hp_range': (170, 200), 'speed_range': 6}],
            [{'behavior': 'neutral', 'count': 2, 'hp_range': (210, 240), 'speed_range': (1, 2)}],
        ],
        'boss': {'behavior': 'neutral', 'hp_range': (380, 450), 'speed_range': (1, 2)},
        'spawn_y_range': (60, 120)
    },
    2: {
        'waves': [
            [{'behavior': 'neutral', 'count': 3, 'hp_range': (210, 250), 'speed_range': (1, 2)}],
            [
                {'behavior': 'sniper', 'count': 1, 'hp_range': (270, 300), 'speed_range': (1, 3)},
                {'behavior': 'neutral', 'count': 1, 'hp_range': (240, 280), 'speed_range': (2, 3)},
            ]
        ],
        'boss': {'behavior': 'sniper', 'hp_range': (530, 600), 'speed_range': (1, 3)},
        'spawn_y_range': (60, 130)
    },
    3: {
        'waves': [
            [{'behavior': 'sniper', 'count': 2, 'hp_range': (280, 330), 'speed_range': (1, 3)}],
            [{'behavior': 'neutral', 'count': 2, 'hp_range': (300, 350), 'speed_range': (2, 3)}],
        ],
        'boss': {'behavior': 'sniper', 'hp_range': (680, 750), 'speed_range': (2, 4)},
        'spawn_y_range': (60, 140)
    },
    4: {
        'waves': [
            [
                {'behavior': 'sniper', 'count': 2, 'hp_range': (340, 380), 'speed_range': (2, 4)},
                {'behavior': 'neutral', 'count': 1, 'hp_range': (340, 380), 'speed_range': (2, 4)},
            ],
            [
                {'behavior': 'zigzag', 'count': 1, 'hp_range': (360, 400), 'speed_range': (2, 4)},
                {'behavior': 'neutral', 'count': 1, 'hp_range': (360, 400), 'speed_range': (2, 4)},
            ]
        ],
        'boss': {'behavior': 'zigzag', 'hp_range': (870, 950), 'speed_range': (2, 4)},
        'spawn_y_range': (60, 150)
    },
    5: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 1, 'hp_range': (380, 430), 'speed_range': (2, 4)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (380, 430), 'speed_range': (2, 4)},
            ],
            [{'behavior': 'zigzag', 'count': 2, 'hp_range': (420, 470), 'speed_range': (3, 5)}],
        ],
        'boss': {'behavior': 'spiral', 'hp_range': (1000, 1200), 'speed_range': (3, 5)},
        'spawn_y_range': (50, 160)
    },
    6: {
        'waves': [
            [{'behavior': 'spiral', 'count': 2, 'hp_range': (460, 510), 'speed_range': (3, 5)}],
            [{'behavior': 'zigzag', 'count': 2, 'hp_range': (500, 550), 'speed_range': (3, 5)}],
        ],
        'boss': {'behavior': 'crazy', 'hp_range': (1350, 1500), 'speed_range': (3, 5)},
        'spawn_y_range': (50, 170)
    },
    7: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 2, 'hp_range': (540, 600), 'speed_range': (3, 5)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (540, 600), 'speed_range': (3, 5)},
            ],
            [{'behavior': 'zigzag', 'count': 2, 'hp_range': (580, 640), 'speed_range': (4, 6)}],
        ],
        'boss': {'behavior': 'crazy', 'hp_range': (1700, 1900), 'speed_range': (4, 6)},
        'spawn_y_range': (50, 180)
    },
    8: {
        'waves': [
            [{'behavior': 'spiral', 'count': 3, 'hp_range': (620, 680), 'speed_range': (4, 6)}],
            [{'behavior': 'zigzag', 'count': 3, 'hp_range': (660, 720), 'speed_range': (4, 6)}],
        ],
        'boss': {'behavior': 'crazy', 'hp_range': (2200, 2400), 'speed_range': (4, 6)},
        'spawn_y_range': (50, 200)
    },
    9: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 3, 'hp_range': (700, 770), 'speed_range': (4, 6)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (700, 770), 'speed_range': (4, 6)},
            ],
            [{'behavior': 'zigzag', 'count': 3, 'hp_range': (760, 830), 'speed_range': (5, 7)}],
        ],
        'boss': {'behavior': 'crazy', 'hp_range': (2900, 3200), 'speed_range': (5, 7)},
        'spawn_y_range': (50, 220)
    },
    10: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 4, 'hp_range': (850, 950), 'speed_range': (5, 7)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (850, 950), 'speed_range': (5, 7)},
            ],
            [{'behavior': 'zigzag', 'count': 4, 'hp_range': (950, 1050), 'speed_range': (6, 8)}],
        ],
        'boss': {'behavior': 'crazy', 'hp_range': (3800, 4300), 'speed_range': (6, 8)},
        'spawn_y_range': (50, 240)
    },
}

def spawn_enemies_for_wave(level_number, wave_number, all_sprites_group, enemies_group):
    if level_number not in LEVEL_DATA:
        print("Không còn level!")
        return False
    
    level_config = LEVEL_DATA[level_number]
    waves = level_config['waves']
    
    if wave_number >= len(waves):
        print("Không còn wave!")
        return False
        
    enemy_specs = waves[wave_number]
    min_y, max_y = level_config['spawn_y_range']
    
    for spec in enemy_specs:
        for _ in range(spec['count']):
            #Random hp and speed
            hp = random.randint(spec['hp_range'][0], spec['hp_range'][1])
            speed = spec['speed_range']
            
            #Tính points dựa trên HP và Speed
            points = int(hp / 20 + speed * 3)
            
            if spec['behavior'] == 'neutral':
                enemy = NeutralEnemy(hp, speed, points)
            elif spec['behavior'] == 'sniper':
                enemy = SniperEnemy(hp, speed, points)
            elif spec['behavior'] == 'zigzag':
                enemy = ZigZagEnemy(hp, speed, points)
            elif spec['behavior'] == 'spiral':
                enemy = SpiralEnemy(hp, speed, points)
            elif spec['behavior'] == 'crazy':
                enemy = CrazyEnemy(hp, speed, points)
            x = 0
            if spec['behavior'] == 'zigzag':
                x = random.randint(80, WIDTH - 80)
            elif spec['behavior'] == 'spiral':
                x = WIDTH // 2
            else:
                x = random.randint(60, WIDTH - 60)
            y = random.randint(min_y, max_y)
            enemy.rect.topleft = (x, y)
            all_sprites_group.add(enemy)
            enemies_group.add(enemy)
    return True

def spawn_boss_for_level(level_number, all_sprites_group, enemies_group):
    if level_number not in LEVEL_DATA or 'boss' not in LEVEL_DATA[level_number]:
        return False
         
    boss_info = LEVEL_DATA[level_number]['boss']
    
    hp = random.randint(boss_info['hp_range'][0], boss_info['hp_range'][1])
    speed = random.randint(boss_info['speed_range'][0], boss_info['speed_range'][1])
    
    points = int(hp / 20 + speed * 3)
    
    boss = Enemy(
        health_point=hp,
        speed=speed,
        points=points,
        behavior=boss_info['behavior']
    )
    boss.rect.topleft = (WIDTH // 2, 60)
    all_sprites_group.add(boss)
    enemies_group.add(boss)
    return True