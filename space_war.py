# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1200
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Gardening"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)
GRASS = (104, 173, 45)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 84)


# Images
start_img = pygame.image.load('assets/images/Background/start screen.jpg')
start_img = pygame.transform.scale(start_img, (1200, 1000))

bkg_img = pygame.image.load('assets/images/Background/grass lmao.jpg')
bkg_img = pygame.transform.scale(bkg_img, (1200, 1000)).convert_alpha()

player_img = pygame.image.load('assets/images/tank_blue.png').convert_alpha()
player_img = pygame.transform.rotate(player_img, 180)
player_img = pygame.transform.scale(player_img, (75, 75))

player_right_img = pygame.image.load('assets/images/tank_blue_face_right.png').convert_alpha()
player_right_img = pygame.transform.scale(player_right_img, (90, 90))
player_right_img = pygame.transform.rotate(player_right_img, 90)

player_left_img = pygame.transform.flip(player_right_img, True, False)


laser_img = pygame.image.load('assets/images/bulletBlue2_outline.png').convert_alpha()
laser_img = pygame.transform.scale(laser_img, (20, 24))

enemy_img = pygame.image.load('assets/images/Evil Tree-1.png.png').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (100, 100)).convert_alpha()

enemy2_img = pygame.image.load('assets/images/Evil Tree-2.png.png').convert_alpha()
enemy2_img = pygame.transform.scale(enemy2_img, (100, 100)).convert_alpha()

bomb_img = pygame.image.load('assets/images/treeGreen_twigs.png').convert_alpha()

powerup_img = pygame.image.load('assets/images/meteorSmall.png').convert_alpha()
# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
WOW = pygame.mixer.Sound('assets/sounds/wow.wav')
BAZINGA = pygame.mixer.Sound('assets/sounds/bazinga.wav')
WIN_JINGLE = pygame.mixer.Sound('assets/sounds/Win Jingle.wav')


#Musics
start_theme = 'assets/musics/Map.wav'
gameplay_theme = 'assets/musics/BossMain.wav'
end_theme = 'assets/musics/Map (basic version).wav'


# Stages
START = 0
PLAYING = 1
END = 2

score = 0
wave = 1
# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, stopped, left, right):
        super().__init__()


        self.stopped = stopped
        self.left = left
        self.right = right
        self.not_dead = True

        self.image = stopped
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 3
        self.speed = 10

    def stop(self):
        self.image = self.stopped
        
    def move_left(self):
        self.rect.x -= self.speed
        self.image = self.left
    
    def move_right(self):
        self.rect.x += self.speed
        self.image = self.right

    def shoot(self):
        print("Diplomacy sound!")
        BAZINGA.play()

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self):
        '''edge detec'''
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        '''yumbo detection'''
        hit_list = pygame.sprite.spritecollide(self, powerups, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            for hit in hit_list:
                hit.apply(self)

        ''' ouch detection '''
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -= 1
            BAZINGA.play()
            print("ouched")

        if self.shield == -1:
            self.not_dead = False
            self.kill()
            stage = END
            set_music(end_theme)
            show_end()

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image1, image2):
        super().__init__()

        self.image = image1
        self.damaged = image2

        self.mask = pygame.mask.from_surface(self.image)
        self.shield = 1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def drop_bomb(self):
        print("Bazinga")

        BAZINGA.play()
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.top
        bombs.add(bomb)

    def update(self):
        global score
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.shield -= 1
            BAZINGA.play()
            print("ouched")

        if self.shield == 0:
            self.image = self.damaged
        elif self.shield == -1:
            BAZINGA.play()
            self.kill()
            score += 1

        if self.rect.y < HEIGHT:
            self.kill
class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 10

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class ShieldPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 6
        self.rect.x = x
        self.rect.y = y

    def apply(self, ship):
        print('yumbo in my tumbo')
        ship.shield = 3
        self.kill()

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

        
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 10
        self.moving_right = True
        self.drop_speed = 20
        self.bomb_rate = 50 #Lower is faster

    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            
            
    def reverse(self):
        self.moving_right = not self.moving_right
        self.move_down()

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()

# Game helper functions
def show_title_screen():
    screen.blit(start_img, (0, 0))

    title_text = FONT_XL.render("Xtreme Gardening!", 1, BLACK)
    w = title_text.get_width()
    screen.blit(title_text, [(WIDTH/2 - w/2), 204])

def show_end():
    if ship.not_dead == True:
        win_text = FONT_XL.render("The end...?", 1, WHITE)
        w = win_text.get_width()
        screen.blit(win_text, [(WIDTH/2 - w/2), 204])

    else:
        lose_text1 = FONT_XL.render("The gardener becomes", 1, WHITE)
        w1 = lose_text1.get_width()
        screen.blit(lose_text1, [(WIDTH/2 - w1/2), 204])

        lose_text2 = FONT_XL.render("the gardened.", 1, WHITE)
        w2 = lose_text2.get_width()
        screen.blit(lose_text2, [(WIDTH/2 - w2/2), 254])

    end_text1 = FONT_LG.render("Press space to play again", 1, WHITE)
    ew1 = end_text1.get_width()
    screen.blit(end_text1, [(WIDTH/2 - ew1/2), 504])

    end_text2 = FONT_LG.render("Press Q to quit", 1, WHITE)
    ew2 = end_text2.get_width()
    screen.blit(end_text2, [(WIDTH/2 - ew2/2), 554])
        
    end_text3 = FONT_LG.render("You scored: " + str(score), 1, WHITE)
    ew3 = end_text3.get_width()
    screen.blit(end_text3, [(WIDTH/2 - ew3/2), 654])
    
def setup():
    global stage, done, score, wave
    global player, ship, lasers, mobs, fleet, bombs, powerups

    ''' Set Stats '''
    score = 0
    wave = 1
    ''' Make game objects '''
    ship = Ship(WIDTH/2, HEIGHT - 100, player_img, player_left_img, player_right_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)

    lasers = pygame.sprite.Group()

    bombs = pygame.sprite.Group()

    mob1 = Mob(100, 100, enemy_img, enemy2_img)
    mob2 = Mob(300, 100, enemy_img, enemy2_img)
    mob3 = Mob(500, 100, enemy_img, enemy2_img)
    mob4 = Mob(200, 200, enemy_img, enemy2_img)
    mob5 = Mob(400, 200, enemy_img, enemy2_img)

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5)

    fleet = Fleet(mobs)

    powerup1 = ShieldPowerUp(200, -800, powerup_img)
    powerup2 = ShieldPowerUp(860, -2000, powerup_img)
    powerup3 = ShieldPowerUp(500, -3000, powerup_img)

    powerups = pygame.sprite.Group()
    powerups.add(powerup1)
    
    ''' set stage '''
    stage = START
    set_music(start_theme)
    done = False

def show_stats(player, score):
    #wave display
    wave_text = FONT_LG.render("Wave " + str(wave), 1, WHITE)
    screen.blit(wave_text, (50, 50))

    #score display
    score_text = FONT_LG.render("Score: " + str(score), 1, WHITE)
    screen.blit(score_text, (50, 125))

    #shield display
    pygame.draw.rect(screen, WHITE, [1000, 50, 150, 20])

    if ship.shield == 2:
        pygame.draw.rect(screen, RED, [1100, 50, 50, 20])
    elif ship.shield == 1:
        pygame.draw.rect(screen, RED, [1050, 50, 100, 20])
    elif ship.shield == 0:
        pygame.draw.rect(screen, RED, [1000, 50, 150, 20])

def set_music(track):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(500)

    if track != None:    
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)

def next_wave():
    global wave, fleet

    lasers = pygame.sprite.Group()

    bombs = pygame.sprite.Group()

    mob1 = Mob(100, 100, enemy_img, enemy2_img)
    mob2 = Mob(300, 100, enemy_img, enemy2_img)
    mob3 = Mob(500, 100, enemy_img, enemy2_img)
    mob4 = Mob(200, 200, enemy_img, enemy2_img)
    mob5 = Mob(400, 200, enemy_img, enemy2_img)

    mobs.add(mob1, mob2, mob3, mob4, mob5)

    fleet = Fleet(mobs)

    wave += 1
    fleet.speed += 10
    fleet.bomb_rate -= 20

# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    set_music(gameplay_theme)
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()
                if event.key == pygame.K_q:
                    pygame.quit()

    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        else:
            ship.stop()

    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        ship.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        powerups.update()
        
    if len(mobs) == 0:
        next_wave()
        
        if wave == 4:
            WIN_JINGLE.play()
            stage = END

    elif ship.not_dead == False:
        stage = END


    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(bkg_img, (0, 0))
    player.draw(screen)
    mobs.draw(screen)
    
    if stage == START:
        show_title_screen()

    elif stage == PLAYING:
        bombs.draw(screen)
        lasers.draw(screen)
        powerups.draw(screen)
        show_stats(player, score)

    elif stage == END:
         show_end()
    
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
