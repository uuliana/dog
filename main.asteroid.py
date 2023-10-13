from pygame import *

window = display.set_mode((580, 500))
display.set_caption("Asteroids")
back = (120, 153, 234)
window.fill(back)

clock = time.Clock()
FPS = 60
game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed= pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("the_kistka_cool.png", self.rect.centerx, self.rect.top, 15, 30, -15)
        bullets.add(bullet)

from random import *
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global hearts
        if self.rect.y > 500:
            try:
                hearts.pop(0)
            except:
                pass
            self.rect.x = randint(0, 600)
            self.rect.y = 0
            self.speed = randint(1, 3)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()


asteroids = sprite.Group()
for i in range(1, 6):
    asteroid = Enemy("super_dog.png", randint(80, 620), -40, 50, 50, randint(1, 5))
    asteroids.add(asteroid)


rocket = Player("dog_food.png", 20, 400, 65, 65, 4)
background = transform.scale(image.load("top_les.jpg"), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(15)

fire_sound = mixer.Sound("fire.ogg")
score = 0

font.init()
mainfont = font.Font("rosehot.ttf", 40)
score = 0

from time import time as timer
rel_time = False
num_fire = 0

hearts = []
hX = 225
for i in range(10):
    heart = GameSprite("pngwing.com.png", hX, 10, 50, 50, 0)
    hearts.append(heart)
    hX += 35

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

                
    if not finish:
        window.blit(background, (0, 0))
        score_text = mainfont.render("KILLED: "+str(score), True, (0, 255, 0))
        lose_text = mainfont.render("MISSED: "+str(lost), True, (255, 0, 0))
        window.blit(score_text, (5, 10))
        window.blit(lose_text, (5, 60))
        rocket.draw()
        rocket.update()
        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score += 1
            asteroid = Enemy("super_dog.png", randint(80, 620), -40, 50, 50, randint(1, 5))
            asteroids.add(asteroid)


        if lost > 10:
            loser = mainfont.render("YOU LOSER", True, (255, 0, 0))
            window.blit(loser, (220, 220))
            finish = True

        if rel_time:
            now_time = timer()
            if now_time - last_time < 0.5:
                reload = mainfont.render("RELOADING...", True, (225, 0, 0))
                window.blit(reload,(220, 220))
            else:
                num_fire = 0
                rel_time = False

        if sprite.spritecollide(rocket, asteroids, False):
            finish = True
            loser = mainfont.render("YOU LOSER", True, (255, 0, 0))
            window.blit(loser, (220, 220))


        for heart in hearts:
            heart.draw()

        if rocket.rect.x >= 515:
            rocket.rect.x = 515

        if rocket.rect.x <= 0:
            rocket.rect.x = 0

            



            


    display.update()
    clock.tick(FPS)
