import pygame
import os
import math
import random
import uuid
from game_bullet import HomingLaserHeader

game_main_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(game_main_dir)

TURRET_STOP = 0
TURRET_OPEN = 1
TURRET_FIRE = 2
TURRET_WAIT = 3
TURRET_CLOSE = 4

class Enemy(pygame.sprite.Sprite):    
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = \
            [pygame.image.load(img_dir + "/img/laser_turret_01.png")
            ,pygame.image.load(img_dir + "/img/laser_turret_02.png")
            ,pygame.image.load(img_dir + "/img/laser_turret_03.png")
            ,pygame.image.load(img_dir + "/img/laser_turret_04.png")
            ,pygame.image.load(img_dir + "/img/laser_turret_05.png")
            ,pygame.image.load(img_dir + "/img/laser_turret_06.png")
            ]
        self.image = self.images[0]
        self.image_idx = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 4
        self.x = x
        self.y = y
        self.theta = 0
        self.angle = 0        
        self.animation_frame = 0
        self.animation_interval = 5
        self.fire_frame = 0
        self.fire_delay_frame = random.randint(200, 300)
        self.aiming = True
        # 0:애니메이션 없음, 1: 포열 여는 애니메이션, 2: 레이저 발사, 3:발사 후 대기, 4:포열을 닫는 애니메이션
        self.turret_status = TURRET_STOP
        self.id = uuid.uuid4()

    def update(self, GameMain):
        self.fire_frame += 1        
        self.animation_frame += 1
        ty = GameMain.flight.rect.centery
        sy = self.rect.centery
        tx = GameMain.flight.rect.centerx
        sx = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

        if self.turret_status == TURRET_OPEN:
            inc = 1
        elif self.turret_status == TURRET_CLOSE:
            inc = -1
        else:
            inc = 0
        
        if self.fire_frame >= self.fire_delay_frame:
            if self.animation_frame >= self.animation_interval:
                self.image_idx += inc
                self.animation_frame = 0
                if self.turret_status == TURRET_STOP:
                    self.turret_status = 1
                elif self.turret_status == TURRET_FIRE:
                    self.createBullet(GameMain.bullet_group, sx, sy, tx, ty, 15, self.speed)
                    self.turret_status = TURRET_WAIT
                    self.animation_frame = -30
                elif self.turret_status == TURRET_WAIT:
                    self.turret_status = TURRET_CLOSE

                if self.image_idx > 5:
                    self.image_idx = 5
                    self.turret_status = TURRET_FIRE
                elif self.image_idx < 0:
                    self.image_idx = 0
                    self.turret_status = TURRET_STOP
                    self.fire_frame = 0
        
        self.image = self.images[self.image_idx]
    

    def createBullet(self, bullet_group, sx, sy, tx, ty, theta, speed):
        tx = sx - random.randint(50, 100)
        ty = sy - random.randint(50, 100)
        enemyBullet = HomingLaserHeader(sx, sy, tx, ty, 0, speed)
        bullet_group.add(enemyBullet)
