#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# 
# PYTHON > 2.6 | WINDOWS TESTED | LINUX TESTED 
# Author of the present code: Deregnaucourt Maxime  space.max@free.fr   
#                                                                     
# Thank a lot to:                           
# Maya and Gabriel for their artistic talent
# Pygame's team
# http://www.universalrsoundbank.com/ for the sounds
# http://www.1001freefonts.com/retro-fonts.php for the fonts
# Josmiley for all tools and modules
#
# HELP KEY USED
# LEFT, RIGHT, SPACE FOR SHOOT, B FOR BOMB, P FOR PAUSE
# Q FOR QUIT MENU / ESCAPE FOR QUIT THE GAME
################################################################################

import pygame, sys, random, os, datetime, math
from pygame.locals import *
from platform import system
from main import slidemenu
from generic import generic
from include import mycolors
from include import words
OS = system().upper()
random.seed()

#_______________________________________________________________________________
# Global variables

FPS = 50
MODE = 0
LANG = 1  # 1 English, 0 French
SOUND = 0.1 # 0 -> 1
#_______________________________________________________________________________
class Game:
    def __init__(self, width=640, height=480):
        pygame.init()

        # Dimensions of the game surface
        self.width = width
        self.height = height
        self.size = width, height
        self.mode = 0  # Used to toggle fullscreen
        self.set_screen()

        pygame.mixer.set_num_channels(30)

        ########################################################################
        # Sounds
        ########################################################################
        self.sound_enemy_cry = pygame.mixer.Sound("./sound/sprite.ogg")
        self.sound_enemy_attack = pygame.mixer.Sound("./sound/alert_attack.ogg")
        self.sound_enemy_explosion = pygame.mixer.Sound("./sound/explode.ogg")
        self.sound_boss_hit = pygame.mixer.Sound("./sound/expl1.ogg")
        self.sound_boss_cry = pygame.mixer.Sound("./sound/boss_cry.ogg")
        self.sound_life = pygame.mixer.Sound("./sound/vie.ogg")
        self.sound_bomb = pygame.mixer.Sound("./sound/bombe.ogg")
        self.sound_power = pygame.mixer.Sound("./sound/shot2.ogg")
        self.sound_shield = pygame.mixer.Sound("./sound/shield.ogg")
        self.sound_alert = pygame.mixer.Sound("./sound/alert.ogg")
        self.sound_ship_explosion = pygame.mixer.Sound("./sound/select_choose.ogg")
        self.sound_extra_life = pygame.mixer.Sound("./sound/extralife.ogg")

        all_sounds = [self.sound_enemy_cry, self.sound_enemy_attack, self.sound_enemy_explosion, self.sound_boss_hit, 
                      self.sound_boss_cry, self.sound_life, self.sound_bomb, self.sound_power, self.sound_shield, self.sound_alert, 
                      self.sound_ship_explosion, self.sound_extra_life]
        
        for sound in all_sounds:
            sound.set_volume(SOUND)

        ########################################################################
        # Images
        ########################################################################
        # Array of PNG image paths for 13 levels, 5 images per sprite
        self.png = 14 * [5 * [""]]
        self.png[0] = ["./graph/space11.png", "./graph/space12.png", "./graph/space13.png", "./graph/space14.png", "./graph/space15.png"]
        self.png[1] = ["./graph/space21.png", "./graph/space22.png", "./graph/space23.png", "./graph/space24.png", "./graph/space25.png"]
        self.png[2] = ["./graph/space31.png", "./graph/space32.png", "./graph/space33.png", "./graph/space34.png", "./graph/space35.png"]
        self.png[3] = ["./graph/space81.png", "./graph/space82.png", "./graph/space83.png", "./graph/space84.png", "./graph/space85.png"]
        self.png[4] = ["./graph/space71.png", "./graph/space72.png", "./graph/space73.png", "./graph/space74.png", "./graph/space75.png"]
        self.png[5] = ["./graph/space61.png", "./graph/space62.png", "./graph/space63.png", "./graph/space64.png", "./graph/space65.png"]
        self.png[6] = ["./graph/space51.png", "./graph/space52.png", "./graph/space53.png", "./graph/space54.png", "./graph/space55.png"]
        self.png[7] = ["./graph/space91.png", "./graph/space92.png", "./graph/space93.png", "./graph/space94.png", "./graph/space95.png"]
        self.png[8] = ["./graph/space41.png", "./graph/space42.png", "./graph/space43.png", "./graph/space44.png", "./graph/space45.png"]
        self.png[9] = ["./graph/space10.1.png", "./graph/space10.2.png", "./graph/space10.3.png", "./graph/space10.4.png", "./graph/space10.5.png"]
        self.png[10] = ["./graph/space11.1.png", "./graph/space11.2.png", "./graph/space11.3.png", "./graph/space11.4.png", "./graph/space11.5.png"]
        self.png[11] = ["./graph/space12.1.png", "./graph/space12.2.png", "./graph/space12.3.png", "./graph/space12.4.png", "./graph/space12.5.png"]
        self.png[12] = ["./graph/space13.1.png", "./graph/space13.2.png", "./graph/space13.3.png", "./graph/space13.4.png", "./graph/space13.5.png"]
        self.png[13] = ["./graph/space14.1.png", "./graph/space14.2.png", "./graph/space14.3.png", "./graph/space14.4.png", "./graph/space14.5.png"]

        # Array of loaded PNG images for enemy sprites
        self.png2 = []
        i = 0
        while i < len(self.png):
            self.pngs = 5 * [pygame.Surface]
            for j in range(5):
                self.pngs[j] = pygame.image.load(self.png[i][j]).convert_alpha()
            self.png2.append(self.pngs)
            i += 1

        # Array of images for enemy explosion
        self.enemy_explosion = [pygame.Surface] * 5
        i = 1
        while i < 6:
            path = "./graph/alien_expl" + str(i) + ".png"
            self.enemy_explosion[i-1] = pygame.image.load(path).convert_alpha()
            i += 1

        # Load ship projectiles
        self.projectile01 = pygame.image.load("./graph/munition01.png").convert_alpha()
        self.projectile02 = pygame.image.load("./graph/munition02.png").convert_alpha()
        self.projectile03 = pygame.image.load("./graph/munition03.png").convert_alpha()
        self.projectile04 = pygame.image.load("./graph/munition04.png").convert_alpha()
        self.projectile05 = pygame.image.load("./graph/munition05.png").convert_alpha()
        self.projectile06 = pygame.image.load("./graph/munition06.png").convert_alpha()

        # Load enemy bombs
        self.enemy_bomb10 = pygame.image.load("./graph/munition10.png").convert_alpha()
        self.enemy_bomb20 = pygame.image.load("./graph/munition20.png").convert_alpha()
        self.enemy_bomb30 = pygame.image.load("./graph/munition30.png").convert_alpha()
        self.enemy_bomb40 = pygame.image.load("./graph/munition40.png").convert_alpha()
        self.enemy_bomb50 = pygame.image.load("./graph/munition50.png").convert_alpha()

        # Load boss images
        self.boss = [pygame.Surface] * 5
        self.boss[0] = pygame.image.load("./graph/boss01.png").convert_alpha()
        self.boss[1] = pygame.image.load("./graph/boss02.png").convert_alpha()
        self.boss[2] = pygame.image.load("./graph/boss03.png").convert_alpha()
        self.boss[3] = pygame.image.load("./graph/boss04.png").convert_alpha()

        # Load ship images
        self.ship01 = pygame.image.load("./graph/vaisseau01.png").convert_alpha()
        self.ship02 = pygame.image.load("./graph/vaisseau02.png").convert_alpha()
        self.ship03 = pygame.image.load("./graph/vaisseau03.png").convert_alpha()
        self.ship04 = pygame.image.load("./graph/vaisseau04.png").convert_alpha()
        self.ship05 = pygame.image.load("./graph/vaisseau05.png").convert_alpha()
        self.ship06 = pygame.image.load("./graph/vaisseau06.png").convert_alpha()
        self.ship07 = pygame.image.load("./graph/leftgun.png").convert_alpha()
        self.ship08 = pygame.image.load("./graph/rightgun.png").convert_alpha()
        self.ship09 = pygame.image.load("./graph/vaisseau09.png").convert_alpha()

        # Load ship explosion images
        self.ship_explosion = [pygame.Surface] * 12
        i = 1
        while i < 13:
            path = "./graph/vaisseau-expl" + str(i) + ".png"
            self.ship_explosion[i-1] = pygame.image.load(path).convert_alpha()
            i += 1

        # Array of trap explosion images
        self.trap_explosion = [pygame.Surface] * 7
        i = 1
        while i < 8:
            path = "./graph/piege_expl" + str(i) + ".png"
            self.trap_explosion[i-1] = pygame.image.load(path).convert_alpha()
            i += 1

        # LuckyDrops image
        self.luckydrop_img = pygame.image.load("./graph/nepomuk.png").convert_alpha()

        # Backgrounds
        self.bg = pygame.image.load("./graph/fond.png").convert_alpha()
        self.bgRect = self.bg.get_rect()
        self.bg2 = pygame.image.load("./graph/fond2.png").convert_alpha()
        self.bgRect2 = self.bg2.get_rect()
        self.bgscroll = pygame.image.load("./graph/scroll.png").convert_alpha()
        self.optionScroll = 0

        # Various images
        self.powerup = pygame.image.load("./graph/cadeau.png").convert_alpha()
        self.bomb = pygame.image.load("./graph/bombe.png").convert_alpha()
        self.power = pygame.image.load("./graph/power.png").convert_alpha()
        self.trap = pygame.image.load("./graph/piege.png").convert_alpha()
        self.shield = pygame.image.load("./graph/shield.png").convert_alpha()
        self.boss_bomb01 = pygame.image.load("./graph/bombe_boss01.png").convert_alpha()
        self.boss_bomb02 = pygame.image.load("./graph/bombe_boss02.png").convert_alpha()
        self.invincibility = pygame.image.load("./graph/vaisseau09.png").convert_alpha()
        self.galaxy = pygame.image.load("./graph/galaxie.png").convert_alpha()
        self.menu_choice = pygame.image.load("./graph/maya2.png").convert_alpha()
        self.menu_choice_rect = self.menu_choice.get_rect()
        self.menu_choice_rect = self.menu_choice_rect.move(460, 258)

        # Sprite groups
        self.all_enemies = Enemy.AllEnemies()
        self.all_extra_enemies = Enemy.AllExtraEnemies()
        self.all_enemy_bombs = Enemy.AllEnemyBombs()
        self.all_projectiles = Ship.AllProjectiles()
        self.all_secondary_projectiles = Ship.AllProjectiles(is_secondary=True)
        self.all_powerups = Enemy.AllPowerUps()
        self.all_weapons = Ship.AllWeapons()
        self.all_bosses = Boss.AllBosses()
        self.all_polygons = Polygon.AllPolygons()

        # Game variables
        self.highscore = []
        self.lives = 3
        self.level = 1
        self.score = 0
        self.extra_bombs = 10
        self.num_extra_bombs = 10
        self.extra_bomb_value = 10
        self.extra_life = 0

        # Clocks
        self.clock = pygame.time.Clock()
        self.clock_shield = pygame.time.Clock()
        self.clock_power = pygame.time.Clock()
        self.time_power = 0

        self.highscore_load()
        pygame.mouse.set_visible(False)

    def set_screen(self, color=(0, 0, 0)):
        # Define the main surface
        self.color = color
        self.surface = pygame.display.set_mode(self.size, MODE)
        pygame.display.set_caption('Space Max')

    def play_sound(self, sound, loop=0):
        try:
            channel = pygame.mixer.find_channel(force=True)
            channel.stop()
            channel.set_volume(0.3)
            channel.play(sound, loop)
        except:
            sound.play(loop)

    def toggle(self):
        global MODE
        # Switch between windowed and full screen
        if MODE == 0:
            MODE = FULLSCREEN
        else:
            MODE = 0
        s = self.surface.copy()
        self.surface = pygame.display.set_mode(self.size, MODE)
        self.surface.blit(s, s.get_rect())
        pygame.display.flip()

    ########################################################################
    # Add enemies to the game
    ########################################################################
    def add_enemy(self, num_enemies=0, max_enemies=15):
        self.num_enemies = num_enemies
        self.max_enemies = max_enemies
        if self.num_enemies < self.max_enemies:
            self.num_enemies += 1
        else:
            self.num_enemies = 1

        valy = [44, 64, 96, 128, 160]
        valx = []
        i = 0
        while i <= 480:
            valx.append(int(i))
            i += 32
        i = 0
        while i < self.num_enemies:
            y = random.sample(valy, 1)
            x = random.sample(valx, 1)
            enemy_obj = Enemy(x[0], y[0])
            valx.remove(x[0])
            i += 1

    def update(self, zone):
        self.zone = zone
        pygame.display.update(self.zone)

    def tick_power(self):
        self.clock_power.tick(FPS)
        self.time_power += self.clock_power.get_time()
        if self.time_power > 30000:
            self.time_power = 0
            if self.num_enemies > 5:
                self.luckydrop = LuckyDrops()

    def clear(self):
        self.surface.fill(mycolors.BLACK)

    def empty(self):
        self.all_projectiles.empty()
        self.all_enemy_bombs.empty()
        self.all_enemies.empty()
        pygame.mixer.stop()
        self.num_extra_bombs = 0

    def pause(self):
        pause = 0
        pygame.event.clear(KEYDOWN)
        e = pygame.event.Event(KEYDOWN, key=K_n)
        while pause != 1:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == 112:
                        pause = 1
                    elif e.key == 97 or e.key == 113 or e.key == 27:
                        self.break_high = True
                        pause = 1
            pygame.time.wait(100)

    ########################################################################
    # Highscore handling
    ########################################################################
    def highscore_load(self):
        self.score_file = True
        try:
            file = open("./high.txt", "r")
        except:
            print("Error opening high.txt")
            self.score_file = False
        if self.score_file:
            eof = False
            while not eof:
                line = file.readline()
                line = line[0:-1]
                if line == "":
                    eof = True
                else:
                    self.highscore.append([int(line.split(",")[0]), str(line.split(",")[1])])
            self.highscore.sort(reverse=True)
        else:
            self.highscore.append([0, "Space Max"])

    def highscore_write(self):
        try:
            if self.score_file:
                file = open("./high.txt", "a")
            else:
                file = open("./high.txt", "w")
            self.clear()
            font = pygame.font.Font(None, 24)
            text1 = font.render(words.words[14][LANG], 1, mycolors.GREEN, mycolors.BLACK)
            text1Rect = text1.get_rect()
            text1Rect = text1Rect.move(int((self.width - text1Rect.width) / 2), 100)
            self.surface.blit(text1, text1Rect)
            self.update(text1Rect)

            name = ""
            flag = True
            while flag:
                for e in pygame.event.get():
                    if e.type == KEYDOWN:
                        if e.key >= 97 and e.key <= 122:
                            if len(name) < 8:
                                s = pygame.key.name(e.key)
                                name += s
                                text2 = font.render(name, 1, mycolors.GREEN, mycolors.RED)
                                text2Rect = text2.get_rect()
                                text2Rect = text2Rect.move(text1Rect.right, 100)
                                self.surface.blit(self.bg, text2Rect, text2Rect)
                                self.update(text2Rect)
                                self.surface.blit(text2, text2Rect)
                                self.update(text2Rect)
                        elif e.key == 13:
                            flag = False
                        elif e.key == 8:
                            self.surface.blit(self.bg, text2Rect, text2Rect)
                            name = name[0:len(name)-1]
                            text2 = font.render(name, 1, mycolors.GREEN, mycolors.BLACK)
                            self.update(text2Rect)
                            self.surface.blit(text2, text2Rect)
                            self.update(text2Rect)
                pygame.time.wait(100)
            if len(name) == 0:
                name = "Space Max"
            file.write(str(self.score) + "," + str(name) + "\n")
            file.close()
        except:
            print("Can't open file high.txt")

    def highscore_print(self):
        font = pygame.font.Font(None, 24)
        font2 = pygame.font.Font(None, 14)
        y = 0
        n = 0
        self.break_high = False
        for score_iter in self.highscore:
            if n == 0:
                self.surface.blit(self.bg2, self.bgRect2)
                self.update(self.bgRect2)
            n += 1
            text1 = font.render(str(score_iter[0]) + "  " + str(score_iter[1]), 1, mycolors.YELLOW, mycolors.BLACK)
            textpos = text1.get_rect()
            y = y + 32
            textpos = textpos.move(int((self.width - textpos.width) / 2), 264 + y)
            self.surface.blit(text1, textpos)
            self.update(textpos)
            if n == 4:
                y = y + 32
                text1 = font2.render("P to see next / Q to Quit high score", 1, mycolors.GREEN, mycolors.BLACK)
                textpos = text1.get_rect()
                textpos = textpos.move(int((self.width - textpos.width) / 2), 264 + y)
                self.surface.blit(text1, textpos)
                self.update(textpos)
                self.pause()
                n = 0
                y = 0
            if self.break_high:
                break

    def option_screen(self):
        self.surface.blit(self.bg, self.bgRect)
        pygame.display.update()
        self.add_enemy(5, 6)
        self.option_display()

    def option_display(self):
        font = pygame.font.Font(None, 16)
        phrase = [words.words[2][LANG], words.words[12][LANG]]
        i = 0
        top = -12
        while i <= 1:
            if i == 0:
                textOption = font.render(phrase[i] + " : " + str(FPS), 1, mycolors.YELLOW, mycolors.BLACK)
            else:
                textOption = font.render(phrase[i], 1, mycolors.GREEN, mycolors.BLACK)
            textOptionRect = textOption.get_rect()
            center = int((self.width - textOptionRect.width) / 2)
            top += textOptionRect.height
            textOptionRect = textOptionRect.move(center, top)
            textOptionRect.width += 50
            self.surface.blit(self.bg, textOptionRect, textOptionRect)
            self.update(textOptionRect)
            self.surface.blit(textOption, textOptionRect)
            self.update(textOptionRect)
            i += 1
        self.clock.tick(FPS)

    def game_over(self):
        '''
        Display the game over message: SpaceMax is stronger than you...
        '''
        font = pygame.font.Font(None, 24)
        self.text1 = font.render(words.words[13][LANG], 1, mycolors.WHITE, mycolors.BLACK)
        self.text1pos = self.text1.get_rect()
        x = (self.width / 2) - (self.text1pos.width / 2)
        y = (self.height / 2) - (self.text1pos.height / 2)
        self.text1pos = self.text1pos.move(x, y)
        self.surface.blit(self.text1, self.text1pos)
        self.update(self.text1pos)
        pygame.time.delay(3000)

#__________________________________________________________________________________________________
class StatusBar(pygame.sprite.Sprite):
    global OS

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = pygame.Surface((32, 8), SRCALPHA)
        self.font = pygame.font.Font(None, 24)
        self.image = pygame.Surface((640, 40))
        self.rect = self.image.get_rect()
        self.extra = [""] * 13
        self.timer = -1
        pygame.time.set_timer(USEREVENT + 1, 300)
        self.ind = 0

    def update(self):
        self.text1 = self.font.render(words.words[6][LANG] + str(game.level) + "  ", 1, mycolors.BLUE_LIGHT, mycolors.BLACK)
        self.textpos1 = self.text1.get_rect()
        self.image.blit(self.text1, self.textpos1)

        self.text2 = self.font.render(words.words[7][LANG] + str(game.lives) + "  ", 1, mycolors.WHITE, mycolors.BLACK)
        self.textpos2 = self.text2.get_rect()
        self.textpos2 = self.textpos2.move(130, 0)
        self.image.blit(self.text2, self.textpos2)

        self.text3 = self.font.render(words.words[8][LANG] + str(game.extra_bombs) + "  ", 1, mycolors.YELLOW, mycolors.BLACK)
        self.textpos3 = self.text3.get_rect()
        self.textpos3 = self.textpos3.move(260, 0)
        self.image.blit(self.text3, self.textpos3)

        try:
            self.text4 = self.font.render(words.words[9][LANG] + str(ship.power) + "  ", 1, mycolors.GREEN, mycolors.BLACK)
        except:
            self.text4 = self.font.render(words.words[9][LANG], 1, mycolors.GREEN, mycolors.BLACK)
        self.textpos4 = self.text4.get_rect()
        self.textpos4 = self.textpos4.move(390, 0)
        self.image.blit(self.text4, self.textpos4)

        self.text5 = self.font.render(words.words[10][LANG] + str(game.score) + "  ", 1, mycolors.RED, mycolors.BLACK)
        self.textpos5 = self.text5.get_rect()
        self.textpos5 = self.textpos5.move(520, 0)
        self.image.blit(self.text5, self.textpos5)

        self.text6 = self.font.render(words.words[11][LANG], 1, mycolors.GREEN, mycolors.BLACK)
        self.textpos6 = self.text6.get_rect()
        self.textpos6.top = 21
        self.image.blit(self.text6, self.textpos6)

        self.shield_rect = self.shield.get_rect()
        self.shield_rect.top = self.textpos6.top + 8
        self.shield_rect.left = self.textpos6.right

        self.ind += 1
        if game.extra_life == 1:
            game.play_sound(game.sound_extra_life, 1)
            self.print_extra_life()
            game.extra_life = 0
            self.timer = 0
            self.clock = pygame.time.Clock()
            self.timer += self.clock.tick(FPS)

        if self.timer > 5000:
            self.erase_extra_life()
            self.timer = -1
        elif self.timer >= 0:
            self.timer += self.clock.tick(FPS)
            if OS != "WINDOWS":
                for event in pygame.event.get():
                    if event.type == USEREVENT + 1:
                        if self.ind / 2 == self.ind / 2.0:
                            self.erase_extra_life()
                        else:
                            self.print_extra_life()
            else:
                if self.ind / 2 == self.ind / 2.0:
                    self.print_extra_life()

        try:
            if ship.protected <= 2:
                color = mycolors.RED
            elif ship.protected <= 4:
                color = mycolors.ORANGE
            elif ship.protected <= 6:
                color = mycolors.YELLOW
            else:
                color = mycolors.GREEN
            self.shield.fill(mycolors.BLACK)
            self.shield.fill(color, pygame.Rect(0, 0, ship.protected * 4, 8))
        except:
            pass
        self.image.blit(self.shield, self.shield_rect)

    def print_extra_life(self):
        self.extra[0] = self.font.render("E", 1, mycolors.PINK, mycolors.BLACK)
        self.extra[1] = self.font.render("x", 1, mycolors.YELLOW, mycolors.BLACK)
        self.extra[2] = self.font.render("t", 1, mycolors.GREEN, mycolors.BLACK)
        self.extra[3] = self.font.render("r", 1, mycolors.PINK, mycolors.BLACK)
        self.extra[4] = self.font.render("a", 1, mycolors.YELLOW, mycolors.BLACK)
        self.extra[5] = self.font.render(" ", 1, mycolors.BLACK, mycolors.BLACK)
        self.extra[6] = self.font.render("L", 1, mycolors.PINK, mycolors.BLACK)
        self.extra[7] = self.font.render("i", 1, mycolors.YELLOW, mycolors.BLACK)
        self.extra[8] = self.font.render("f", 1, mycolors.GREEN, mycolors.BLACK)
        self.extra[9] = self.font.render("e", 1, mycolors.PINK, mycolors.BLACK)
        self.extra[10] = self.font.render("!", 1, mycolors.YELLOW, mycolors.BLACK)
        self.extra[11] = self.font.render("!", 1, mycolors.GREEN, mycolors.BLACK)
        self.extra[12] = self.font.render("!", 1, mycolors.PINK, mycolors.BLACK)

        start = 140
        for character in self.extra:
            letter_pos = character.get_rect()
            letter_pos = letter_pos.move(start, 21)
            start += letter_pos.width
            self.image.blit(character, letter_pos)

    def erase_extra_life(self):
        blank = self.font.render("Extra Life !!!", 1, mycolors.BLACK, mycolors.BLACK)
        self.image.blit(blank, blank.get_rect().move(140, 21))

#__________________________________________________________________________________________________
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.bgscroll
        self.rect = self.image.get_rect()
        self.y1 = 0
        self.y2 = -self.rect.height
        self.speed = 1

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= self.rect.height:
            self.y1 = self.y2 - self.rect.height
        if self.y2 >= self.rect.height:
            self.y2 = self.y1 - self.rect.height

    def draw(self, surface):
        game.surface.blit(self.image, (0, self.y1))
        game.surface.blit(self.image, (0, self.y2))

#__________________________________________________________________________________________________
class Galaxy(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./graph/galaxie.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = bg.speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 600:
            self.kill()

#__________________________________________________________________________________________________
class Polygon(pygame.sprite.Sprite):

    class AllPolygons(pygame.sprite.RenderUpdates):
        def __init__(self):
            pygame.sprite.RenderUpdates.__init__(self)

    def __init__(self, left=0, top=0):
        pygame.sprite.Sprite.__init__(self)
        game.all_polygons.add(self)
        self.image = pygame.Surface((160, 120))
        self.nb_tuple = random.randint(3, 12)
        self.coordinates = []
        for i in range(self.nb_tuple):
            x = random.randint(0, 160)
            y = random.randint(0, 120)
            self.coordinates.append((x, y))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.polygon(self.image, color, self.coordinates)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.x = self.rect.left
        self.y = self.rect.top

    def update(self):
        self.rect.bottom += 1
        if self.rect.top > 480:
            pol = Polygon(self.x, -120)
            game.all_polygons.add(pol)
            self.kill()

#__________________________________________________________________________________________________
class LuckyDrops(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.luckydrop_img
        self.rect = self.image.get_rect()
        self.lottery = random.randint(0, 1)
        if self.lottery == 0:
            self.rect.left = game.width
            self.direction = -1
        else:
            self.rect.left = 0
            self.direction = 1
        self.rect.top = 96

    def update(self):
        self.rect.left += 2 * self.direction
        if 0 < self.rect.left < game.width:
            game.surface.blit(self.image, self.rect)
            if self.rect.colliderect(ship.rect):
                randomize = random.randint(1, 6)
                if randomize == 1:
                    ship.power += 1
                elif randomize == 2:
                    game.extra_bombs += 3
                elif randomize == 3:
                    game.shield += 1
                elif randomize == 4:
                    game.lives += 1
                elif randomize == 5:
                    if ship.power > 1:
                        ship.power -= 1
                self.rect = None

#__________________________________________________________________________________________________
class Enemy(pygame.sprite.Sprite):

    class AllPowerUps(pygame.sprite.RenderUpdates):
        def __init__(self):
            pygame.sprite.RenderUpdates.__init__(self)

    class AllEnemies(pygame.sprite.RenderUpdates):
        def __init__(self):
            pygame.sprite.RenderUpdates.__init__(self)

    class AllExtraEnemies(pygame.sprite.RenderUpdates):
        def __init__(self):
            pygame.sprite.RenderUpdates.__init__(self)

    class AllEnemyBombs(pygame.sprite.RenderUpdates):
        def __init__(self):
            pygame.sprite.RenderUpdates.__init__(self)

    def __init__(self, x, y, extra=False):
        pygame.sprite.Sprite.__init__(self)
        game.all_enemies.add(self)
        self.extra = extra
        self.explosion_index = 0
        self.exploded = False
        self.grow = 1
        self.time_for_shoot = random.randint(0, 2000)
        self.time_for_shield = random.randint(0, 2000)
        self.invincibility = False

        if not self.extra:
            self.images = game.png2[game.level - 1]
        else:
            self.images = game.png2[13]
            game.play_sound(game.sound_enemy_attack, -1)
            game.all_extra_enemies.add(self)

        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        self.image_index = -1
        self.radius = 32
        self.x = x
        self.y = y
        self.rect.top = self.y
        self.rect.left = self.x

        ########################################################################
        # Enemy characteristics
        # Neutral: Stays on its line
        # Nervous: Moves up and down
        # Aggressive: Can attack the ship
        # Crazy: Makes circles and shoots twice
        # Spiral: Kamikaze
        ########################################################################
        if not self.extra:
            self.behavior = random.sample(["neutral", "slightly nervous", "nervous", "very nervous", "aggressive", "crazy", "spiral", "crazy2"], 1)
        else:
            self.behavior = random.sample(["extra"], 1)

        if self.behavior[0] == "crazy" and (self.y < 96 or self.x < 64 or self.x > 576):
            self.behavior[0] = "aggressive"
        if self.behavior[0] == "spiral" and (self.y < 96 or self.x < 64 or self.x > 576):
            self.behavior[0] = "aggressive"

        self.powerup = False
        self.powerup_type = 0
        lottery = random.randint(0, 250)

        if game.level < 4:
            if lottery == 10:
                self.powerup = True
                self.powerup_type = 2
        elif 3 < game.level < 8:
            if lottery in [10, 100]:
                self.powerup = True
                self.powerup_type = 2
        else:
            if lottery in [10, 100, 200]:
                self.powerup = True
                self.powerup_type = 2

        if lottery == 17:
            self.powerup = True
            self.powerup_type = 0
        elif lottery in [9, 3, 21]:
            self.powerup = True
            self.powerup_type = 1
        elif 50 <= lottery <= 60:
            self.powerup = True
            self.powerup_type = 3
        elif 60 < lottery <= 63:
            self.powerup = True
            self.powerup_type = 4
        elif lottery > 245:
            self.powerup = True
            self.powerup_type = 5

        self.hits = 0
        self.direction_x = random.sample([-1, 1], 1)[0]
        self.direction_y = 0

    def update(self, step=4):
        self.time_for_shoot += game.clock.get_time()
        self.time_for_shield += game.clock_shield.get_time()

        if len(game.all_extra_enemies) == 0:
            game.sound_enemy_attack.stop()

        if self.behavior[0] != "crazy":
            if game.level in [1, 6]:
                bomb_type = 10
            elif game.level in [2, 7]:
                bomb_type = 20
            elif game.level in [3, 8, 11]:
                bomb_type = 30
            elif game.level in [5, 9, 12]:
                bomb_type = 40
            elif game.level in [4, 10, 13]:
                bomb_type = 50
        else:
            bomb_type = random.sample([10, 20, 30, 40, 50], 1)[0]

        if self.time_for_shoot > (5000 - game.level * 200) and game.level < 7 and self.behavior[0] != "crazy":
            self.time_for_shoot = 0
            bomb = EnemyBomb(bomb_type, self.rect)
            game.all_enemy_bombs.add(bomb)
        elif self.time_for_shoot > 3000 and 7 <= game.level < 10 and self.behavior[0] != "crazy":
            self.time_for_shoot = 0
            bomb = EnemyBomb(bomb_type, self.rect)
            game.all_enemy_bombs.add(bomb)
        elif self.time_for_shoot > 3000 and (game.level >= 10 or self.behavior[0] in ["crazy", "crazy2"]):
            self.time_for_shoot = 0
            bomb = EnemyBomb(bomb_type, self.rect)
            game.all_enemy_bombs.add(bomb)
            self.tictac = 0
            self.laps = pygame.time.Clock()
            self.laps.tick(FPS)
        try:
            self.tictac += self.laps.get_time()
            if self.tictac > 200:
                bomb = EnemyBomb(bomb_type, self.rect)
                game.all_enemy_bombs.add(bomb)
                self.tictac = 0
                self.laps = None
        except:
            pass

        if 7000 < self.time_for_shield < 9000:
            pygame.draw.circle(game.surface, mycolors.WHITE, (self.rect.left + 16, self.rect.top + 16), 32, 1)
            self.invincibility = True
        elif self.time_for_shield > 9000:
            self.time_for_shield = 0
            self.invincibility = False

        self.step = step
        if self.image_index < len(self.images) - 1:
            self.image_index += 1
            self.image = self.images[self.image_index]
        else:
            self.image_index = -1

        if self.rect.right >= game.width:
            self.direction_x = -1
        elif self.rect.left <= 0:
            self.direction_x = 1

        if self.behavior[0] == "slightly nervous":
            if self.rect.top <= self.y:
                self.direction_y = 1
            elif self.rect.top >= self.y + 16:
                self.direction_y = -1
        elif self.behavior[0] == "nervous":
            if self.rect.top <= self.y:
                self.direction_y = 1
            elif self.rect.top >= self.y + 32:
                self.direction_y = -1
        elif self.behavior[0] == "very nervous":
            if self.rect.top <= self.y:
                self.direction_y = 1
            elif self.rect.top >= 224:
                self.direction_y = -1
        elif self.behavior[0] == "aggressive":
            if self.rect.top <= self.y:
                self.direction_y = 1
            elif self.rect.top >= 448:
                self.direction_y = -1
        elif self.behavior[0] == "extra":
            if self.rect.top < 478:
                if game.level < 10:
                    self.rect.top += 2
                else:
                    self.rect.top += 4
            else:
                self.rect.top = self.y
            diff = math.fabs(self.rect.left - ship.rect.left)
            if self.rect.left <= ship.rect.left:
                if diff > 4:
                    self.rect.left += 4
                else:
                    self.rect.left += diff
            elif self.rect.left > ship.rect.left:
                if diff > 4:
                    self.rect.left -= 4
                else:
                    self.rect.left -= diff

        if self.behavior[0] not in ["crazy", "spiral", "extra"]:
            self.rect = self.rect.move(step * self.direction_x, self.direction_y)

        if self.behavior[0] in ["crazy", "crazy2"]:
            self.cx = self.radius * math.cos(self.radius)
            self.cy = self.radius * math.sin(self.radius)
            self.rect.left = self.x + self.cx
            self.rect.top = self.y + self.cy
            if self.radius < 100.0 and 44 < self.rect.top < 448 and 32 < self.rect.left < 608:
                self.radius += 0.1
            else:
                self.radius = 1

            if self.behavior[0] == "crazy2":
                if self.rect.width <= 16:
                    self.grow = -1
                elif self.rect.width >= 32:
                    self.grow = 1
                self.rect.width -= self.grow
                self.rect.height -= self.grow
                self.rect = self.rect.fit((self.rect.left, self.rect.top, self.rect.width, self.rect.height))
                self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        elif self.behavior[0] == "spiral":
            if self.rect.right >= game.width:
                self.direction_x = -1
            elif self.rect.left <= 0:
                self.direction_x = 1
            self.cx = 64 * math.cos(self.radius)
            self.cy = 64 * math.sin(self.radius)
            self.rect.left = self.x + self.cx * self.direction_x
            self.rect.top = self.y + self.cy
            if self.radius < 6.3:
                self.radius += 0.1
                self.x += 0.5 * self.direction_x
            else:
                self.radius = 0

        if self.rect.colliderect(ship.rect):
            self.hits = 99
            if not self.exploded:
                if not ship.invincibility:
                    ship.explosion()
                self.exploded = True

        if game.num_extra_bombs == 1 or self.hits >= game.level:
            if self.explosion_index < 5:
                self.image = game.enemy_explosion[self.explosion_index]
                self.explosion_index += 1
            else:
                self.explosion_index = -1
                game.score += 1 * game.level
                if self.behavior[0] == "aggressive":
                    game.score += 10
                game.all_enemies.remove(self)
                if self.extra:
                    game.all_extra_enemies.remove(self)
                self.explosion()
                game.play_sound(game.sound_enemy_explosion)
                if len(game.all_enemies) == 0:
                    game.num_extra_bombs = 0
                    game.all_extra_enemies.empty()

    def explosion(self):
        if self.powerup:
            bonus = PowerUp(self.powerup_type, self.rect.top, self.rect.right)
            game.all_powerups.add(bonus)
        if self.behavior[0] == "spiral" and not self.exploded:
            if game.level <= 4:
                n = 2
            elif game.level <= 8:
                n = 3
            else:
                n = 4
            for i in range(n):
                enemy_obj = Enemy(self.x + i * 64, self.y + i * 32, extra=True)
                game.all_enemies.add(enemy_obj)

#__________________________________________________________________________________________________
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type, top, right):
        pygame.sprite.Sprite.__init__(self)
        self.powerup_type = powerup_type
        if self.powerup_type == 0:
            self.image = game.powerup
        elif self.powerup_type == 1:
            self.image = game.bomb
        elif self.powerup_type == 2:
            self.image = game.power
        elif self.powerup_type == 3:
            self.image = game.trap
        elif self.powerup_type == 4:
            self.image = game.shield
        elif self.powerup_type == 5:
            self.image = game.invincibility

        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.right = right

    def update(self):
        if self.powerup_type != 3:
            limit = 480
        else:
            limit = 448

        if self.rect.top < limit:
            self.rect = self.rect.move(0, 4)
        else:
            self.kill()
            if self.powerup_type == 3:
                trap = Trap(self.rect.top, self.rect.right)

        if self.rect.colliderect(ship.rect):
            if self.powerup_type == 0:
                game.lives += 1
                game.play_sound(game.sound_life)
                game.score += 100
            elif self.powerup_type == 1:
                game.extra_bombs += 1
                game.play_sound(game.sound_bomb)
                game.score += 50
            elif self.powerup_type == 2:
                game.score += 25
                ship.power += 1
                game.play_sound(game.sound_power, 5)
                game.score += 25
            elif self.powerup_type == 3 and not ship.invincibility:
                ship.explosion()
            elif self.powerup_type == 4:
                if ship.protected < 8:
                    game.play_sound(game.sound_shield)
                    game.score += 25
                    ship.protected += 1
                else:
                    game.extra_life = 1
                    game.score += 500
                    game.lives += 1
            elif self.powerup_type == 5:
                ship.invisibility_duration = 10000
                ship.invincibility = True
            self.kill()

#__________________________________________________________________________________________________
class Trap(pygame.sprite.Sprite):
    def __init__(self, top, right):
        pygame.sprite.Sprite.__init__(self)
        self.image = game.trap_explosion[0]
        self.rect = game.trap_explosion[0].get_rect()
        self.rect.top = top
        self.rect.right = right + 96
        self.update()
        hit = False
        for image in game.trap_explosion:
            game.surface.blit(image, self.rect)
            game.update(self.rect)
            if self.rect.colliderect(ship.rect):
                hit = True
        if hit:
            ship.protected -= 6
            if ship.protected <= 0:
                self.kill()
                ship.explosion()
            status_bar.shield.fill(mycolors.BLACK)
        pygame.time.delay(30)
        game.play_sound(game.sound_enemy_explosion)

#__________________________________________________________________________________________________
class EnemyBomb(pygame.sprite.Sprite):
    def __init__(self, bomb_type, rect):
        pygame.sprite.Sprite.__init__(self)
        self.bomb_type = bomb_type
        self.image = eval("game.enemy_bomb" + str(bomb_type))
        self.rect = self.image.get_rect()
        x = (rect.width - self.rect.width) / 2
        self.rect = self.rect.move(rect.left + x, rect.top + 32)

    def update(self):
        if game.level < 3:
            step_x = 0
            step_y = 4
        elif 3 <= game.level <= 6:
            step_x = 0
            step_y = 6
        elif 6 <= game.level <= 9:
            step_x = 0
            step_y = 8
        elif 9 <= game.level <= 12:
            step_x = 0
            step_y = 10
        else:
            step_x = 0
            step_y = 12
        self.rect = self.rect.move(step_x, step_y)
        if self.rect.top > 480:
            self.kill()
        if not ship.invincibility:
            if self.rect.colliderect(ship.rect):
                if self.bomb_type == 10:
                    ship.protected -= 1
                elif self.bomb_type == 20:
                    ship.protected -= 2
                elif self.bomb_type == 30:
                    ship.protected -= 3
                elif self.bomb_type == 40:
                    ship.protected -= 4
                elif self.bomb_type == 50:
                    ship.protected -= 5
                self.kill()
                if ship.protected < 0:
                    ship.explosion()
                else:
                    ship.alert()
                    game.play_sound(game.sound_boss_hit)

#__________________________________________________________________________________________________
class Weapon(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if self.type == 1:
            self.image = game.ship07
        else:
            self.image = game.ship08
        self.rect = self.image.get_rect()

    def update(self):
        if self.type == 1:
            self.rect.right = ship.rect.left
        else:
            self.rect.left = ship.rect.right
        self.rect.top = ship.rect.top + 10

#__________________________________________________________________________________________________
class Ship(pygame.sprite.Sprite):

    class AllWeapons(pygame.sprite.RenderUpdates):
        def __init__(self):
            pygame.sprite.RenderUpdates.__init__(self)
            
    class AllProjectiles(pygame.sprite.RenderUpdates):
        def __init__(self, is_secondary = False):
            pygame.sprite.RenderUpdates.__init__(self)
            self.is_secondary = is_secondary            

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.power = 3
        self.protected = 1
        self.ship_explosion = [pygame.Surface] * 12
        self.image = game.ship01
        self.rect = self.image.get_rect()
        self.invisibility_duration = 5000
        self.laps_invisibility = 0
        self.clock_invisibility = pygame.time.Clock()
        self.laps_blink = 0
        self.blink = False
        self.invincibility = False
        self.shoot_cooldown = 50
        self.last_shot = 0

    def pos(self, x, y):
        self.rect = self.rect.move(x, y)

    def reset(self):
        self.rect.top = 0
        self.rect.right = 0
        self.pos(304, 448)
        game.surface.blit(self.image, self.rect)

    def update(self):
        current_time = pygame.time.get_ticks()
        self.clock_invisibility.tick()
        if self.invincibility:
            if self.laps_invisibility < self.invisibility_duration:
                self.laps_invisibility += self.clock_invisibility.get_time()
                if self.laps_blink < 500:
                    self.laps_blink += self.clock_invisibility.get_time()
                else:
                    self.blink = not self.blink
                    self.laps_blink = 0
            else:
                self.laps_invisibility = 0
                self.laps_blink = 0
                self.invincibility = False
                self.blink = False

        if self.blink:
            self.image = game.ship09
        else:
            self.image = game.ship01

        if self.power > 9:
            if len(game.all_weapons) < 2:
                weapon1 = Weapon(1)
                weapon2 = Weapon(2)
                game.all_weapons.add(weapon1)
                game.all_weapons.add(weapon2)
        else:
            game.all_weapons.empty()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot_ship()
        if keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.left -= 8
            else:
                self.rect = self.rect.move(608, 0)
            if keys[pygame.K_SPACE]:
                self.shoot_ship()
        if keys[pygame.K_RIGHT]:
            if self.rect.right < 640:
                self.rect.left += 8
            else:
                self.rect = self.rect.move(-608, 0)
            if keys[pygame.K_SPACE]:
                self.shoot_ship()
        if keys[pygame.K_UP]:
            if self.rect.top > 40:
                self.rect.top -= 8
            if keys[pygame.K_SPACE]:
                self.shoot_ship()
        if keys[pygame.K_DOWN]:
            if self.rect.top < 448:
                self.rect.top += 8
            if keys[pygame.K_SPACE]:
                self.shoot_ship()

    def shoot_ship(self):
        if self.power == 1:
            self.power1(5)
            if self.blink:
                self.image = game.ship09
            else:
                self.image = game.ship02
        elif self.power == 2:
            self.power2(15)
            if self.blink:
                self.image = game.ship09
            else:
                self.image = game.ship03
        elif 3 <= self.power <= 5:
            self.power3(25)
            if self.blink:
                self.image = game.ship09
            else:
                self.image = game.ship04
        elif self.power == 6:
            self.power3(50)
            if self.blink:
                self.image = game.ship09
            else:
                self.image = game.ship04
        elif 7 <= self.power <= 9:
            self.power4(70)
            if self.blink:
                self.image = game.ship09
            else:
                self.image = game.ship04
        elif self.power > 9:
            self.power5(100)

    def power1(self, num_projectiles):
        if len(game.all_projectiles) < num_projectiles:
            projectile = Projectile(1, 14)
            game.all_projectiles.add(projectile)

    def power2(self, num_projectiles):
        if len(game.all_projectiles) < num_projectiles:
            self.power1(num_projectiles)
            projectile = Projectile(3, 4)
            game.all_projectiles.add(projectile)
            projectile = Projectile(3, 24)
            game.all_projectiles.add(projectile)

    def power3(self, num_projectiles):
        if len(game.all_projectiles) < num_projectiles:
            self.power1(num_projectiles)
            self.power2(num_projectiles)
            projectile = Projectile(2, 0)
            game.all_projectiles.add(projectile)
            projectile = Projectile(2, 31)
            game.all_projectiles.add(projectile)

    def power4(self, num_projectiles):
        if len(game.all_projectiles) < num_projectiles:
            self.power1(num_projectiles)
            self.power2(num_projectiles)
            self.power3(num_projectiles)
            projectile = Projectile(4, 0)
            game.all_projectiles.add(projectile)
            projectile = Projectile(4, 31)
            game.all_projectiles.add(projectile)

    def power5(self, num_projectiles):
        if len(game.all_projectiles) < num_projectiles:
            self.power1(num_projectiles)
            self.power2(num_projectiles)
            self.power3(num_projectiles)
            projectile = Projectile(4, 0)
            game.all_projectiles.add(projectile)
            projectile = Projectile(4, 31)
            game.all_projectiles.add(projectile)
            if len(game.all_secondary_projectiles) < 10:
                projectile = Projectile(5, -6)
                game.all_secondary_projectiles.add(projectile)
                projectile = Projectile(6, 37)
                game.all_secondary_projectiles.add(projectile)

    def shoot_bomb(self):
        if game.extra_bombs > 0 and len(game.all_enemies) != 0 and game.num_extra_bombs == 0:
            game.num_extra_bombs = 1
            game.extra_bombs -= 1
        try:
            if game.extra_bombs > 0 and boss.strength > 0 and game.num_extra_bombs == 0:
                game.num_extra_bombs = 1
                game.extra_bombs -= 1
                boss.strength -= 50
                game.play_sound(game.sound_boss_cry)
        except:
            pass

    def explosion(self):
        self.invincibility = True
        game.play_sound(game.sound_ship_explosion)
        if self.protected <= 0:
            self.protected = random.randint(2, 9)
        if self.power > 1:
            self.power -= 1
        else:
            self.power = 1
        game.lives -= 1
        for image in game.ship_explosion:
            game.surface.blit(image, self.rect)
            game.update(self.rect)
            game.play_sound(game.sound_ship_explosion)
            pygame.time.delay(50)

    def alert(self):
        game.surface.blit(game.ship05, self.rect)
        game.play_sound(game.sound_alert)
        game.surface.blit(game.ship06, ship.rect)
        game.play_sound(game.sound_alert)
        pygame.time.delay(50)

#__________________________________________________________________________________________________
class Projectile(pygame.sprite.Sprite):
    def __init__(self, type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.pos = pos
        self.direction = self.direction2 = 1
        if self.type == 1:
            self.image = game.projectile01
        elif self.type == 2:
            self.image = game.projectile02
        elif self.type == 3:
            self.image = game.projectile03
        elif self.type == 4:
            self.image = game.projectile04
        elif self.type == 5:
            self.image = game.projectile05
        elif self.type == 6:
            self.image = game.projectile06
        self.rect = self.image.get_rect()
        self.rect.left = ship.rect.left
        self.rect = self.rect.move(self.pos, ship.rect.top - 2)
        game.surface.blit(self.image, self.rect)

    def update(self):
        if self.type <= 3:
            self.rect = self.rect.move(0, -16)
        elif self.type == 4:
            if self.pos == 0:
                self.rect = self.rect.move(-4 * self.direction, -16)
            else:
                self.rect = self.rect.move(4 * self.direction, -16)
        elif self.type == 5:
            if self.rect.left < 16 or self.rect.right > 624:
                self.direction2 *= -1
                if self.image == game.projectile05:
                    self.image = game.projectile06
                else:
                    self.image = game.projectile05
            self.rect = self.rect.move(-8 * self.direction2, -2)
        elif self.type == 6:
            if self.rect.left < 16 or self.rect.right > 624:
                self.direction2 *= -1
                if self.image == game.projectile05:
                    self.image = game.projectile06
                else:
                    self.image = game.projectile05
            self.rect = self.rect.move(8 * self.direction2, -2)

        if self.rect.top < 32 or self.rect.left < 1 or self.rect.left > game.width:
            self.kill()

        test = pygame.sprite.spritecollide(self, game.all_enemies, 0, collided=None)
        if test:
            for enemy in test:
                if not enemy.invincibility:
                    game.score += 1 * game.level
                    if self.type <= 3:
                        enemy.hits += 1
                        game.play_sound(game.sound_enemy_cry)
                    elif self.type == 4:
                        enemy.hits += 5
                    else:
                        enemy.hits = game.level

        try:
            test = pygame.sprite.spritecollide(self, game.all_bosses, 0, collided=None)
            if test:
                for boss in test:
                    if self.type <= 3:
                        boss.strength -= 1
                    elif self.type == 4:
                        boss.strength -= 2
                    game.play_sound(game.sound_boss_hit)
                    game.score += 10
                    self.kill()
                    if boss.strength <= 0:
                        boss.explosion()
                    elif 5 <= self.type <= 6:
                        boss.strength -= 20
                        game.play_sound(game.sound_boss_hit)
                        game.score += 10
        except:
            pass

#__________________________________________________________________________________________________
class Boss(pygame.sprite.Sprite):

    class AllBosses(pygame.sprite.RenderUpdates):
        def __init__(self):
            pygame.sprite.RenderUpdates.__init__(self)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        game.all_bosses.add(self)
        self.ind = 0
        self.image = game.boss[self.ind]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(random.randint(100, 540), random.randint(80, 260))
        self.strength = game.level * 100
        self.time_for_shoot = 0
        self.hits = 0
        self.direction_x = 4 * random.sample([-1, 1], 1)[0]
        self.direction_y = 4 * random.sample([-1, 1], 1)[0]
        self.grow = 1

    def update(self):
        if self.strength <= 0:
            self.explosion()
        font = pygame.font.Font(None, 16)
        spaces = 32 * " "
        total_boss_strength = 0
        for boss in game.all_bosses:
            total_boss_strength += boss.strength
            self.info = font.render(spaces + "Boss Strength: " + str(total_boss_strength) + spaces, 1, mycolors.YELLOW, mycolors.RED)
            self.infoRect = self.info.get_rect()
            self.infoRect.top = 23
            self.infoRect.left = ((game.width - self.infoRect.width) / 2)

            if self.strength >= 0:
                game.surface.blit(self.info, self.infoRect)

            self.time_for_shoot += game.clock.get_time()

            if self.rect.right >= game.width:
                self.direction_x = -1
            elif self.rect.left <= 0:
                self.direction_x = 1
            if self.rect.top < 50:
                self.direction_y = 1
            elif self.rect.top >= 250:
                self.direction_y = -1
            self.rect = self.rect.move(self.direction_x, self.direction_y)

            if game.num_extra_bombs == 1:
                if self.ind < 3:
                    self.ind += 1
                else:
                    self.ind = 0
            else:
                self.ind = 0
            self.image = game.boss[self.ind]

            if self.rect.width <= 24:
                self.grow = -1
            elif self.rect.width >= 64:
                self.grow = 1

            self.rect.width -= self.grow
            self.rect.height -= self.grow

            if game.level > 3:
                self.rect = self.rect.fit((self.rect.left, self.rect.top, self.rect.width, self.rect.height))
                self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

            game.surface.blit(self.image, self.rect)

            tps = 3000 - (game.level * 50)
            if self.time_for_shoot > tps:
                self.time_for_shoot = 0
                bomb = BossBomb(random.randint(1, 2), self.rect)
                game.all_enemy_bombs.add(bomb)

    def explosion(self):
        game.surface.blit(game.bg, self.rect, self.rect)
        game.score += 50 * game.level
        self.kill()

#__________________________________________________________________________________________________
class BossBomb(pygame.sprite.Sprite):
    def __init__(self, id, rect):
        pygame.sprite.Sprite.__init__(self)
        if game.level <= 8:
            multi = 1
        else:
            multi = 2
        self.id = id
        if self.id == 1:
            self.image = game.boss_bomb01
            self.direction_x = random.randint(-4 * multi, 4 * multi)
        elif self.id == 2:
            self.image = game.boss_bomb02
            self.direction_x = 0
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(rect.left + 16, rect.top + 64)
        game.surface.blit(self.image, self.rect)

    def update(self):
        if self.rect.right >= game.width:
            self.direction_x = -1 * self.direction_x
        elif self.rect.left <= 0:
            self.direction_x = -1 * self.direction_x
        self.rect = self.rect.move(self.direction_x, 4)
        game.surface.blit(self.image, self.rect)
        if self.rect.top > 480 and self.id == 1:
            game.all_enemy_bombs.remove(self)
        elif self.rect.top > 448 and self.id == 2:
            game.all_enemy_bombs.remove(self)
            trap = Trap(self.rect.top, self.rect.right)
        if not ship.invincibility:
            if self.rect.colliderect(ship.rect):
                self.kill()
                ship.explosion()
                ship.invincibility = True

#__________________________________________________________________________________________________
def keyboard():
    pygame.event.get(pygame.KEYDOWN)
    ship.update()
    if pygame.key.get_pressed()[112]:
        game.pause()
    elif pygame.key.get_pressed()[97] or pygame.key.get_pressed()[113]:
        game.lives = 0
    elif pygame.key.get_pressed()[98]:
        ship.shoot_bomb()
    elif pygame.key.get_pressed()[K_ESCAPE]:
        sys.exit()
    elif pygame.key.get_pressed()[K_f]:
        game.toggle()
    else:
        ship.update()

def test_bomb():
    if game.num_extra_bombs == 1 and game.extra_bomb_value > 50:
        game.extra_bomb_value = 0
        game.num_extra_bombs = 0
    elif game.num_extra_bombs == 1:
        game.extra_bomb_value += 1

def environment():
    dir = os.getcwd()
    myscript = sys.argv[0]
    mydir = os.path.dirname(myscript)
    try:
        os.chdir(mydir)
    except:
        pass

def create_polygons():
    for y in range(5):
        for i in range(4):
            pol = Polygon(160 * i, 120 * y)
            game.all_polygons.add(pol)

#__________________________________________________________________________________________________
environment()
game = Game()
global choice

end = False
while not end:
    create_polygons()
    pygame.font.init()
    choice = -1
    while choice != 0:
        pygame.time.Clock().tick(FPS)
        game.surface.blit(game.bg2, game.bgRect2)
        game.update(game.bgRect2)
        joemenu = slidemenu.menu([
            words.words[0][LANG],
            words.words[1][LANG],
            words.words[2][LANG],
            words.words[3][LANG],
            words.words[4][LANG],
            words.words[44][LANG],
            words.words[5][LANG],
        ],
            font1=pygame.font.Font('./slidemenu/BeteNoirNF.ttf', 20),
            font2=pygame.font.Font('./slidemenu/BeteNoirNF.ttf', 25),
            tooltipfont=pygame.font.Font('./slidemenu/Roboto-MediumItalic.ttf', 12),
            color1=(255, 80, 40),
            cursor_img=pygame.image.load("./graph/nepomuk.png"),
            light=9,
            centerx=320,
            y=240
        )
        choice = joemenu[1]

        if choice == 1:
            game.highscore_print()
            if game.break_high:
                choice = -1
            while choice == 1:
                pygame.time.wait(100)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key in [97, 113]:
                            choice = -1

        if choice == 2:
            game.option_screen()
            pygame.key.set_repeat(10, 50)
            ship = Ship()
            while choice == 2:
                game.clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key in [97, 113, 13, K_ESCAPE]:
                            choice = -1
                        elif event.key == 275:
                            FPS += 1
                            game.option_display()
                        elif event.key == 276:
                            FPS -= 1
                            game.option_display()
                game.all_enemies.update()
                game.all_enemies.draw(game.surface)
                game.all_enemy_bombs.update()
                game.all_enemy_bombs.draw(game.surface)
                pygame.display.update()
                game.all_enemy_bombs.clear(game.surface, game.bg)
                game.all_enemies.clear(game.surface, game.bg)
            game.all_enemies.empty()

        if choice == 3:
            scroll = generic.Scrolling([
                (words.words[15][LANG], "c", 24),
                (words.words[16][LANG], "c", 12),
                (words.words[17][LANG], "c", 16),
                (words.words[18][LANG], "c", 14),
                (words.words[19][LANG], "c", 12),
                (words.words[20][LANG], "c", 16),
                (words.words[21][LANG], "c", 14),
                (words.words[22][LANG], "c", 12),
                (words.words[23][LANG], "c", 12),
                (words.words[24][LANG], "c", 16),
                (words.words[25][LANG], "c", 14),
                (words.words[26][LANG], "c", 12),
                (words.words[27][LANG], "c", 16),
                (words.words[28][LANG], "c", 14),
                (words.words[29][LANG], "c", 12),
                (words.words[30][LANG], "c", 12),
                (words.words[31][LANG], "c", 18),
                (words.words[32][LANG], "c", 14),
                (words.words[33][LANG], "c", 12),
                (words.words[34][LANG], "c", 16),
                (words.words[35][LANG], "c", 12),
                (words.words[36][LANG], "c", 12),
                (words.words[37][LANG], "c", 12),
                (words.words[38][LANG], "c", 12),
                (words.words[39][LANG], "c", 12),
                (words.words[40][LANG], "c", 12),
                (words.words[41][LANG], "c", 18),
                (words.words[42][LANG], "c", 14),
                (words.words[43][LANG], "c", 10),
            ],
                (255, 255, 255), game.surface, None)
            scroll.populate()

        if choice == 4:
            if LANG == 0:
                LANG = 1
            else:
                LANG = 0

        if choice == 5:
            choice2 = 0
            while choice2 != 2:
                if choice2 == 0:
                    game.surface.blit(game.bgscroll, game.bgRect)
                    game.update(game.bgRect)
                    game.optionScroll = 0
                elif choice2 == 1:
                    game.surface.fill(mycolors.BLACK)
                    game.all_polygons.draw(game.surface)
                    pygame.display.flip()
                    game.optionScroll = 1
                joemenu2 = slidemenu.menu([
                    words.words[45][LANG],
                    words.words[46][LANG],
                    words.words[5][LANG]
                ],
                    font1=pygame.font.Font('./slidemenu/BeteNoirNF.ttf', 20),
                    font2=pygame.font.Font('./slidemenu/BeteNoirNF.ttf', 25),
                    tooltipfont=pygame.font.Font('./slidemenu/Roboto-MediumItalic.ttf', 12),
                    color1=(255, 80, 40),
                    cursor_img=pygame.image.load("./graph/nepomuk.png"),
                    light=9,
                    centerx=320,
                    y=240
                )
                choice2 = joemenu2[1]

        if choice == 6 or choice is None:
            choice = 0
            sys.exit()

    ship = Ship()
    ship.reset()
    direction = 1
    game.add_enemy(0, 15)
    bg = Background()
    status_bar = StatusBar()
    all_info = pygame.sprite.RenderPlain(status_bar)
    all_sprites = pygame.sprite.Group()
    galaxies = pygame.sprite.Group()
    next_galaxy_time = pygame.time.get_ticks() + random.randint(2000, 10000)

    while game.lives > 0:
        game.clock.tick(FPS)
        game.clock_shield.tick(FPS)
        game.tick_power()
        keyboard()
        if len(game.all_enemies) != 0:
            if game.optionScroll == 0:
                current_time = pygame.time.get_ticks()
                if current_time >= next_galaxy_time:
                    galaxy = Galaxy(800)
                    galaxies.add(galaxy)
                    all_sprites.add(galaxy)
                    next_galaxy_time = current_time + random.randint(2000, 10000)
                bg.update()
                bg.draw(game.surface)
                galaxies.update()
                galaxies.draw(game.surface)
            else:
                game.surface.fill(mycolors.BLACK)
                game.all_polygons.update()
                game.all_polygons.draw(game.surface)

            game.surface.blit(ship.image, ship.rect)
            game.all_weapons.update()
            game.all_weapons.draw(game.surface)
            game.all_enemies.update()
            game.all_enemies.draw(game.surface)
            game.all_enemy_bombs.update()
            game.all_enemy_bombs.draw(game.surface)
            game.all_projectiles.update()
            game.all_projectiles.draw(game.surface)
            game.all_secondary_projectiles.update()
            game.all_secondary_projectiles.draw(game.surface)
            game.all_powerups.update()
            game.all_powerups.draw(game.surface)
            all_info.draw(game.surface)
            all_info.update()

            try:
                game.nepomuk.update()
            except:
                pass

            pygame.display.flip()

        elif len(game.all_enemies) == 0 and game.num_enemies < game.max_enemies:
            game.add_enemy(game.num_enemies, game.max_enemies)

        elif game.level < 13:
            game.num_enemies = 0
            game.empty()
            ship.reset()
            fin = False

            if game.level < 4:
                num_bosses = 1
            elif game.level < 8:
                num_bosses = 2
            else:
                num_bosses = 3

            for i in range(num_bosses):
                boss = Boss()
            while len(game.all_bosses) != 0 and game.lives > 0:
                game.clock.tick(FPS)
                keyboard()
                if game.optionScroll == 0:
                    bg.update()
                    bg.draw(game.surface)
                else:
                    game.surface.fill(mycolors.BLACK)
                    game.all_polygons.update()
                    game.all_polygons.draw(game.surface)
                game.surface.blit(ship.image, ship.rect)
                game.all_weapons.update()
                game.all_weapons.draw(game.surface)
                game.all_projectiles.update()
                game.all_projectiles.draw(game.surface)
                game.all_secondary_projectiles.update()
                game.all_secondary_projectiles.draw(game.surface)
                game.all_enemy_bombs.update()
                game.all_enemy_bombs.draw(game.surface)
                all_info.update()
                all_info.draw(game.surface)
                game.all_bosses.update()
                game.all_bosses.draw(game.surface)
                test_bomb()
                pygame.display.update()

            boss = None
            game.clear()
            if game.lives != 0:
                game.level += 1
                if game.level / 4.0 == int(game.level / 4.0):
                    game.lives += 1
        else:
            game.num_enemies = 0
            game.level = 1

    game.empty()
    game.highscore_write()
    game.game_over()
    game.__init__()

# That's All Folks
# END