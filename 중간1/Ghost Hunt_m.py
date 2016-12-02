import pygame
import random
import time

start_time = time.time()
black = [ 0, 0, 0 ]
white = [ 255, 255, 255 ]
screen_width = 500
screen_height = 500
random.seed()

class Player(pygame.sprite.Sprite):
    speed_x = 0
    speed_y = 0
    g = 1   #중력

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = []

        for i in range(1, 3):
            img = pygame.image.load("player"+str(i)+".png").convert()
            img.set_colorkey(black)
            self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def set_speed(self, x, y):
        self.speed_x += x
        self.speed_y += y

    def update(self):
        if self.speed_y != 0:
            self.g = 1
        else:
            self.g += 0.1
        old_x = self.rect.x
        old_y = self.rect.y

        self.rect.x += self.speed_x
        if self.rect.x < 5 or self.rect.x > screen_width - 25 - 5:   #테두리
            self.rect.x = old_x

        if (150 - 25 < self.rect.x and self.rect.x < 350) and self.rect.y > 430 - 60:   #땅
            self.rect.x = old_x

        self.rect.y += self.speed_y
        self.rect.y += self.g
        if self.rect.y < 5 or self.rect.y > screen_height - 60 - 5:  #테두리 (떨어짐처리X)
            self.rect.y = old_y

        if (150 - 25 < self.rect.x and self.rect.x < 350) and self.rect.y > 430 - 60:   #땅
            self.rect.y = old_y

        if self.speed_x < 0:
            self.image = self.images[1]
        elif self.speed_x > 0:
            self.image = self.images[0]

class Bullet(pygame.sprite.Sprite):
    speed_x = 0
    speed_y = 0

    def __init__(self, n):
        pygame.sprite.Sprite.__init__(self)

        self.images = []

        for i in range(0, 8):
            img = pygame.image.load("bullet"+str(i)+".png").convert()
            img.set_colorkey(black)
            self.images.append(img)

        self.image = self.images[n]
        self.rect = self.image.get_rect()

        if 0 <= n and n <= 2 :  #이미지 번호에 따른 x, y 방향 설정
            self.speed_y = -10
        if 5 <= n and n <= 7 :
            self.speed_y = 10
        if n == 0 or n == 3 or n == 5 :
            self.speed_x = -10
        if n == 2 or n == 4 or n == 7 :
            self.speed_x = 10

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x > 500 or  self.rect.x < 0 or self.rect.y > 500 or self.rect.y < 0:   #테두리 밖 소멸
            bullets.remove(self)
            all_sprite.remove(self)

        #ghosts와 충돌처리
        bullet_hits = pygame.sprite.spritecollide(self, ghosts, True)
        if bullet_hits:
            bullets.remove(self)
            all_sprite.remove(self)

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = []

        for i in range(0, 3):
            img = pygame.image.load("ghost"+str(i)+".png").convert()
            img.set_colorkey(black)
            self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()

class Ghost0(Ghost):
    speed = 0

    def __init__(self):
        Ghost.__init__(self)

        self.sl = random.randrange(2)  #0이면 위 1이면 아래
        if self.sl == 0:
            self.rect.y = -50
            self.speed = 5
        else:
            self.rect.y = 550
            self.speed = -5
        self.rect.x = random.randrange(50, 400)

    def update(self):
        self.rect.y += self.speed

        if self.rect.x > 600 or  self.rect.x < -100 or self.rect.y > 600 or self.rect.y < -100:   #테두리 밖 소멸
            bullets.remove(self)
            all_sprite.remove(self)

class Ghost1(Ghost):
    speed = 0

    def __init__(self):
        Ghost.__init__(self)

        self.sl = random.randrange(2)  #0이면 왼 1이면 오른
        if self.sl == 0:
            self.rect.x = -50
            self.speed = 5
            self.image = self.images[2]
        else:
            self.rect.x = 550
            self.speed = -5
            self.image = self.images[1]
        self.rect.y = random.randrange(50, 400)

    def update(self):
        self.rect.x += self.speed

        if self.rect.x > 600 or  self.rect.x < -100 or self.rect.y > 600 or self.rect.y < -100:   #테두리 밖 소멸
            bullets.remove(self)
            all_sprite.remove(self)

pygame.init()

screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Ghost Hunt")
bg = pygame.image.load("bg.png").convert()
clock = pygame.time.Clock()
font = pygame.font.Font("nanumgothic.ttf", 20)
done = False
gameover = False

player = Player()
player.rect.x = 230
player.rect.y = 370

ghosts = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()
all_sprite.add(player)

key_list = [0, 0, 0, 0]
delay = 0
ghost_list = [1, 0]

while done==False:
    now_time = time.time()
    print_time = font.render(str(int(now_time - start_time)), True, white)

    screen.blit(bg, [0, 0])
    screen.blit(print_time, [460, 5])  #버틴 시간 표시
    for event in pygame.event.get():    #조작 처리
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.set_speed(0, -5)
            if event.key == pygame.K_s:
                player.set_speed(0, 5)
            if event.key == pygame.K_a:
                player.set_speed(-5, 0)
            if event.key == pygame.K_d:
                player.set_speed(5, 0)
            if event.key == pygame.K_UP:
                key_list[0] = 1
            if event.key == pygame.K_DOWN:
                key_list[1] = 1
            if event.key == pygame.K_LEFT:
                key_list[2] = 1
            if event.key == pygame.K_RIGHT:
                key_list[3] = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.set_speed(0, 5)
            if event.key == pygame.K_s:
                player.set_speed(0, -5)
            if event.key == pygame.K_a:
                player.set_speed(5, 0)
            if event.key == pygame.K_d:
                player.set_speed(-5, 0)
            if event.key == pygame.K_UP:
                key_list[0] = 0
            if event.key == pygame.K_DOWN:
                key_list[1] = 0
            if event.key == pygame.K_LEFT:
                key_list[2] = 0
            if event.key == pygame.K_RIGHT:
                key_list[3] = 0

    if key_list.count(1) != 0 and (delay % 8 ) == 0:   #조작 처리 후 총알 처리
        if key_list[0] == 1 and key_list[2] == 1 :
            bullet = Bullet(0)
        elif key_list[0] == 1 and key_list[3] == 1 :
            bullet = Bullet(2)
        elif key_list[1] == 1 and key_list[2] == 1 :
            bullet = Bullet(5)
        elif key_list[1] == 1 and key_list[3] == 1 :
            bullet = Bullet(7)
        elif key_list[0] == 1:
            bullet = Bullet(1)
        elif key_list[1] == 1:
            bullet = Bullet(6)
        elif key_list[2] == 1:
            bullet = Bullet(3)
        elif key_list[3] == 1:
            bullet = Bullet(4)

        bullet.rect.x = player.rect.x
        bullet.rect.y = player.rect.y
        bullets.add(bullet)
        all_sprite.add(bullet)


    delay += 1

    #유령 처리
    if delay % 100 == 0:
        if round(now_time - start_time, 1) > 5: #조절요망
            ghost_list[1] = 1

        ghost0 = Ghost0()
        ghosts.add(ghost0)
        all_sprite.add(ghost0)


        if ghost_list[1] == 1:
            ghost1 = Ghost1()
            ghosts.add(ghost1)
            all_sprite.add(ghost1)

    #플레이어-유령 충돌처리
    player_hits = pygame.sprite.spritecollide(player, ghosts, False)
    if player_hits:
        all_sprite.remove(player)
        gameover = True

    if gameover == True:
        gotext = font.render("GAME OVER", True, white)
        screen.blit(gotext, [180, 250])

    all_sprite.update()
    all_sprite.draw(screen)

    pygame.display.flip()
    clock.tick(45)

pygame.quit()
