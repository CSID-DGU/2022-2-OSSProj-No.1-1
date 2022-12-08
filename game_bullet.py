import pygame
import os
import math

game_main_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(game_main_dir)

class HomingLaserHeader(pygame.sprite.Sprite):
    def __init__(self, sx, sy, tx, ty, rad, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img_dir + "/data/homing_laser_01.png").convert_alpha()
        self.speed = 1
        self.max_speed = 8
        self.angle = math.atan2(ty - sy, tx - sx)
        self.rect = self.image.get_rect()
        self.rect.center = [sx, sy]
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.x = sx
        self.y = sy
        self.tracking = True

    def update(self, Extreme):
        if self.tracking:
            extreme = Extreme()            
            tx = extreme.player.rect.x
            ty = extreme.player.rect.y
            sx = self.rect.x
            sy = self.rect.y
            self.angle = math.atan2(ty - sy, tx - sx)
            self.dx = math.cos(self.angle) * self.speed
            self.dy = math.sin(self.angle) * self.speed            

        if (self.rect.y > extreme.player.rect.y - 60 and self.rect.y < extreme.player.rect.y + 60) and \
            (self.rect.x > extreme.player.rect.x - 60 and self.rect.x < extreme.player.rect.x + 60):            
            self.dx = math.cos(self.angle) * self.max_speed
            self.dy = math.sin(self.angle) * self.max_speed
            self.tracking = False
        
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        if self.max_speed > self.speed:
            self.speed += 0.3

        homingLaserShadow = HomingLaserTail(self.x, self.y)
        extreme.bullet_group.add(homingLaserShadow)

        if self.rect.y < -100:
            self.kill()
        elif self.rect.y > 900:
            self.kill()
        elif self.rect.x < -100:
            self.kill()
        elif self.rect.x > 900:
            self.kill()

class HomingLaserTail(pygame.sprite.Sprite):
    def __init__(self, sx, sy):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(img_dir + "/data/homing_laser_01.png").convert_alpha()
                     , pygame.image.load(img_dir + "/data/homing_laser_02.png").convert_alpha()
                     , pygame.image.load(img_dir + "/data/homing_laser_03.png").convert_alpha()
                     , pygame.image.load(img_dir + "/data/homing_laser_04.png").convert_alpha()
                     , pygame.image.load(img_dir + "/data/homing_laser_05.png").convert_alpha()
                      ]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [sx, sy]
        self.count = 0

    def update(self, Extreme):
        self.count += 1        
        if self.count <= 5:
            self.image = self.images[0]
        elif self.count <= 10:
            self.image = self.images[1]
        elif self.count <= 15:
            self.image = self.images[2]
        elif self.count <= 20:
            self.image = self.images[3]
        elif self.count <= 25:
            self.image = self.images[4]
        else:
            self.kill()