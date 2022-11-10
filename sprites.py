import pygame
import random
import math
from load import load_image
from pygame.locals import *

### pygame.sprite.Sprite 자식 클래스 
### -> MasterSprite, Bomb 
freq = 1 / 20
siney_move = 3
roundy_move = 2
explosion_linger = 12
spikey_slope = range(-3, 4)
spikey_interval = 4
spikey_period = range(10, 41)
fasty_movefunc = 3

scr_size = 500

class size :
    update = scr_size*0.008
    radius = scr_size*0.04
    middle = scr_size // 2
    speed = scr_size*0.002
    masterspritespeed = scr_size*0.004
    lives = scr_size*0.06
    crawly = scr_size*0.006
    x_background = scr_size*1
    right = x_background*0.6

def get_size() :
    global user_size, level_size, scr_size
    size.update = scr_size*0.008
    size.radius = scr_size*0.04
    size.middle = scr_size // 2
    size.speed = scr_size*0.002
    size.masterspritespeed = scr_size*0.004
    size.lives = scr_size*0.06
    size.crawly = scr_size*0.006

    size.x_background = scr_size*2
    size.right = size.x_background*0.6

class MasterSprite(pygame.sprite.Sprite):
    ### 자식 클래스들 : Explosion, Missile, Powerup(<- BombPowerup, ShieldPowerup),
    ###              Ship, Alien 
    allsprites = None
    speed = None


class Explosion(MasterSprite): 
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self):
        super().__init__()
        self.image, self.rect = load_image('explosion.png', -1)
        self.linger = MasterSprite.speed * 3

    @classmethod
    def position(cls, loc):
        if len(cls.pool) > 0:
            explosion = cls.pool.sprites()[0]
            explosion.add(cls.active, cls.allsprites)
            explosion.remove(cls.pool)
            explosion.rect.center = loc
            explosion.linger = 12

    def update(self):
        self.linger -= 1
        if self.linger <= 0:
            self.remove(self.allsprites, self.active)
            self.add(self.pool)
        
        
########### kirin 추가
class Kirin(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('kirin.png', -1)
        self.original = self.image
        self.shield, self.rect = load_image('kirin_shield.png', -1)
        self.fart, self.rect = load_image('kirin_bomb.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 400) # 비율 변동
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.rect.midbottom = (self.screen.get_width() // 2, self.area.bottom)
        self.radius = max(self.rect.width, self.rect.height)
        self.alive = True
        self.shieldUp = False
        self.fartNow = False
        self.vert = 0
        self.horiz = 0
        self.life = 3

    def initializeKeys(self):
        keyState = pygame.key.get_pressed()
        self.vert = 0
        self.horiz = 0
        if keyState[pygame.K_w]:
            self.vert -= 2 * MasterSprite.speed
        if keyState[pygame.K_a]:
            self.horiz -= 2 * MasterSprite.speed
        if keyState[pygame.K_s]:
            self.vert += 2 * MasterSprite.speed
        if keyState[pygame.K_d]:
            self.horiz += 2 * MasterSprite.speed

    def update(self, screen_size): 
        self.screen_size = screen_size
        newpos = self.rect.move((self.horiz, self.vert))
        newhoriz = self.rect.move((self.horiz, 0))
        newvert = self.rect.move((0, self.vert))

        if not (newpos.left <= self.area.left
                or newpos.top <= self.area.top
                or newpos.right >= self.area.right
                or newpos.bottom >= self.area.bottom):
            self.rect = newpos
        elif not (newhoriz.left <= self.area.left
                  or newhoriz.right >= self.area.right):
            self.rect = newhoriz
        elif not (newvert.top <= self.area.top
                  or newvert.bottom >= self.area.bottom):
            self.rect = newvert

        if self.shieldUp and self.image != self.shield:
            self.image = self.shield

        if self.fartNow and self.image == self.original:
            self.image = self.fart

        if (not self.shieldUp or not self.fartNow) and self.image != self.original:
            self.image = self.original


    def bomb(self):
        return Bomb(self)

class Friendkirin(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('friendkirin.png', -1)
        self.original = self.image
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.radius = max(self.rect.width, self.rect.height)
   
    def remove(self) :
        pygame.sprite.Sprite.kill(self)

class Kirin2(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('ship.png', -1)
        self.original = self.image
        self.shield, self.rect = load_image('kirin_shield.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.rect.midbottom = (self.screen.get_width() * (1/4) , self.area.bottom)
        self.radius = max(self.rect.width, self.rect.height)
        self.alive = True
        self.shieldUp = False
        self.vert = 0
        self.horiz = 0
        self.life = 3   

    def initializeKeys(self):
        keyState = pygame.key.get_pressed()
        self.vert = 0
        self.horiz = 0

    def update(self, screen_size):
        self.screen_size = screen_size
        newpos = self.rect.move((self.horiz, self.vert))
        newhoriz = self.rect.move((self.horiz, 0))
        newvert = self.rect.move((0, self.vert))

        if not (newpos.left <= self.area.left
                or newpos.top <= self.area.top
                or newpos.right >= (self.area.width / 2)
                or newpos.bottom >= self.area.bottom):
            self.rect = newpos
        elif not (newhoriz.left <= self.area.left
                  or newhoriz.right >= (self.area.width / 2)):
            self.rect = newhoriz
        elif not (newvert.top <= self.area.top
                  or newvert.bottom >= self.area.bottom):
            self.rect = newvert

        if self.shieldUp and self.image != self.shield:
            self.image = self.shield

        if not self.shieldUp and self.image != self.original:
            self.image = self.original

    def bomb(self):
        return Bomb(self)

class Kirin3(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('ship.png', -1)
        self.original = self.image
        self.shield, self.rect = load_image('kirin_shield.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.rect.midbottom = (self.screen.get_width() * (3/4), self.area.bottom)
        self.radius = max(self.rect.width, self.rect.height)
        self.alive = True
        self.shieldUp = False
        self.vert = 0
        self.horiz = 0
        self.life = 3 

    def initializeKeys(self):
        keyState = pygame.key.get_pressed()
        self.vert = 0
        self.horiz = 0

    def update(self, screen_size):
        self.screen_size = screen_size
        newpos = self.rect.move((self.horiz, self.vert))
        newhoriz = self.rect.move((self.horiz, 0))
        newvert = self.rect.move((0, self.vert))

        if not (newpos.left <= (self.area.width / 2)
                or newpos.top <= self.area.top
                or newpos.right >= self.area.right
                or newpos.bottom >= self.area.bottom):
            self.rect = newpos
        elif not (newhoriz.left <= (self.area.width / 2)
                  or newhoriz.right >= self.area.right):
            self.rect = newhoriz
        elif not (newvert.top <= self.area.top
                  or newvert.bottom >= self.area.bottom):
            self.rect = newvert

        if self.shieldUp and self.image != self.shield:
            self.image = self.shield

        if not self.shieldUp and self.image != self.original:
            self.image = self.original

    def bomb(self):
        return Bomb(self)

class Bear(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self, trait, screen_size):
        super().__init__()
        self.image, self.rect = load_image(
            'bear_' + trait + '.png', -1)
        self.initialRect = self.rect
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.loc = 0
        self.radius = min(self.rect.width // 2, self.rect.height // 2)

    @classmethod
    def position(cls):
        if len(cls.pool) > 0 and cls.numOffScreen > 0:
            bear = random.choice(cls.pool.sprites())
            if isinstance(bear, Panda):
                bear.rect.midbottom = (random.choice(
                    (bear.area.left, bear.area.right)),
                    random.randint(
                    (bear.area.bottom * 3) // 4,
                    bear.area.bottom))
            else:
                bear.rect.midtop = (random.randint(
                    bear.area.left
                    + bear.rect.width // 2,
                    bear.area.right
                    - bear.rect.width // 2),
                    bear.area.top)
            bear.initialRect = bear.rect
            bear.loc = 0
            bear.add(cls.allsprites, cls.active)
            bear.remove(cls.pool)
            Bear.numOffScreen -= 1

    def update(self, screen_size):
        self.screen_size = screen_size
        horiz, vert = self.moveFunc()
        if horiz + self.initialRect.x > self.screen_size:
            horiz -= self.screen_size + self.rect.width
        elif horiz + self.initialRect.x < 0 - self.rect.width:
            horiz += self.screen_size + self.rect.width
        self.rect = self.initialRect.move((horiz, self.loc + vert))
        self.loc = self.loc + MasterSprite.speed
        if self.rect.top > self.area.bottom:
            self.table()
            Bear.numOffScreen += 1

    def table(self):
        self.kill()
        self.add(self.pool)


class Green(Bear):
    def __init__(self, screen_size):
        super().__init__('green',screen_size)
        self.amp = random.randint(self.rect.width, 3.5 * self.rect.width) ## 적 좌우 움직임 변동
        self.freq = (1 / 20)
        self.moveFunc = lambda: (self.amp * math.sin(self.loc * self.freq), 0)
        self.pType = 'green'


class Sunglasses(Bear):
    def __init__(self, screen_size):
        super().__init__('sunglasses',screen_size)
        self.amp = random.randint(self.rect.width, 2 * self.rect.width)
        self.freq = 1 / (25) # 원 움직임 변동 횟수 늘리기
        self.moveFunc = lambda: (
            self.amp *
            math.sin(
                self.loc *
                self.freq),
            self.amp *
            math.cos(
                self.loc *
                self.freq))
        self.pType = 'sunglasses'


class Brown(Bear):
    def __init__(self, screen_size):
        super().__init__('brown',screen_size)
        self.slope = random.choice(list(x for x in range(-3, 3) if x != 0)) # 범위 -3 ~ 3이 게임 진행에 있어 안정적
        self.period = random.choice(list(4 * x for x in range(15, 41))) # 기본 적의 좌우 움직이는 주기 start를 늘림
        self.moveFunc = lambda: (self.slope * (self.loc % self.period)
                                 if self.loc % self.period < self.period // 2
                                 else self.slope * self.period // 2
                                 - self.slope * ((self.loc % self.period)
                                 - self.period // 2), 0)
        self.pType = 'brown'


class Stone(Bear):
    def __init__(self, screen_size):
        super().__init__('stone',screen_size)
        self.moveFunc = lambda: (0, 1.5 * self.loc)
        self.pType = 'stone'


class Panda(Bear):
    def __init__(self, screen_size):
        super().__init__('panda',screen_size)
        self.moveFunc = lambda: (self.loc, 0)
        self.pType = 'panda'

    def update(self, screen_size):
        horiz, vert = self.moveFunc()
        horiz = (-horiz if self.initialRect.center[0] == self.area.right
                 else horiz)
        if (horiz + self.initialRect.left > self.area.right
                or horiz + self.initialRect.right < self.area.left):
            self.table()
            Bear.numOffScreen += 1
        self.rect = self.initialRect.move((horiz, vert))
        self.loc = self.loc + MasterSprite.speed
        
class Explosion(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('explosion.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.linger = MasterSprite.speed * 3

    @classmethod
    def position(cls, loc):
        if len(cls.pool) > 0:
            explosion = cls.pool.sprites()[0]
            explosion.add(cls.active, cls.allsprites)
            explosion.remove(cls.pool)
            explosion.rect.center = loc
            explosion.linger = 12

    def update(self, screen_size):
        self.screen_size = screen_size
        self.linger -= 1
        if self.linger <= 0:
            self.remove(self.allsprites, self.active)
            self.add(self.pool)


class Leaf(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('leaf.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()

    @classmethod
    def position(cls, loc):
        if len(cls.pool) > 0:
            leaf = cls.pool.sprites()[0]
            leaf.add(cls.allsprites, cls.active)
            leaf.remove(cls.pool)
            leaf.rect.midbottom = loc
    
    def table(self):
        self.add(self.pool)
        self.remove(self.allsprites, self.active)

    def update(self, screen_size):
        self.screen_size = screen_size
        newpos = self.rect.move(0, -4 * MasterSprite.speed)
        self.rect = newpos
        if self.rect.top < self.area.top:
            self.table()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, kirin):
        super().__init__()
        self.image = None
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.radius = 20
        self.radiusIncrement = 4
        self.rect = kirin.rect

    def update(self):
        self.radius += self.radiusIncrement
        pygame.draw.circle(
            pygame.display.get_surface(),
            pygame.Color(153, 76, 0, 128),
            self.rect.center, self.radius, 3)
        if (self.rect.center[1] - self.radius <= self.area.top
            and self.rect.center[1] + self.radius >= self.area.bottom
            and self.rect.center[0] - self.radius <= self.area.left
                and self.rect.center[0] + self.radius >= self.area.right):
            self.kill()


class Powerup(MasterSprite):
    def __init__(self, kindof, screen_size):
        super().__init__()
        self.image, self.rect = load_image(kindof + '_powerup.png', -1)
        self.original = self.image
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.rect.midtop = (random.randint(
                            self.area.left + self.rect.width // 2,
                            self.area.right - self.rect.width // 2),
                            self.area.top)
        self.angle = 0

    def update(self, screen_size):
        self.screen_size = screen_size
        center = self.rect.center
        self.angle = (self.angle + 2) % 360
        rotate = pygame.transform.rotate
        self.image = rotate(self.original, self.angle)
        self.rect = self.image.get_rect(
            center=(
                center[0],
                center[1] +
                MasterSprite.speed))


class BombPowerup(Powerup):
    def __init__(self, screen_size):
        super().__init__('bomb', screen_size)
        self.pType = 'bomb'


class ShieldPowerup(Powerup):
    def __init__(self, screen_size):
        super().__init__('shield', screen_size)
        self.pType = 'shield'

class DoubleleafPowerup(Powerup):
    def __init__(self, screen_size):
        super().__init__('doubleleaf', screen_size)
        self.pType = 'doubleleaf'

class FriendPowerup(Powerup):
    def __init__(self, screen_size):
        super().__init__('friendkirin', screen_size)
        self.pType = 'friendkirin'

class LifePowerup(Powerup):
    def __init__(self, screen_size):
        super().__init__('life', screen_size)
        self.pType = 'life'