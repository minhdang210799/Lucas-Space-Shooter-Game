#Create your own shooter

from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 60:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 30, 25, 25)
        bullets.add(bullet)

class Enemy(GameSprite):   
    def update(self):
        self.rect.y += self.speed
        global lost
        global finish
        if self.rect.y >= win_height:
            self.rect.y = 0
            lost += 1
        if lost == 10:
            finish = True
            window.blit(lose, (win_width/2, win_height/2))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 1:
            bullets.remove(self)
            

win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))

score = 0
lost = 0

background = GameSprite("galaxy.jpg", 0, 0, win_width, win_height, 0)
player = Player("rocket.png", 0, win_height - 60, 50, 57, 14)

enemies = sprite.Group()
for i in range(1, 6):
    randPos = randint(60, win_width - 50)
    monster = Enemy("ufo.png", randPos, 0, 60, 50, randint(5, 7))
    enemies.add(monster)

bullets = sprite.Group()
 
mixer.init()

mixer.music.load("space.ogg")
mixer.music.play()

shoot_sound = mixer.Sound("shoot.wav")

font.init()
font1 = font.Font(None, 72)
win = font1.render('You winner!1!', True, (0, 255, 0))
lose = font1.render('You lost...', True, (255, 0, 0))
font2 = font.Font(None, 36)

game = True
finish = False
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                shoot_sound.play()
    
    if not finish:
        background.reset()

        player.update()

        player.reset()

        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)

        if sprite.groupcollide(enemies, bullets, True, True):
            score += 1
            randPos = randint(60, win_width - 50)
            enemy = Enemy("ufo.png", randPos, 0, 60, 50, randint(5, 9))
            enemies.add(enemy)
            if score == 10:
                finish = True
                window.blit(win, (win_width/2, win_height/2))

        if sprite.spritecollide(player, enemies, False):
            finish = True
            window.blit(lose, (win_width/2, win_height/2))


        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

    display.update()
    time.delay(FPS)
