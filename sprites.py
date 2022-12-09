import pygame
import random
import math
import uuid
from numpy import sqrt 
from load import load_image,Var
from pygame.locals import *
from sys import *
import os

game_main_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(game_main_dir)

TURRET_STOP = 0
TURRET_OPEN = 1
TURRET_FIRE = 2
TURRET_WAIT = 3
TURRET_CLOSE = 4
    
class MasterSprite(pygame.sprite.Sprite):
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
        
        
## Player 추가
class Player(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image(Var.lst[0], -1) # 캐릭터 이미지
        self.original = self.image
        self.shield, self.rect = load_image('ship_shield.png', -1) # 쉴드 상태 캐릭터 이미지
        self.fart, self.rect = load_image('explosion.png', -1) # 폭탄 상태 캐릭터 이미지
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
        self.speed = None
        self.org_speed = self.speed

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
    
    def speedUp(self):
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_w]:
            self.vert -= 2 * self.speed
        if keyState[pygame.K_a]:
            self.horiz -= 2 * self.speed
        if keyState[pygame.K_s]:
            self.vert += 2 * self.speed
        if keyState[pygame.K_d]:
            self.horiz += 2 * self.speed
            
        newpos = self.rect.move((self.horiz, self.vert))
        newhoriz = self.rect.move((self.horiz, 0))
        newvert = self.rect.move((0, self.vert))

class FriendShip(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('friendShip.png', -1)
        self.original = self.image
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 400)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.radius = max(self.rect.width, self.rect.height)
   
    def remove(self) :
        pygame.sprite.Sprite.kill(self)


class FriendShip(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('friendShip.png', -1)
        self.original = self.image
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 400)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect()
        self.radius = max(self.rect.width, self.rect.height)
   
    def remove(self) :
        pygame.sprite.Sprite.kill(self)

class Player2(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image(Var.lst[0], -1)
        self.original = self.image
        self.shield, self.rect = load_image('ship_shield.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 400)
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

class Player3(MasterSprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('ship.png', -1)
        self.original = self.image
        self.shield, self.rect = load_image('ship_shield.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 400)
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



class Monster(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self, trait, screen_size):
        super().__init__()
        self.image, self.rect = load_image(
            trait + '.png', -1)
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
            monster = random.choice(cls.pool.sprites())
            if isinstance(monster, Blue):
                monster.rect.midbottom = (random.choice(
                    (monster.area.left, monster.area.right)),
                    random.randint(
                    (monster.area.bottom * 3) // 4,
                    monster.area.bottom))
            else:
                monster.rect.midtop = (random.randint(
                    monster.area.left
                    + monster.rect.width // 2,
                    monster.area.right
                    - monster.rect.width // 2),
                    monster.area.top)
            monster.initialRect = monster.rect
            monster.loc = 0
            monster.add(cls.allsprites, cls.active)
            monster.remove(cls.pool)
            monster.numOffScreen -= 1

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
            Monster.numOffScreen += 1

    def table(self):
        self.kill()
        self.add(self.pool)

class Green(Monster):
    def __init__(self, screen_size):
        super().__init__('green',screen_size)
        self.amp = random.randint(self.rect.width, 3.5 * self.rect.width) ## 적 좌우 움직임 변동
        self.freq = (1 / 20)
        self.moveFunc = lambda: (self.amp * math.sin(self.loc * self.freq), 0)
        self.pType = 'green'


class Pink(Monster):
    def __init__(self, screen_size):
        super().__init__('pink',screen_size)
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
        self.pType = 'pink'


class Yellow(Monster):
    def __init__(self, screen_size):
        super().__init__('yellow',screen_size)
        self.slope = random.choice(list(x for x in range(-3, 3) if x != 0)) # 범위 -3 ~ 3이 게임 진행에 있어 안정적
        self.period = random.choice(list(4 * x for x in range(15, 41))) # 기본 적의 좌우 움직이는 주기 start를 늘림
        self.moveFunc = lambda: (self.slope * (self.loc % self.period)
                                 if self.loc % self.period < self.period // 2
                                 else self.slope * self.period // 2
                                 - self.slope * ((self.loc % self.period)
                                 - self.period // 2), 0)
        self.pType = 'yellow'


class Grey(Monster):
    def __init__(self, screen_size):
        super().__init__('grey',screen_size)
        self.moveFunc = lambda: (0, 1.5 * self.loc)
        self.pType = 'grey'


class Blue(Monster):
    def __init__(self, screen_size):
        super().__init__('blue',screen_size)
        self.moveFunc = lambda: (self.loc, 0)
        self.pType = 'blue'

    def update(self, screen_size):
        horiz, vert = self.moveFunc()
        horiz = (-horiz if self.initialRect.center[0] == self.area.right
                 else horiz)
        if (horiz + self.initialRect.left > self.area.right
                or horiz + self.initialRect.right < self.area.left):
            self.table()
            Monster.numOffScreen += 1
        self.rect = self.initialRect.move((horiz, vert))
        self.loc = self.loc + MasterSprite.speed
        
class Boss(Monster):
    def __init__(self, screen_size):
        super().__init__('boss', screen_size)
        self.amp = random.randint(self.rect.width, self.rect.width)
        self.freq = 1 / (35) # 원 움직임 변동 횟수 늘리기
        self.moveFunc = lambda: (
            self.amp *
            math.sin(
                self.loc *
                self.freq),
            self.amp *
            math.cos(
                self.loc *
                self.freq))
        self.pType = 'boss'
        self.health = 10
    
    def update(self, screen_size):
        horiz, vert = self.moveFunc()
        horiz = (-horiz if self.initialRect.center[0] == self.area.right
                 else horiz)
        if (horiz + self.initialRect.left > self.area.right
                or horiz + self.initialRect.right < self.area.left):
            self.table()
            Monster.numOffScreen += 1
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

## Power
class Beam(MasterSprite): 
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self, screen_size):
        super().__init__()
        self.image, self.rect = load_image('beam.png', -1)
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.area = self.screen.get_rect() 
        self.speed = 1


    @classmethod
    def position(cls, loc):
        if len(cls.pool) > 0:
            beam = cls.pool.sprites()[0]
            beam.add(cls.allsprites, cls.active)
            beam.remove(cls.pool)
            beam.rect.midbottom = loc
            
    @classmethod
    def position2(cls, loc):
        if len(cls.pool) > 0:
            beam = cls.pool.sprites()[0]
            beam.add(cls.allsprites, cls.active)
            beam.remove(cls.pool)
            beam.rect.bottom = loc
    
    def table(self):
        self.add(self.pool)
        self.remove(self.allsprites, self.active)

    def update(self, screen_size):
        self.screen_size = screen_size
        newpos = self.rect.move(0, -4.5 * self.speed)
        self.rect = newpos
        if self.rect.top < self.area.top:
            self.table()
            
        

class Bomb(pygame.sprite.Sprite):
    def __init__(self, Player):
        super().__init__()
        self.image = None
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.radius = 20
        self.radiusIncrement = 4
        self.rect = Player.rect

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


class Power(MasterSprite): # 쉴드, 폭탄, 하트, Friend(헬퍼)
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


class BombPower(Power):
    def __init__(self, screen_size):
        super().__init__('bomb', screen_size)
        self.pType = 'bomb'


class ShieldPower(Power):
    def __init__(self, screen_size):
        super().__init__('shield', screen_size)
        self.pType = 'shield'

class DoublebeamPower(Power):
    def __init__(self, screen_size):
        super().__init__('doublebeam', screen_size)
        self.pType = 'doublebeam'

class FriendPower(Power):
    def __init__(self, screen_size):
        super().__init__('friendShip', screen_size)
        self.pType = 'friendShip'

class LifePower(Power):
    def __init__(self, screen_size):
        super().__init__('life', screen_size)
        self.pType = 'life'
        
class TriplecupcakePower(Power):
    def __init__(self, screen_size):
        super().__init__('triplecupcake', screen_size)
        self.pType = 'triplecupcake'

class BroccoliBeamfast(Power):
    def __init__(self, screen_size):
        super().__init__('broccoli', screen_size)
        self.pType = 'broccoli'
        
# Extreme mode Monsters
class Monster2(MasterSprite):
    pool = pygame.sprite.Group()
    active = pygame.sprite.Group()

    def __init__(self, trait, screen_size):
        super().__init__()
        self.image, self.rect = load_image(
            trait + '.png', -1)
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
            monster = random.choice(cls.pool.sprites())
            if isinstance(monster, Blue2):
                monster.rect.midbottom = (random.choice(
                    (monster.area.left, monster.area.right)),
                    random.randint(
                    monster.area.centery, monster.area.bottom))
            elif isinstance(monster, Blue3):
                monster.rect.midtop = (random.choice(
                    (monster.area.left, monster.area.right)),
                    random.randint(
                    monster.area.top, monster.area.centery))
            else:
                monster.rect.midtop = (random.randint(
                    monster.area.left
                    + monster.rect.width // 2,
                    monster.area.right
                    - monster.rect.width // 2),
                    monster.area.top)
            monster.initialRect = monster.rect
            monster.loc = 0
            monster.add(cls.allsprites, cls.active)
            monster.remove(cls.pool)
            monster.numOffScreen -= 1

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
            Monster2.numOffScreen += 1

    def table(self):
        self.kill()
        self.add(self.pool)

# Blue (left, right)
# Green, Yellow (Top)
# Pink (Bottom)

class Green2(Monster2):
    def __init__(self, screen_size):
        super().__init__('green',screen_size)
        self.amp = random.randint(self.rect.width, 3.5 * self.rect.width) ## 적 좌우 움직임 변동
        self.freq = (1 / 20)
        self.moveFunc = lambda: (self.amp * math.sin(self.loc * self.freq), 0)
        self.pType = 'green2'


class Pink2(Monster2):
    def __init__(self, screen_size):
        super().__init__('pink',screen_size)
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
        self.pType = 'pink2'


class Yellow2(Monster2):
    def __init__(self, screen_size):
        super().__init__('yellow',screen_size)
        self.slope = random.choice(list(x for x in range(-3, 3) if x != 0)) # 범위 -3 ~ 3이 게임 진행에 있어 안정적
        self.period = random.choice(list(4 * x for x in range(15, 41))) # 기본 적의 좌우 움직이는 주기 start를 늘림
        self.moveFunc = lambda: (self.slope * (self.loc % self.period)
                                 if self.loc % self.period < self.period // 2
                                 else self.slope * self.period // 2
                                 - self.slope * ((self.loc % self.period)
                                 - self.period // 2), 0)
        self.pType = 'yellow2'


class Grey2(Monster2):
    def __init__(self, screen_size):
        super().__init__('grey',screen_size)
        self.moveFunc = lambda: (0, 1.5 * self.loc)
        self.pType = 'grey2'

# Blue (bottomleft, bottomright)
class Blue2(Monster2):
    def __init__(self, screen_size):
        super().__init__('blue',screen_size)
        self.moveFunc = lambda: (1.8 * self.loc, 0)
        self.pType = 'blue2'

    def update(self, screen_size):
        horiz, vert = self.moveFunc()
        horiz = (-horiz if self.initialRect.center[0] == self.area.right
                 else horiz)
        if (horiz + self.initialRect.left > self.area.right
                or horiz + self.initialRect.right < self.area.left):
            self.table()
            Monster2.numOffScreen += 1
        self.rect = self.initialRect.move((horiz, vert))
        self.loc = self.loc + MasterSprite.speed        
        
# Blue (topleft, topright)
class Blue3(Monster2):
    def __init__(self, screen_size):
        super().__init__('blue',screen_size)
        self.moveFunc = lambda: (1.8 * self.loc, 0)
        self.pType = 'blue3'

    def update(self, screen_size):
        horiz, vert = self.moveFunc()
        horiz = (-horiz if self.initialRect.center[0] == self.area.right
                 else horiz)
        if (horiz + self.initialRect.left > self.area.right
                or horiz + self.initialRect.right < self.area.left):
            self.table()
            Monster2.numOffScreen += 1
        self.rect = self.initialRect.move((horiz, vert))
        self.loc = self.loc + MasterSprite.speed    
