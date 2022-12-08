import pygame
import os
from game_player import Flight
from game_enemy import Enemy

pygame.init()
screen = pygame.display.set_mode([700, 800])
pygame.display.set_caption("Bullet Hell")

game_main_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(game_main_dir)

class GameMain():
    def __init__(self):
        self.screen = screen
        self.flight = None
        self.flight_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

    def play(self, GameMain):
        clock = pygame.time.Clock()
        running = True

        self.flight = Flight(400, 600)
        enemy = Enemy(100, 300)
        enemy2 = Enemy(200, 200)
        enemy3 = Enemy(300, 100)
        enemy4 = Enemy(400, 100)
        enemy5 = Enemy(500, 200)
        enemy6 = Enemy(600, 300)

        self.enemy_group.add(enemy)
        self.enemy_group.add(enemy2)
        self.enemy_group.add(enemy3)
        self.enemy_group.add(enemy4)
        self.enemy_group.add(enemy5)
        self.enemy_group.add(enemy6)
        
        self.flight_group.add(self.flight)

        while running:
            clock.tick(60)
            screen.fill([0,0,0])

            self.enemy_group.draw(screen)
            self.enemy_group.update(GameMain)
            
            self.flight_group.draw(screen)
            self.flight_group.update(GameMain)

            self.bullet_group.draw(screen)
            self.bullet_group.update(GameMain)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.update()


if __name__ == "__main__":
    gameMain = GameMain()
    gameMain.play(gameMain)
    pygame.quit()
