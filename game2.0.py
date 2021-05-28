# Imports
import pygame
import random


# Window settings
WIDTH = 1920
HEIGHT = 1080
TITLE = "Into The Void"
FPS = 60

# Game stages
START = 0
PLAYING = 1
TRANSITION = 2
VICTORY = 3
END = 4

# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 4, 23)
GREEN = (2, 227, 62)
YELLOW = (241, 245, 12)
RED = (247, 7, 7)
PURPLE = (147, 2, 204)
LIGHT_BLUE = (23, 91, 92)
PINK = (92, 3, 65)
BROWN = (38, 14, 2)
GREY = (46, 46, 46)
DARK_GREEN = (21, 69, 12)
ORANGE = (186, 81, 0)
YELLOW2 = (23, 91, 92)
RED2 = (23, 91, 92)
PURPLE2 = (45, 4, 54)


# Load fonts
default_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font('assets/fonts/recharge bd.ttf', 80)

# Load images
ship_img = pygame.image.load('assets/images/playerShip2_blue.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserBlue05.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserRed05.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/enemyRed.png').convert_alpha()
enemy2_img = pygame.image.load('assets/images/enemyBlack.png').convert_alpha()
enemy3_img = pygame.image.load('assets/images/enemyGreen2.png').convert_alpha()
missle_img = pygame.image.load('assets/images/laserBlue08.png').convert_alpha()
damage1_img = pygame.image.load('assets/images/playerShip2_damage1.png').convert_alpha()
damage2_img = pygame.image.load('assets/images/playerShip2_damage2.png').convert_alpha()
powerup_img = pygame.image.load('assets/images/powerupBlue_bolt.png').convert_alpha()
powerup2_img = pygame.image.load('assets/images/powerupBlue_shield.png').convert_alpha()
powerup3_img = pygame.image.load('assets/images/powerupBlue.png').convert_alpha()
powerup4_img = pygame.image.load('assets/images/powerupBlue_star.png').convert_alpha()
powerup5_img = pygame.image.load('assets/images/star_gold.png').convert_alpha()
bigmeteor_img = pygame.image.load('assets/images/meteorGrey_big1.png').convert_alpha()
medmeteor_img = pygame.image.load('assets/images/meteorGrey_med2.png').convert_alpha()
ammopowerup_img = pygame.image.load('assets/images/pill_blue.png').convert_alpha()
ammopowerup2_img = pygame.image.load('assets/images/pill_green.png').convert_alpha()
shieldpowerup_img = pygame.image.load('assets/images/shield_silver.png').convert_alpha()
boss_img = pygame.image.load('assets/images/enemyBlack3.png').convert_alpha()
boss2_img = pygame.image.load('assets/images/enemyRed5.png').convert_alpha()

# Load sounds
laser_snd = pygame.mixer.Sound('assets/sounds/sfx_laser2.ogg')
explosion_snd = pygame.mixer.Sound('assets/sounds/explosion.ogg')
missle_snd = pygame.mixer.Sound('assets/sounds/cool_laser.ogg')
bomb_snd = pygame.mixer.Sound('assets/sounds/laser.ogg')
hit_snd = pygame.mixer.Sound('assets/sounds/hit.ogg')
not_hit_snd = pygame.mixer.Sound('assets/sounds/not_hit.ogg')
hit2_snd = pygame.mixer.Sound('assets/sounds/hit2.ogg')
powerup_snd = pygame.mixer.Sound('assets/sounds/powerup.ogg')
victory_snd = pygame.mixer.Sound('assets/sounds/victory.ogg')

#Music
start_music = 'assets/music/PowerBotsLoop.wav'
main_theme = 'assets/music/FiberitronLoop.wav'

# Game classes
class Ship(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.shield = 3
        self.shoots_double = False
        self.invincibility_time = 0
        self.superspeed_time = 0
        self.speed = 5
        self.ammo = 100
        self.ammo2 = 10
        self.shot_wait_time = 0


    def move_left(self):
        if self.superspeed_time > 0:
            self.rect.x -= 2 * self.speed
            self.superspeed_time -= 1
        else:
            self.rect.x -= self.speed

        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        if self.superspeed_time > 0:
            self.rect.x += 2 * self.speed
            self.superspeed_time -= 1
        else:
            self.rect.x += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def move_up(self):
        self.rect.y -= self.speed

        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def move_up2(self):
        self.rect.y -= self.speed

    def shoot(self):
        if self.shoots_double and self.ammo > 0 and self.shot_wait_time == 0:
            x = self.rect.left + 4
            y = self.rect.centery
            lasers.add( Laser(x, y, laser_img) )

            x = self.rect.right - 4
            y = self.rect.centery
            lasers.add( Laser(x, y, laser_img) )
            self.ammo -= 2
            self.shot_wait_time = 15
            laser_snd.play()
        elif not self.shoots_double and self.ammo > 0 and self.shot_wait_time == 0:
            x = self.rect.centerx
            y = self.rect.top
            lasers.add( Laser(x, y, laser_img) )
            self.ammo -= 1
            self.shot_wait_time = 20
            laser_snd.play()

    def shoot2(self):
        if self.ammo2 > 0:
            x = self.rect.centerx
            y = self.rect.top

            missle = Missle(x, y, missle_img)
            missles.add(missle)
            self.ammo2 -= 1
            
            missle_snd.play()

    def check_bombs(self):
        hits = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask) + 2 * (pygame.sprite.spritecollide(self, meteors, True, pygame.sprite.collide_mask))
        if self.invincibility_time == 0: 
            for hit in hits:
                self.shield -= 1
                self.shoots_double = False

                if self.shield <= 0:
                    self.kill()
                    explosion_snd.play()
                elif self.shield > 0:
                    hit_snd.play()
                elif self.shield == 2:
                    pass
                elif self.shield == 1:
                    pass
        else:
            for hit in hits:
                not_hit_snd.play()
                
            self.invincibility_time -= 1
            

    def check_powerups(self):
        hits = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)

        for hit in hits:
            hit.apply(self)
            powerup_snd.play()

    def update(self):
        self.check_bombs()
        self.check_powerups()

        if self.shot_wait_time > 0:
            self.shot_wait_time -= 1


class Laser(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 8

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Missle(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 4

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Bomb(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 6

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class ShieldPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5

    def apply(self, ship):
        if ship.shield >= 3:
            ship.shield += 1
        else:
            ship.shield = 3

        player.score += 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class SpeedPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5

    def apply(self, ship):
        ship.superspeed_time = 10 * FPS
        player.score += 5
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class DoubleShotPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5

    def apply(self, ship):
        ship.shoots_double = True

        player.score += 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class InvincibilityPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5

    def apply(self, ship):
        ship.invincibility_time = 5 * FPS

        player.score += 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            
class RandomPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5

    def apply(self, ship):
        r = random.randrange(1, 10)
        if r == 1:
            ship.invincibility_time = 10 * FPS
        elif r == 2:
            if ship.shield >= 4:
                ship.shield += 1
            else:
                ship.shield = 4
        elif r == 3:
            ship.superspeed_time = 15 * FPS
        elif r == 4:
            ship.shoots_double = True
        elif r == 5:
            ship.ammo += 100
        elif r == 6:
            if ship.shield >= 3:
                ship.shield -= 2
        elif r == 7:
            if ship.ammo >= 50:
                ship.ammo -= 50
            elif ship.ammo >= 10 and ship.ammo < 50:
                ship.ammo -= 10
        elif r == 8:
            if ship.ammo2 >= 3:
                ship.ammo2 -= 3
        elif r == 9:
            ship.shoots_double = False
        else:
            ship.ammo2 += 5

        player.score += 10

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class AmmoPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def apply(self, ship):
        if player.level <= 5:
            ship.ammo += 100 - (10 * player.level)
        else:
            ship.ammo += 50

class AmmoPowerup2(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def apply(self, ship):
        ship.ammo2 += 3

class ShieldPowerup2(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def apply(self, ship):
        if ship.shield <= 3:
            ship.shield += 2
        else:
            ship.shield += 1

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, image, shield, value):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.shield = shield
        self.value = value

    def drop_bomb(self):
        x = self.rect.centerx
        y = self.rect.bottom
        bombs.add( Bomb(x, y, bomb_img) )
        
        bomb_snd.play()

    def update(self):
        hits = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask) + 2*(pygame.sprite.spritecollide(self, missles, True, pygame.sprite.collide_mask))

        for laser in hits:
            self.shield -= 1
            
            if self.shield > 0:
                hit2_snd.play()

        if self.shield <= 0:
            self.kill()
            explosion_snd.play()
            player.score += self.value

class Fleet(pygame.sprite.Group):

    def __init__(self, *sprites):
        super().__init__(*sprites)

        self.speed = 3
        self.speed2 = 2
        self.bomb_rate = 2

    def move(self):
        reverse = False
        reverse2 = False
        
        for sprite in self.sprites():
            sprite.rect.x += self.speed
            sprite.rect.y += self.speed2
            
            if sprite.rect.right >= WIDTH or sprite.rect.left <= 0:
                reverse = True
            elif sprite.rect.top <= 0 or sprite.rect.bottom >= HEIGHT // 2:
                reverse2 = True

        if reverse: self.speed *= -1
        elif reverse2: self.speed2 *= -1

    def select_bomber(self):
        sprites = self.sprites()
        
        if len(sprites) > 0:
            r = random.randrange(0, 120)
            
            if r < self.bomb_rate + 0.50 * player.level:
                bomber = random.choice(sprites)
                bomber.drop_bomb()

    def update(self, *args):
        super().update(*args)

        self.move()

        if len(player) > 0:
            self.select_bomber()

class Meteor(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        
        self.speed = random.randrange(-10, 10)
        self.speed2 = random.randrange(1, 10)
        
    def update(self):
        self.rect.y += self.speed2 + .5 * player.level
        self.rect.x += self.speed + .5 * player.level

        if self.rect.top > HEIGHT:
             self.kill()
                    
        hits = pygame.sprite.spritecollide(self, lasers, True) + 2*(pygame.sprite.spritecollide(self, missles, True))

        if len(hits) > 0:
            self.kill()
            explosion_snd.play()
            player.score += 5
        
# Setup
def new_game():
    global ship, player, star_locs, planet_things
    
    start_x = WIDTH / 2
    start_y = HEIGHT - 100
    ship = Ship(start_x, start_y, ship_img)
    
    player = pygame.sprite.GroupSingle(ship)
    player.score = 0
    player.level = 1

    pygame.mixer.music.load(start_music)
    pygame.mixer.music.play(-1)

    num_stars = 300
    num_planets = 6

    star_locs = []
    while len(star_locs) < num_stars:
        x = random.randrange(0, WIDTH)
        y = random.randrange(0, HEIGHT)
        loc = [x, y]
        star_locs.append(loc)

    planet_things = []
    while len(planet_things) < num_planets:
        x = random.randrange(-100, 2020)
        y = random.randrange(0, HEIGHT)
        
        colors = [PURPLE2, RED2, YELLOW2, DARK_GREEN, LIGHT_BLUE, PINK, ORANGE, BROWN, GREY]
        c = random.choice(colors)

        d = random.randrange(10, 300)

        thing = [x, y, c, d]
        planet_things.append(thing)

def start_level():
    global enemies, lasers, bombs, missles, meteors, powerups

    if player.level == 1:
        e1 = Enemy(310, 100, enemy_img, 1, 10)
        e4 = Enemy(460, 100, enemy_img, 1, 10)
        e5 = Enemy(1110, 300, enemy2_img, 3, 30)
        e6 = Enemy(810, 300, enemy2_img, 3, 30)
        e7 = Enemy(960, 150, enemy2_img, 3, 30)
        e8 = Enemy(960, 450, enemy2_img, 3, 30)
        e9 = Enemy(1360, 100, enemy_img, 1, 10)
        e10 = Enemy(1510, 100, enemy_img, 1, 10)
        e11 = Enemy(360, 400, enemy_img, 1, 10)
        e13 = Enemy(610, 400, enemy_img, 1, 10)
        e14 = Enemy(1310, 400, enemy_img, 1, 10)
        e16 = Enemy(1560, 400, enemy_img, 1, 10)
        enemies = Fleet(e1, e4, e5, e6, e7, e8, e9, e10, e11, e13, e14, e16)
    elif player.level == 2:
        e1 = Enemy(100, 100, enemy_img, 1, 10)
        e2 = Enemy(250, 100, enemy_img, 1, 10)
        e3 = Enemy(710, 100, enemy_img, 1, 10)
        e4 = Enemy(860, 100, enemy_img, 1, 10)
        e5 = Enemy(410, 250, enemy2_img, 3, 30)
        e6 = Enemy(540, 250, enemy2_img, 3, 30)
        e7 = Enemy(175, 300, enemy2_img, 3, 30)
        e8 = Enemy(785, 300, enemy2_img, 3, 30)
        e9 = Enemy(475, 75, enemy2_img, 3, 30)
        e10 = Enemy(475, 375, enemy2_img, 3, 30)
        e11 = Enemy(50, 400, enemy_img, 1, 10)
        e13 = Enemy(300, 400, enemy_img, 1, 10)
        e14 = Enemy(655, 400, enemy_img, 1, 10)
        e16 = Enemy(910, 400, enemy_img, 1, 10)
        enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e13, e14, e16)
    elif player.level >= 3 and player.level <= 9:
        e1 = Enemy(100, 100, enemy2_img, 3, 30)
        e2 = Enemy(250, 100, enemy_img, 1, 10)
        e3 = Enemy(710, 100, enemy_img, 1, 10)
        e4 = Enemy(860, 100, enemy2_img, 3, 30)
        e5 = Enemy(410, 250, enemy3_img, 5, 50)
        e6 = Enemy(540, 250, enemy3_img, 5, 50)
        e7 = Enemy(175, 300, enemy3_img, 5, 50)
        e8 = Enemy(785, 300, enemy3_img, 5, 50)
        e9 = Enemy(475, 75, enemy3_img, 5, 50)
        e10 = Enemy(475, 375, enemy3_img, 5, 50)
        e11 = Enemy(50, 400, enemy_img, 1, 10)
        e12 = Enemy(175, 425, enemy2_img, 3, 30)
        e13 = Enemy(300, 400, enemy_img, 1, 10)
        e14 = Enemy(655, 400, enemy_img, 1, 10)
        e15 = Enemy(785, 425, enemy2_img, 3, 30)
        e16 = Enemy(910, 400, enemy_img, 1, 10)
        enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16)
    elif player.level == 10:
        e1 = Enemy(960, 490, boss_img, 10, 100)
        e2 = Enemy(960, 380, boss2_img, 8, 80)
        e3 = Enemy(960, 200, boss_img, 10, 100)
        e4 = Enemy(760, 450, enemy3_img, 5, 50)
        e5 = Enemy(1160, 450, enemy3_img, 5, 50)
        e6 = Enemy(610, 300, enemy3_img, 5, 50)
        e7 = Enemy(1310, 300, enemy3_img, 5, 50)
        e8 = Enemy(860, 300, enemy3_img, 5, 50)
        e9 = Enemy(1060, 300, enemy3_img, 5, 50)
        e10 = Enemy(560, 200, enemy3_img, 5, 50)
        e11 = Enemy(1360, 200, enemy3_img, 5, 50)
        e12 = Enemy(760, 200, enemy2_img, 3, 30)
        e13 = Enemy(1160, 200, enemy2_img, 3, 30)
        e14 = Enemy(360, 340, boss2_img, 8, 80)
        e15 = Enemy(1560, 340, boss2_img, 8, 80)
        enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15)

    lasers = pygame.sprite.Group()
    missles = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    x = random.randrange(-1000, -100)
    y = random.randrange(-1000, -100)
    m1 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(-2000, -200)
    y = random.randrange(-2000, -200)
    m2 = Meteor(x, y, medmeteor_img)

    x = random.randrange(-3000, -300)
    y = random.randrange(-3000, -300)
    m3 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(-1000, -100)
    y = random.randrange(-1000, -100)
    m4 = Meteor(x, y, bigmeteor_img)
        
    x = random.randrange(-2000, -200)
    y = random.randrange(-2000, -200)
    m5 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(-3000, -300)
    y = random.randrange(-3000, -300)
    m6 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(-2000, -200)
    y = random.randrange(-2000, -200)
    m7 = Meteor(x, y, medmeteor_img)

    x = random.randrange(-3000, -300)
    y = random.randrange(-3000, -300)
    m8 = Meteor(x, y, medmeteor_img)

    x = random.randrange(2020, 2920)
    y = random.randrange(-1000, -100)
    m9 = Meteor(x, y, bigmeteor_img)
        
    x = random.randrange(2120, 3920)
    y = random.randrange(-2000, -200)
    m10 = Meteor(x, y, medmeteor_img)

    x = random.randrange(2220, 4920)
    y = random.randrange(-3000, -300)
    m11 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(2020, 2920)
    y = random.randrange(-1000, -100)
    m12 = Meteor(x, y, bigmeteor_img)
        
    x = random.randrange(2120, 3920)
    y = random.randrange(-2000, -200)
    m13 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(2220, 4920)
    y = random.randrange(-3000, -300)
    m14 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(2120, 3920)
    y = random.randrange(-2000, -200)
    m15 = Meteor(x, y, medmeteor_img)

    x = random.randrange(2220, 4920)
    y = random.randrange(-3000, -300)
    m16 = Meteor(x, y, medmeteor_img)

    x = random.randrange(0, 1920)
    y = random.randrange(-1000, -100)
    m17 = Meteor(x, y, bigmeteor_img)
        
    x = random.randrange(0, 1920)
    y = random.randrange(-2000, -200)
    m18 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(0, 1920)
    y = random.randrange(-3000, -300)
    m19 = Meteor(x, y, bigmeteor_img)

    x = random.randrange(0, 1920)
    y = random.randrange(-2000, -200)
    m20 = Meteor(x, y, medmeteor_img)

    meteors = pygame.sprite.Group(m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20)


    x = random.randrange(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p1 = ShieldPowerup(x, y, powerup2_img)

    x = random.randrange(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p2 = SpeedPowerup(x, y, powerup_img)

    x = random.randrange(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p3 = DoubleShotPowerup(x, y, powerup3_img)

    x = random.randrange(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p4 = InvincibilityPowerup(x, y, powerup4_img)

    x = random.randrange(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p5 = RandomPowerup(x, y, powerup5_img)
    
    powerups = pygame.sprite.Group(p1, p2, p3, p4, p5)

def transition_screen():
    global powerups
    p1 = AmmoPowerup(WIDTH // 2 - 100, HEIGHT // 2, ammopowerup_img)
    p2 = AmmoPowerup2(WIDTH // 2 + 100, HEIGHT // 2, ammopowerup2_img)
    p3 = ShieldPowerup2(WIDTH // 2, HEIGHT // 2, shieldpowerup_img)
    powerups = pygame.sprite.Group(p1, p2, p3)

def display_stats():
    score_text = default_font.render("Score: " + str(player.score), True, WHITE)
    rect = score_text.get_rect()
    rect.top = 20
    rect.left = 20
    screen.blit(score_text, rect)

    level_text = default_font.render("Level: " + str(player.level), True, WHITE)
    rect = score_text.get_rect()
    rect.top = 20
    rect.right = WIDTH - 20
    screen.blit(level_text, rect)

    pygame.draw.rect(screen, WHITE, [50, HEIGHT - 80, 225, 50])
    if ship.shield == 3:
        pygame.draw.rect(screen, GREEN, [53, HEIGHT - 77, 219, 44])
    elif ship.shield == 2:
        pygame.draw.rect(screen, YELLOW, [53, HEIGHT - 77, 146, 44])
    elif ship.shield == 1:
        pygame.draw.rect(screen, RED, [53, HEIGHT - 77, 73, 44])
    elif ship.shield >= 4:
        x = (ship.shield - 3) * 5
        pygame.draw.rect(screen, PURPLE, [280, HEIGHT - 77, x, 44])
        pygame.draw.rect(screen, GREEN, [53, HEIGHT - 77, 219, 44])

    ammo_text = default_font.render("Ammo: " + str(ship.ammo), True, WHITE)
    rect = ammo_text.get_rect()
    rect.bottom = HEIGHT - 20
    rect.right = WIDTH - 20
    screen.blit(ammo_text, rect)

    ammo2_text = default_font.render("Missle Ammo: " + str(ship.ammo2), True, WHITE)
    rect = ammo2_text.get_rect()
    rect.bottom = HEIGHT - 60
    rect.right = WIDTH - 20
    screen.blit(ammo2_text, rect)

def draw_stars():
    for loc in star_locs:
        x = loc[0]
        y = loc[1]
        pygame.draw.ellipse(screen, WHITE, [x, y, 3, 3])

def draw_planets():
    for thing in planet_things:
        x = thing[0]
        y = thing[1]
        c = thing[2]
        d = thing[3]
        pygame.draw.ellipse(screen, c, [x, y, d, d])

def start_screen():
    title_text = title_font.render(TITLE, True, WHITE)
    rect = title_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.bottom = HEIGHT // 2
    screen.blit(title_text, rect)

    sub_text = default_font.render("Mission: Fight your way through enemy forces to end the war", True, WHITE)
    rect = sub_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.top = HEIGHT // 2
    screen.blit(sub_text, rect)

    sub_text2 = default_font.render("Press any key to start", True, WHITE)
    rect = sub_text2.get_rect()
    rect.centerx = WIDTH // 2
    rect.top = HEIGHT // 2 + 30
    screen.blit(sub_text2, rect)

def end_screen():
    end_text = title_font.render("GAME OVER" , True, WHITE)
    rect = end_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.centery = HEIGHT // 2
    screen.blit(end_text, rect)

def victory_screen():
    victory_text = title_font.render("You Saved The Galaxy!!!" , True, WHITE)
    rect = victory_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.bottom = HEIGHT // 2
    screen.blit(victory_text, rect)

    sub_text = default_font.render("Press any key to play again", True, WHITE)
    rect = sub_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.top = HEIGHT // 2
    screen.blit(sub_text, rect)

# Game loop
new_game()
start_level()
stage = START

running = True

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
            if stage == START:
                stage = PLAYING
                pygame.mixer.music.load(main_theme)
                pygame.mixer.music.play(-1)
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                elif event.key == pygame.K_n:
                    ship.shoot2()
            elif stage == END:
                if event.key == pygame.K_r:
                    new_game()
                    start_level()
                    stage = START

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        elif pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()

    elif stage == TRANSITION:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        elif pressed[pygame.K_UP]:
            ship.move_up2()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()
            
        if ship.rect.bottom <= 0:
                player.level += 1
                stage = PLAYING
                start_level()
                ship.rect.top = HEIGHT

    elif stage == VICTORY:
        if event.type == pygame.KEYDOWN:
            new_game()
            start_level()
            stage = START       
        
    # Game logic
    if stage != START:
        missles.update()
        lasers.update()
        enemies.update()
        meteors.update()
        bombs.update()
        player.update()
        powerups.update()
        ship.check_powerups()
        

    if len(enemies) == 0 and player.level == 10:
        stage = VICTORY
        
    if len(enemies) == 0 and stage == PLAYING and not player.level == 10:
        victory_snd.play()
        transition_screen()

    if len(enemies) == 0 and not player.level == 10:
        stage = TRANSITION

    if len(player)== 0:
        stage = END
        pygame.mixer.music.stop()

    elif ship.ammo + ship.ammo2 <= 0:
        stage = END
        pygame.mixer.music.stop()

    for loc in star_locs:
        loc[1] += 1

        if loc[1] > HEIGHT:
            loc[0] = random.randrange (0, WIDTH)
            loc[1] = random.randrange(-600, 0)

    for thing in planet_things:
        thing[1] += 1

        if thing[1] > HEIGHT:
            thing[0] = random.randrange (-100, 2020)
            thing[1] = random.randrange(-900, -300)

    # Drawing code
    screen.fill(BLACK)
    draw_stars()
    draw_planets()
    lasers.draw(screen)
    player.draw(screen)
    enemies.draw(screen)
    missles.draw(screen)
    meteors.draw(screen)
    bombs.draw(screen)
    powerups.draw(screen)
    display_stats()

    if stage == START:
        start_screen()
    elif stage == END:
        end_screen()
    elif stage == VICTORY:
        victory_screen()
        
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

