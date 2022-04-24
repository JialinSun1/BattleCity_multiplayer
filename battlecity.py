import pygame
import time
import random



steel_image = pygame.image.load('./img/wall/steels.gif')
wall_image = pygame.image.load('./img/wall/walls.gif')
water_image = pygame.image.load('./img/wall/water.gif')
bullet_image = pygame.image.load("./img/tankmissile.gif")
up = pygame.K_UP
down = pygame.K_DOWN
left = pygame.K_LEFT
right = pygame.K_RIGHT
fire = pygame.K_SPACE

class game():
    def __init__(self):
        self.size = (1200, 900)
        self.bg = (0, 0, 0)
        self.tanklist = pygame.sprite.Group()
        self.map = map(self)
        self.screen = pygame.display.set_mode(self.size)
        self.end = False

        self.bullet_group = pygame.sprite.Group()

    def add_tank(self, tank):
        self.tanklist.add(tank)

    def new_map(self,load=False):
        tankpos = []
        for tank in self.tanklist:
            tankpos.append(tank.rect)
        if not load:
            self.map.generate_wall(tankpos)
        self.map.add_wall()

    def new_bullet(self, tank):
        # bullet_pos = self.rect.copy()#.move(22, 22)
        
        # bullet_pos.center = (bullet_pos[0] + 30, bullet_pos[1]+30)
        b = bullet(0,0, tank)
        if tank.facing == 0:

            b = bullet(0, -2, tank)
        elif tank.facing == 1:
            b = bullet(2, 0, tank)
        elif tank.facing == 2:
            b = bullet(0, 2, tank)
        elif tank.facing == 3:
            b = bullet(-2, 0, tank)

        b.rect.center = tank.rect.copy().center
        self.bullet_group.add(b)
        # pygame.mixer.music.load('./img/fire.wav')
        # pygame.mixer.music.play(1)
    def setup(self):
        pygame.init()

        pygame.display.set_caption('Tank')
        self.screen.fill(self.bg)
        start_time = time.time()


    def run(self):
        

        # self.screen.fill(self.bg)

        # self.map.print_wall()
        for bullets in self.bullet_group:
            bullets.rect = bullets.rect.move([bullets.x, bullets.y])
        for tanks in self.tanklist:
            # tanks.print_tank()
            tanks.rect = tanks.rect.move([tanks.x, tanks.y])
            # tanks.print_bullet()
            tanks.wall_check()
            tanks.bullet_check()
        # pygame.display.flip()  
        if len(self.tanklist) <= 1: 
        #     time.sleep(5)
            
            self.end = True

class bullet(pygame.sprite.Sprite):
    def __init__(self,x ,y, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.tank = tank

class tank(pygame.sprite.Sprite):
    def __init__(self, game, pos, id='p1tank'):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.id = id
        self.imgD = pygame.image.load("./img/"+str(id)+"D.gif")
        self.imgU = pygame.image.load("./img/"+str(id)+"U.gif")
        self.imgL = pygame.image.load("./img/"+str(id)+"L.gif")
        self.imgR = pygame.image.load("./img/"+str(id)+"R.gif")
        self.image = self.imgD
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect = self.rect.inflate(-5,-5)
        print(self.rect)
        self.facing = 2


        self.x = 0
        self.y = 0
        self.keyLock = {pygame.K_DOWN:True, pygame.K_UP:True, pygame.K_LEFT:True, pygame.K_RIGHT:True}
        self.keyState = operation({pygame.K_DOWN:False, pygame.K_UP:False, pygame.K_LEFT:False, pygame.K_RIGHT:False, pygame.K_SPACE:False}, 769) 
        # if self.id =='p1tank':
        #     self.keyState = pygame.key.get_pressed()
        self.destroyed = False

    def set_facing(self, f):
        self.facing = f
        if f == 0:
            self.image = self.imgU
        elif f == 1:
            self.image = self.imgR
        elif f == 2:
            self.image = self.imgD
        elif f == 3:
            self.image = self.imgL



    def print_tank(self):
        if self.destroyed: return
        self.rect = self.rect.move([self.x, self.y])
        # self.game.screen.blit(self.image, self.rect) 

    def print_bullet(self):
        for bullet in self.game.bullet_group:
            bullet.rect = bullet.rect.move([bullet.x, bullet.y])
            # self.game.screen.blit(bullet.image, bullet.rect) 

    def move_tank(self, operation):
        # if self.id == 1:

        self.keyState = operation #operation(pygame.key.get_pressed(), event.type == 771)
        if self.keyState.KEYDOWN and self.keyState.K_SPACE and not self.destroyed:
            self.game.new_bullet(self)

        if self.destroyed:
            self.x = 0
            self.y = 0
            return
            
        # if event.type == pygame.KEYUP:
        #     ks[event.key] = False
        ks = [0, 0, 0, 0]#down, up, left, right
        if self.keyState.K_DOWN and self.keyLock[down]: ks[0] = 1 
        if self.keyState.K_UP and self.keyLock[up]: ks[1] = 1 
        if self.keyState.K_LEFT and self.keyLock[left]: ks[2] = 1 
        if self.keyState.K_RIGHT and self.keyLock[right]: ks[3] = 1 
        # print(ks)
        if ks[0] and not ks[1] and not ks[2] and not ks[3]:
            self.y = 1
            self.set_facing(2)
        if ks[1] and not ks[0] and not ks[2] and not ks[3]:
            self.y = -1
            self.set_facing(0)
        if ks[2] and not ks[0] and not ks[1] and not ks[3]:
            self.x = -1
            self.set_facing(3)
        if ks[3] and not ks[1] and not ks[2] and not ks[0]:
            self.x = 1
            self.set_facing(1)
        if not (ks[0] or ks[1]):
            self.y = 0
        if not  (ks[2] or ks[3]):
            self.x = 0


    def wall_check(self):
        self.keyLock = {pygame.K_DOWN:True, pygame.K_UP:True, pygame.K_LEFT:True, pygame.K_RIGHT:True}
        if pygame.sprite.spritecollideany(self, self.game.map.wall_group) or pygame.sprite.spritecollideany(self, self.game.map.steel_group) or pygame.sprite.spritecollideany(self, self.game.map.water_group):
            hit_wall = pygame.sprite.spritecollideany(self, self.game.map.wall_group)
            if not hit_wall: hit_wall = pygame.sprite.spritecollideany(self, self.game.map.steel_group)
            if not hit_wall: hit_wall = pygame.sprite.spritecollideany(self, self.game.map.water_group)
            if self.x > 0:
                self.rect.right = hit_wall.rect.left
                self.x = 0
                self.keyLock[pygame.K_RIGHT] = False
            if self.x < 0:
                self.rect.left = hit_wall.rect.right
                self.x = 0
                self.keyLock[pygame.K_LEFT] = False
            if self.y > 0:
                self.rect.bottom = hit_wall.rect.top
                self.y = 0
                self.keyLock[pygame.K_DOWN] = False
            if self.y < 0:
                self.rect.top = hit_wall.rect.bottom
                self.y = 0
                self.keyLock[pygame.K_UP] = False
    
    def bullet_check(self):
        pygame.sprite.groupcollide(self.game.bullet_group, self.game.map.steel_group, True, False)
            # pygame.mixer.music.load('./img/hit.wav')
            # pygame.mixer.music.play(1)
        pygame.sprite.groupcollide(self.game.bullet_group, self.game.map.wall_group, True, True)
            # pygame.mixer.music.load('./img/blast.wav')
            # pygame.mixer.music.play(1)

        for tanks in self.game.tanklist:
            if tanks == self:
                continue
            elif pygame.sprite.spritecollideany(tanks, self.game.bullet_group):
                bullets = pygame.sprite.spritecollideany(tanks, self.game.bullet_group)
                if tanks != bullets.tank:
                    tanks.destroyed = True
                    self.game.tanklist.remove(tanks)
                    self.game.bullet_group.remove(bullets)
                # pygame.mixer.music.load('./img/blast.wav')
                # pygame.mixer.music.play(1)  

    def destroy(self):
        self.destroyed = True


class wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = wall_image
        self.rect = self.image.get_rect()

class steel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = steel_image
        self.rect = self.image.get_rect()

class water(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = water_image
        self.rect = self.image.get_rect()

class map():
    def __init__(self, game, id=0):
        self.wall_group = pygame.sprite.Group()
        self.steel_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.wall_rectlist = []
        self.steel_rectlist = []
        self.water_rectlist = []
        self.game = game


    def add_wall(self):
        for rect in self.wall_rectlist:
            wall1 = wall()
            wall1.rect.topleft = rect
            self.wall_group.add(wall1)
        for rect in self.steel_rectlist:
            steel1 = steel()
            steel1.rect.topleft = rect
            self.steel_group.add(steel1)
        for rect in self.water_rectlist:
            water1 = water()
            water1.rect.topleft = rect
            self.water_group.add(water1)
        
            

    def generate_wall(self, tankposes):

        for p in range(0, 20):
            self.steel_rectlist.append((p *60, 0))
            self.steel_rectlist.append((p *60, 14 * 60))

        for q in range(0, 15):
            self.steel_rectlist.append((0 *60, q * 60))
            self.steel_rectlist.append((19 *60, q * 60))

        for i in range(1, 19):
            for j in range (1, 14):
                k = random.random()
                for tankpos in tankposes:
                    if abs(i - tankpos[0] / 60) < 2 and abs(j - tankpos[1] / 60) < 2:
                        k = 1
                if k < 0.1:
                    self.steel_rectlist.append((i *60, j *60))                
                elif k < 0.3:
                    self.water_rectlist.append((i *60, j *60)) 
                elif k < 0.5:
                    self.wall_rectlist.append((i *60, j *60))              

    def print_wall(self):
        for wall in self.wall_group:
            self.game.screen.blit(wall.image, wall.rect)
        for steel in self.steel_group:
            self.game.screen.blit(steel.image, steel.rect)
        for water in self.water_group:
            self.game.screen.blit(water.image, water.rect)

class operation():
    def __init__(self, key_pressed, KEYDOWN):
        self.K_UP = key_pressed[pygame.K_UP]
        self.K_DOWN = key_pressed[pygame.K_DOWN]
        self.K_LEFT = key_pressed[pygame.K_LEFT]
        self.K_RIGHT = key_pressed[pygame.K_RIGHT]
        self.K_SPACE = key_pressed[pygame.K_SPACE]
        self.KEYDOWN = KEYDOWN
