import pygame
import random
from classes import WIDTH, Boss
from enemy import NeutralEnemy, SniperEnemy, ZigZagEnemy, SpiralEnemy, CrazyEnemy


LEVEL_DATA = {
    1: {
        'waves': [
            [{'behavior': 'spiral', 'count': 2, 'hp_range': (200, 220), 'speed_range': (1, 2)}],
            [
                {'behavior': 'neutral', 'count': 1, 'hp_range': (210, 240), 'speed_range': (2, 3)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (230, 250), 'speed_range': (1, 2)}
            ],
        ],
        'spawn_y_range': (70, 160)
    },
    2: {
        'waves': [
            [
                {'behavior': 'neutral', 'count': 2, 'hp_range': (240, 280), 'speed_range': (2, 3)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (250, 290), 'speed_range': (2, 3)}
            ],
            [
                {'behavior': 'sniper', 'count': 2, 'hp_range': (260, 300), 'speed_range': (2, 3)},
                {'behavior': 'zigzag', 'count': 1, 'hp_range': (280, 320), 'speed_range': (2, 3)}
            ]
        ],
        'spawn_y_range': (70, 130)
    },
    3: {
        'waves': [
            [
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (300, 340), 'speed_range': (3, 4)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (320, 350), 'speed_range': (2, 4)}
            ],
            [
                {'behavior': 'spiral', 'count': 1, 'hp_range': (380, 420), 'speed_range': (2, 3)},
                {'behavior': 'neutral', 'count': 2, 'hp_range': (340, 380), 'speed_range': (3, 4)}
            ]
        ],
        'spawn_y_range': (70, 140)
    },
    4: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 2, 'hp_range': (400, 450), 'speed_range': (3, 4)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (420, 460), 'speed_range': (3, 4)}
            ],
            [
                {'behavior': 'crazy', 'count': 1, 'hp_range': (500, 550), 'speed_range': (3, 4)},
                {'behavior': 'sniper', 'count': 3, 'hp_range': (440, 480), 'speed_range': (3, 5)}
            ]
        ],
        'spawn_y_range': (70, 150)
    },
    # Cấp 5: CrazyEnemy được tách ra wave riêng và tăng máu
    5: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 3, 'hp_range': (500, 550), 'speed_range': (3, 4)}
            ],
            [
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (540, 600), 'speed_range': (4, 5)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (550, 610), 'speed_range': (4, 6)}
            ],
            [
                {'behavior': 'crazy', 'count': 1, 'hp_range': (1000, 1150), 'speed_range': (4, 5)}
            ]
        ],
        'spawn_y_range': (70, 160)
    },
    6: {
        'waves': [
            [
                {'behavior': 'crazy', 'count': 1, 'hp_range': (600, 660), 'speed_range': (4, 6)},
                {'behavior': 'spiral', 'count': 2, 'hp_range': (620, 680), 'speed_range': (4, 5)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (650, 710), 'speed_range': (5, 7)}
            ],
            [
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (640, 700), 'speed_range': (5, 6)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (650, 710), 'speed_range': (5, 7)},
                {'behavior': 'crazy', 'count': 2, 'hp_range': (530, 590), 'speed_range': (4, 5)}
            ],
            [
                {'behavior': 'neutral', 'count': 2, 'hp_range': (630, 680), 'speed_range': (4, 5)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (640, 700), 'speed_range': (5, 6)},
                {'behavior': 'spiral', 'count': 1, 'hp_range': (620, 680), 'speed_range': (4, 5)}
            ]
        ],
        'spawn_y_range': (70, 150)
    },
    7: {
        'waves': [
            [
                {'behavior': 'crazy', 'count': 2, 'hp_range': (700, 770), 'speed_range': (5, 7)},
                {'behavior': 'spiral', 'count': 2, 'hp_range': (720, 790), 'speed_range': (5, 6)},
                {'behavior': 'zigzag', 'count': 1, 'hp_range': (740, 810), 'speed_range': (6, 7)}
            ],
            [
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (740, 810), 'speed_range': (6, 7)},
                {'behavior': 'neutral', 'count': 2, 'hp_range': (750, 820), 'speed_range': (5, 7)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (750, 820), 'speed_range': (6, 7)}
            ],
            [
                {'behavior': 'sniper', 'count': 2, 'hp_range': (750, 820), 'speed_range': (6, 7)},
                {'behavior': 'crazy', 'count': 2, 'hp_range': (700, 770), 'speed_range': (5, 7)},
                {'behavior': 'spiral', 'count': 2, 'hp_range': (720, 790), 'speed_range': (5, 6)}
            ]
        ],
        'spawn_y_range': (70, 160)
    },
    8: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 2, 'hp_range': (800, 880), 'speed_range': (5, 7)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (820, 900), 'speed_range': (6, 8)},
                {'behavior': 'crazy', 'count': 2, 'hp_range': (850, 930), 'speed_range': (6, 8)}
            ],
            [
                {'behavior': 'crazy', 'count': 2, 'hp_range': (850, 930), 'speed_range': (6, 8)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (880, 960), 'speed_range': (6, 8)},
                {'behavior': 'neutral', 'count': 1, 'hp_range': (810, 870), 'speed_range': (5, 7)}
            ],
            [
                {'behavior': 'spiral', 'count': 2, 'hp_range': (830, 900), 'speed_range': (5, 7)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (880, 960), 'speed_range': (6, 8)},
                {'behavior': 'sniper', 'count': 1, 'hp_range': (820, 900), 'speed_range': (6, 8)}
            ]
        ],
        'spawn_y_range': (70, 180)
    },
    9: {
        'waves': [
            [
                {'behavior': 'crazy', 'count': 3, 'hp_range': (900, 990), 'speed_range': (7, 8)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (920, 1010), 'speed_range': (6, 8)},
                {'behavior': 'zigzag', 'count': 1, 'hp_range': (980, 1080), 'speed_range': (7, 9)}
            ],
            [
                {'behavior': 'spiral', 'count': 2, 'hp_range': (950, 1050), 'speed_range': (6, 8)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (980, 1080), 'speed_range': (7, 9)},
                {'behavior': 'crazy', 'count': 2, 'hp_range': (930, 1000), 'speed_range': (7, 8)}
            ],
            [
                {'behavior': 'crazy', 'count': 2, 'hp_range': (930, 1000), 'speed_range': (7, 8)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (980, 1080), 'speed_range': (7, 9)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (920, 1010), 'speed_range': (6, 8)}
            ]
        ],
        'spawn_y_range': (70, 170)
    },
    # Cấp 10: Có Boss cuối
    10: {
        'waves': [
            [
                {'behavior': 'crazy', 'count': 3, 'hp_range': (1100, 1200), 'speed_range': (7, 9)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (920, 1010), 'speed_range': (6, 8)},
                {'behavior': 'spiral', 'count': 1, 'hp_range': (1150, 1250), 'speed_range': (7, 8)}
            ],
            [
                {'behavior': 'spiral', 'count': 2, 'hp_range': (1150, 1250), 'speed_range': (7, 8)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (1200, 1300), 'speed_range': (7, 9)},
                {'behavior': 'crazy', 'count': 2, 'hp_range': (1100, 1200), 'speed_range': (8, 9)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (1150, 1250), 'speed_range': (8, 9)},
            ],
            [ 
                {'behavior': 'crazy', 'count': 3, 'hp_range': (1100, 1200), 'speed_range': (8, 9)},
                {'behavior': 'sniper', 'count': 2, 'hp_range': (1200, 1300), 'speed_range': (7, 9)},
                {'behavior': 'zigzag', 'count': 2, 'hp_range': (1150, 1250), 'speed_range': (8, 9)},
                {'behavior': 'spiral', 'count': 2, 'hp_range': (1150, 1250), 'speed_range': (7, 8)}
            ]
        ],
        'boss': {'hp_range': (7000, 8000), 'speed_range': (5, 7)},
        'spawn_y_range': (70, 150)
    }
}

def spawn_enemies_for_wave(level_number, wave_number, all_sprites_group, enemies_group, player = None):
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
            speed = random.randint(spec['speed_range'][0], spec['speed_range'][1])
            
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
                enemy = CrazyEnemy(hp, speed, points, target = player)
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

# trong file levels.py

def spawn_boss_for_level(level_number, all_sprites_group, enemies_group):
    if level_number not in LEVEL_DATA or 'boss' not in LEVEL_DATA[level_number]:
        return False
    boss_info = LEVEL_DATA[level_number]['boss']
    
    hp = random.randint(boss_info['hp_range'][0], boss_info['hp_range'][1])
    speed = random.randint(boss_info['speed_range'][0], boss_info['speed_range'][1])
    points = int(hp / 20 + speed * 3)

    boss = Boss(
        health_point=hp,
        speed=speed,
        points=points
    )

    all_sprites_group.add(boss)
    enemies_group.add(boss)
    return True