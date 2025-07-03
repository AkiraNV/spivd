import pygame
import random
from classes import Enemy, WIDTH

LEVEL_DATA = {
    1: {
        'waves': [
            [  # Wave 1
                {'behavior': 'sniper', 'count': 2, 'hp': 18, 'speed': 1, 'points': 5},
            ],
            [  # Wave 2
                {'behavior': 'neutral', 'count': 2, 'hp': 22, 'speed': 1, 'points': 7},
            ]
        ],
        'boss': {'behavior': 'neutral', 'hp': 40, 'speed': 1, 'points': 20},
        'spawn_y_range': (60, 120)
    },
    2: {
        'waves': [
            [
                {'behavior': 'neutral', 'count': 3, 'hp': 22, 'speed': 1, 'points': 7},
            ],
            [
                {'behavior': 'sniper', 'count': 1, 'hp': 28, 'speed': 1, 'points': 12},
                {'behavior': 'neutral', 'count': 1, 'hp': 25, 'speed': 2, 'points': 10},
            ]
        ],
        'boss': {'behavior': 'sniper', 'hp': 55, 'speed': 1, 'points': 30},
        'spawn_y_range': (60, 130)
    },
    3: {
        'waves': [
            [
                {'behavior': 'sniper', 'count': 2, 'hp': 30, 'speed': 1, 'points': 12},
            ],
            [
                {'behavior': 'neutral', 'count': 2, 'hp': 32, 'speed': 2, 'points': 14},
            ]
        ],
        'boss': {'behavior': 'sniper', 'hp': 70, 'speed': 2, 'points': 40},
        'spawn_y_range': (60, 140)
    },
    4: {
        'waves': [
            [
                {'behavior': 'sniper', 'count': 2, 'hp': 36, 'speed': 2, 'points': 16},
                {'behavior': 'neutral', 'count': 1, 'hp': 36, 'speed': 2, 'points': 16},
            ],
            [
                {'behavior': 'zigzag', 'count': 1, 'hp': 38, 'speed': 2, 'points': 18},
                {'behavior': 'neutral', 'count': 1, 'hp': 38, 'speed': 2, 'points': 18},
            ]
        ],
        'boss': {'behavior': 'zigzag', 'hp': 90, 'speed': 2, 'points': 60},
        'spawn_y_range': (60, 150)
    },
    5: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 1, 'hp': 40, 'speed': 2, 'points': 20},
                {'behavior': 'sniper', 'count': 2, 'hp': 40, 'speed': 2, 'points': 20},
            ],
            [
                {'behavior': 'zigzag', 'count': 2, 'hp': 44, 'speed': 3, 'points': 22},
            ]
        ],
        'boss': {'behavior': 'spiral', 'hp': 110, 'speed': 3, 'points': 80},
        'spawn_y_range': (50, 160)
    },
    6: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 2, 'hp': 48, 'speed': 3, 'points': 25},
            ],
            [
                {'behavior': 'zigzag', 'count': 2, 'hp': 52, 'speed': 3, 'points': 28},
            ]
        ],
        'boss': {'behavior': 'crazy', 'hp': 140, 'speed': 3, 'points': 110},
        'spawn_y_range': (50, 170)
    },
    7: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 2, 'hp': 56, 'speed': 3, 'points': 30},
                {'behavior': 'sniper', 'count': 1, 'hp': 56, 'speed': 3, 'points': 30},
            ],
            [
                {'behavior': 'zigzag', 'count': 2, 'hp': 60, 'speed': 4, 'points': 34},
            ]
        ],
        'boss': {'behavior': 'crazy', 'hp': 180, 'speed': 4, 'points': 140},
        'spawn_y_range': (50, 180)
    },
    8: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 3, 'hp': 64, 'speed': 4, 'points': 36},
            ],
            [
                {'behavior': 'zigzag', 'count': 3, 'hp': 68, 'speed': 4, 'points': 40},
            ]
        ],
        'boss': {'behavior': 'crazy', 'hp': 230, 'speed': 4, 'points': 180},
        'spawn_y_range': (50, 200)
    },
    9: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 3, 'hp': 72, 'speed': 4, 'points': 44},
                {'behavior': 'sniper', 'count': 1, 'hp': 72, 'speed': 4, 'points': 44},
            ],
            [
                {'behavior': 'zigzag', 'count': 3, 'hp': 78, 'speed': 5, 'points': 50},
            ]
        ],
        'boss': {'behavior': 'crazy', 'hp': 300, 'speed': 5, 'points': 250},
        'spawn_y_range': (50, 220)
    },
    10: {
        'waves': [
            [
                {'behavior': 'spiral', 'count': 4, 'hp': 90, 'speed': 5, 'points': 60},
                {'behavior': 'sniper', 'count': 2, 'hp': 90, 'speed': 5, 'points': 60},
            ],
            [
                {'behavior': 'zigzag', 'count': 4, 'hp': 100, 'speed': 6, 'points': 70},
            ]
        ],
        'boss': {'behavior': 'crazy', 'hp': 400, 'speed': 6, 'points': 400},
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
            enemy = Enemy(
                health_point=spec['hp'],
                speed=spec['speed'],
                points=spec['points'],
                behavior=spec['behavior']
            )
            x = random.randint(32, WIDTH - 32)
            y = random.randint(min_y, max_y)
            enemy.rect.topleft = (x, y)
            all_sprites_group.add(enemy)
            enemies_group.add(enemy)
    return True

def spawn_boss_for_level(level_number, all_sprites_group, enemies_group):
    if level_number not in LEVEL_DATA or 'boss' not in LEVEL_DATA[level_number]:
        return False
    boss_info = LEVEL_DATA[level_number]['boss']
    boss = Enemy(
        health_point=boss_info['hp'],
        speed=boss_info['speed'],
        points=boss_info['points'],
        behavior=boss_info['behavior']
    )
    boss.rect.topleft = (WIDTH // 2, 60)
    all_sprites_group.add(boss)
    enemies_group.add(boss)
    return True