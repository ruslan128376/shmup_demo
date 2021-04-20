import pygame
import random
import sys
import func_lib as f

from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# CONSTANTS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ENEMY_BULLET_SPEED = 8.0
MOB_SPEED = 8.0
DAMAGE = 9



#----------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()


    def update(self):
        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # тайм-аут для бонусов
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()


    def shoot(self):
        if self.rect.top > HEIGHT:
            return
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.centerx, self.rect.centery)
                bullet3 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()


    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

#-------------------------------------------------------------
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        if MOB_SPEED >= 2.0:
            self.speedy = random.randrange(1, int(MOB_SPEED))
        else:
            self.speedy = 1
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

#-------------------------------------------------------------
class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_images['enemy1']
        self.image = pygame.transform.scale(self.image, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .8 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)
        self.last_update = pygame.time.get_ticks()
        self.aim_y = random.randrange(100,400)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.hp = 10


    def update(self):
        self.shoot()
        if self.rect.centery >= self.aim_y:
            self.speedy = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if  self.rect.left < 25  or self.rect.right > (WIDTH-25) :
           self.speedx = -self.speedx

        


    def shoot(self):
         now = pygame.time.get_ticks()
         if now - self.last_shot > self.shoot_delay:
             self.last_shot = now
             bullet = Bullet_enemy(self.rect.centerx, self.rect.bottom)
             all_sprites.add(bullet)
             bullets_enemy.add(bullet)
             

#--------------------------BOSS---------------------------
class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = enemy_images['enemy2']
        self.image_orig.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image_orig, (50*3, 38*4))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 3)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = 1
        self.last_update = pygame.time.get_ticks()
        self.aim_y = random.randrange(100,250)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 600
        self.hp = 250


    def update(self):
        self.shoot()
        if self.rect.centery >= self.aim_y:
            self.speedy = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if  self.rect.left < 25  or self.rect.right > (WIDTH-25) :
            self.speedx = -self.speedx
        

    def shoot(self):
         now = pygame.time.get_ticks()
         if now - self.last_shot > self.shoot_delay:
             self.last_shot = now
             bullet = Bullet_enemy(self.rect.centerx, self.rect.bottom)
             all_sprites.add(bullet)
             bullets_enemy.add(bullet)

#-------------------------------------------------------------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#-------------------------------------------------------------------------
class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(bullet_enemy_img, (20, 20))

        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.last_update = pygame.time.get_ticks()
        self.rot = 0
        self.rot_speed = 10
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        d=f.dist(x, y, player.rect.centerx, player.rect.centery)
        self.speedx = ENEMY_BULLET_SPEED * (player.rect.centerx - x) / d
        self.speedy = ENEMY_BULLET_SPEED * (player.rect.centery - y) / d

    def update(self):
        self.rotate()
        self.rect.x = float(self.rect.x) + self.speedx
        self.rect.y = float(self.rect.y) + self.speedy


        if self.rect.bottom < 0:
            self.kill()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


#--------------------------------------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#--------------------------------------------------------------------

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > HEIGHT:
            self.kill()

#----------------------------------------------------------------------
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def new_enemy1():
    e = Enemy1()
    all_sprites.add(e)
    enemies.add(e)
    
def new_enemy2():
    e = Enemy2()
    all_sprites.add(e)
    enemies.add(e)


"""
def f.dist(x1, y1, x2, y2):
    d=(x2-x1)**2 + (y2-y1)**2
    return float(d**0.5)
"""
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHOOT'EM UP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_win_screen():
    
    screen.blit(background, background_rect)
    draw_text(screen, "CONGRATULATION!", 50, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "MISSION COMPLETE", 36,
              WIDTH / 2, HEIGHT / 2)
    sc = "Score: " + str(score)
    draw_text(screen, sc, 18, WIDTH / 2, HEIGHT * 5 / 8)
    draw_text(screen, "Press a key to exit", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.time.delay(2000)
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYUP:
                pygame.quit()
                sys.exit()
            #if event.type == pygame.KEYUP:
            #    pygame.quit()
                


               
#------------------------------------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.3)

# Загрузка мелодий игры
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'Powerup2.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'Powerup3.wav'))

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

# Загрузка всей игровой графики
powerups = pygame.sprite.Group()

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

# enemies
enemy_images = {}
enemy_images['enemy1'] = pygame.image.load(path.join(img_dir, 'enemyBlack3.png')).convert()
enemy_images['enemy2'] = pygame.image.load(path.join(img_dir, 'enemyBlack5.png')).convert()

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

meteor_images = []
meteor_list =['meteorBrown_big1.png','meteorBrown_med1.png',
              'meteorBrown_med1.png','meteorBrown_med3.png',
              'meteorBrown_small1.png','meteorBrown_small2.png',
              'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

background = pygame.image.load(path.join(img_dir, 'starfield.webp')).convert()
background = pygame.transform.scale(background, (WIDTH,HEIGHT))
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "playerShip1_blue.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()
bullet_enemy_img = pygame.image.load(path.join(img_dir, "laserRed10.png")).convert()

#----------------------------------------------------------
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()
score = 0
game_pause = 0
pygame.mixer.music.play(loops = -1)

# Цикл игры
game_over = True
running = True
enemy_count = 1
boss_run = False
bosses = 0

while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bullets_enemy = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(10):
            newmob()
        score = 0

    clock.tick(FPS)
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    all_sprites.update()
    
    # логика  выпуска вражеских  космолетов
    #print("len(enemies)",len(enemies))

    if len(enemies) == 0 and boss_run == False:
        for i in range(enemy_count):
            new_enemy1()
        enemy_count += 1
        if enemy_count == 9:
            boss_run = True
        
    # BOSS
    if boss_run == True and MOB_SPEED>0.1:
        MOB_SPEED -= 0.05
    if boss_run == True and bosses == 0:
        new_enemy2()
        bosses = 1
    

    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            power_sound.play()
            player.powerup()

    # проверка, не попала ли пуля в моб
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # попала ли наша пуля во врага
    hits = pygame.sprite.groupcollide(enemies, bullets, False,True)
    for hit in hits:
        hit.hp -= DAMAGE
        if hit.hp <= 0:
            hit.kill()
            
            if type(hit) == Enemy2:
                expl = Explosion(hit.rect.bottomleft, 'lg')
                all_sprites.add(expl)
                expl = Explosion(hit.rect.bottomright, 'lg')
                all_sprites.add(expl)
                expl = Explosion(hit.rect.topleft, 'lg')
                all_sprites.add(expl)
                expl = Explosion(hit.rect.topright, 'lg')
                all_sprites.add(expl)
                game_pause = 300
                
                
                
        score += 50
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.85:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        
    if game_pause>0:
        game_pause -=1
    if game_pause == 1 and boss_run == True:
        show_win_screen()
        
    
    # попала ли вражеская пуля в нас
    hits = pygame.sprite.spritecollide(player, bullets_enemy, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        random.choice(expl_sounds).play()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            print("Your score:", score)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            print("Your score:", score)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

        # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives,  player_mini_img)
    if boss_run:
        draw_text(screen, "KILL ENEMY STARSHIP!", 24, WIDTH / 2, 50)
        

    pygame.display.flip()

pygame.quit()
sys.exit()



