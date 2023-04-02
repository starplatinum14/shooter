from pygame import *
from random import randint
import pygame_menu
import os
init()
font.init()

mixer.init()
mixer.music.load("song.mp3")
mixer.music.set_volume(0.3)
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)


WIDTH, HEIGHT = 700, 500
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("treasure")
clock = time.Clock()

path = os.getcwd()
exp_images = os.listdir(path + "/explosion")
images_list = []
for img in exp_images:
    images_list.append(transform.scale(image.load("explosion/" + img), (1000,1000)))

class Explosion(sprite.Sprite):
    def __init__(self, x, y, images_list):
        super().__init__()
        self.images = images_list
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y-300

        self.k = 0
        self.frames = 0

    def update(self):
        window.blit(self.image, self.rect)
        self.frames += 1
        if self.frames == 3 and self.k < len(self.images) -1:
            self.frames = 0
            self.k += 1
            self.image = self.images[self.k]
        if  self.k == len(self.images) -1:
            self.kill()   
    

bullet_image = image.load("bullet.png")
explosions = sprite.Group()
rocket_image = image.load("roketka.png")
ufo_image = image.load("rotation.png")

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y, speed=3):
        super().__init__()

        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.mask = mask.from_surface(self.image)

    def draw(self):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lives = 1000 

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 7:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(bullet_image, 10, 20, self.rect.centerx, self.rect.y)
        bullets.add(bullet)
        fire_sound.play()


class Enemy(GameSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = randint(3, 6) 

    def update(self):
        global lost
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else:
            lost += 1
            lost_text.set_text("Пропущено: " + str(lost))
            self.rect.y = randint(-500, -100)
            self.rect.x = randint(0, WIDTH - 70)

class Text(GameSprite):
    def __init__(self,text, x, y, font_size=22, font_name="Impact", color=(255,255,255)):
        self.font = font.SysFont(font_name, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.color = color
    def draw(self):
        window.blit(self.image, self.rect)
    def set_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)


class Bullet(GameSprite):
    def update(self):
        if self.rect.y > -20:
            self.rect.y -= self.speed
        else:
            self.kill()

        
score_text = Text("Рахунок:0", 20, 50,)
lost_text = Text("Пропущено:0", 20, 20)
lives_text = Text("життя:3", 20, 80)
bg = transform.scale(image.load("bg.jpg"), (WIDTH, HEIGHT))
bg2 = transform.scale(image.load("bg.jpg"), (WIDTH, HEIGHT))
bg1_y = 0
bg2_y = -HEIGHT
player = Player(rocket_image, width = 70, height = 70, x = WIDTH-200, y = HEIGHT-100, speed = 20)
bullets = sprite.Group()
Meteors = sprite.Group()
for i in range(10):
    rand_y = randint(-500, -100)
    rand_x = randint(0,WIDTH - 70)
    rand_speed = randint(1,15 )
    Meteors.add(Enemy(ufo_image, width = 180, height = 150, x = rand_x, y = rand_y, speed = rand_speed))


step = 3
FPS = 60
font.init()
font1 = font.SysFont("Impact", 50)
win = font1.render("YOUR WINERS", True,(0,255,0))
lose = font1.render("YOUR LOZER", True,(255,0,0))
run = True
finish = False
score = 0
lost = 0
result_text = Text("YOU WWWIIIINN", 350, 250)

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    menu.disable()

menu = pygame_menu.Menu('Spase hooter', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='SEMEN')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(window)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_ESCAPE:
                menu.enable()
                menu.mainloop(window)
    if not finish:
        spritelist = sprite.spritecollide(player, Meteors, True, sprite.collide_mask)
        for colide in spritelist:
            player.lives -= 1
            if player.lives == 0:
                finish = True
                result_text.set_text("YOU LOSE")
            else:
                lives_text.set_text("Lives: " + str(player.lives))
        spritelist = sprite.groupcollide(Meteors, bullets, True, True, sprite.collide_mask)
        for colide in spritelist:
            explosions.add(Explosion(colide.rect.x, colide.rect.y, images_list))
            score += 1
            score_text.set_text("Рахунок: " + str(score))
            rand_y = randint(-500, -100)
            rand_x = randint(0,WIDTH - 70)
            rand_speed = randint(2, 5)
            Meteors.add(Enemy(ufo_image, width = 80, height = 50, x = rand_x, y = rand_y, speed = rand_speed))
        if lost >= 40:
            finish = True
            result_text.set_text("YOU LOSE")
        if score >= 50:
            finish = True
        window.blit(bg,(0,bg1_y))
        window.blit(bg,(0,bg2_y))
        bg1_y +=1
        bg2_y +=1
        if bg1_y > HEIGHT:
            bg1_y = -HEIGHT
        if bg2_y > HEIGHT:
            bg2_y = -HEIGHT
        player.update()
        bullets.update()
        Meteors.update()
        explosions.update()
        explosions.draw(window)
        
    else:
        result_text.draw()

    player.draw()
    Meteors.draw(window)
    bullets.draw(window)
    lives_text.draw()
    score_text.draw()
    lost_text.draw()
    display.update()
    clock.tick(FPS)                    