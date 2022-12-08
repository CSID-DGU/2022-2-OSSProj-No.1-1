import pygame
import os

game_main_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(game_main_dir)

class Flight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = \
            [pygame.image.load(img_dir + "/img/flight_C.png")
           , pygame.image.load(img_dir + "/img/flight_L.png")
           , pygame.image.load(img_dir + "/img/flight_LL.png")
           , pygame.image.load(img_dir + "/img/flight_R.png")
           , pygame.image.load(img_dir + "/img/flight_RR.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 4
        self.move_left = False
        self.move_right = False
        self.move_left_press = 0
        self.move_right_press = 0


    def update(self, GameMain):
        key = pygame.key.get_pressed()
        self.move_left = False
        self.move_right = False

        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.move_left = True
            self.move_left_press += 1

        if key[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
            self.move_right = True
            self.move_right_press += 1
        
        if key[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if key[pygame.K_DOWN] and\
             self.rect.y + self.rect.height < 800:
            self.rect.y += self.speed

        if self.move_left == True:
            self.move_right_press = 0
            if self.move_left_press >= 30:
                self.image = self.images[2]
            else:
                self.image = self.images[1]

        elif self.move_right == True:
            self.move_left_press = 0
            if self.move_right_press >= 30:
                self.image = self.images[4]
            else:
                self.image = self.images[3]
        else:
            self.image = self.images[0]