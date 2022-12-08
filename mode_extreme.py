import pygame
import os
import sys
from pygame.locals import *
from game_player import Flight
from game_enemy import Enemy
from sprites import (MasterSprite, EPlayer, Enemy)
from database import Database
from load import load_image, load_sound, load_music,Var
from menu import *

pygame.init()
screen = pygame.display.set_mode([700, 800])
pygame.display.set_caption("Bullet Hell")

game_main_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(game_main_dir)


if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0
SINGLE = 0

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

class Extreme():
    def __init__(self):
        self.player = EPlayer(400, 600, 600)
        self.bullet_group = pygame.sprite.Group()
    
    def playGame(self, screen_size):
    # Initialize everything
        pygame.mixer.pre_init(11025, -16, 2, 512)
        pygame.init()
        ratio = (screen_size / 400)
        screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.set_caption("Let's Play!")
        pygame.mouse.set_visible(0)
        
    # Prepare background image
        # Game field
        field1, field1Rect = load_image("field.png")
        field2, field2Rect = load_image("field.png")
        field1Rect.midtop = screen.get_rect().midtop
        field2Rect.midbottom = field1Rect.midtop

        # pause
        pause,pauseRect = load_image('pause.png')
        pause = pygame.transform.scale(pause, (600, 600))
        pauseRect.midtop = screen.get_rect().midtop
        pauseMenu = False

    # Prepare game contents
        # life
        life1, life1Rect = load_image('heart1.png')
        life2, life2Rect = load_image('heart2.png')
        life3, life3Rect = load_image('heart3.png')
        
    # Sounds
        missile_sound = load_sound('missile.ogg')
        bomb_sound = load_sound('bomb.ogg')
        alien_explode_sound = load_sound('alien_explode.ogg')
        ship_explode_sound = load_sound('ship_explode.ogg')
        load_music('music_loop.ogg')
        soundFX = Database().getSound()
        
        # font
        font = pygame.font.Font("LeeSeoyun.ttf", round(20*ratio))
        beforeWaveCountFont = pygame.font.Font(None, 60)
        leftCountFont = pygame.font.Font(None, 60)
        
        # clock - 60 FPS game
        clockTime = 60  # maximum FPS
        clock = pygame.time.Clock()
        
        # speed
        speed = 1.5
        MasterSprite.speed = speed
        
        
        
        #########################
        #    Start Time Mode    #
        #########################

        restart = True
        while restart == True:

        # Prepare game objects : reset
            # Reset Sprite groups
            alldrawings = pygame.sprite.Group()
            allsprites = pygame.sprite.RenderPlain((self.player,))
            MasterSprite.allsprites = allsprites


            score = 0
            wave = 1
            
            # object
            self.player =  EPlayer(400, 600, screen_size)
            self.player.life = 3
            enemy = Enemy(100, 300)
            player_group = pygame.sprite.Group()
            enemy_group = pygame.sprite.Group()
            self.bullet_group = pygame.sprite.Group()
            
            enemy = Enemy(100, 300)
            enemy2 = Enemy(200, 200)
            enemy3 = Enemy(300, 100)
            enemy4 = Enemy(400, 100)
            enemy5 = Enemy(500, 200)
            enemy6 = Enemy(600, 300)

            enemy_group.add(enemy)
            enemy_group.add(enemy2)
            enemy_group.add(enemy3)
            enemy_group.add(enemy4)
            enemy_group.add(enemy5)
            enemy_group.add(enemy6)
                
            player_group.add(self.player)

            # speed
            speed = 1.5 * ratio
            newspeed = 2.5 * ratio
            org_speed = 1.5 * ratio
            self.player.speed = speed
        
            # Reset all time
            bearPeriod = clockTime // speed
            curTime = 0
            powerTime = 8 * clockTime
            powerTimeLeft = powerTime
            beforeWaveTime = 4 * clockTime      # 3, 2, 1... before game start
            beforeWaveCount = beforeWaveTime
            leftTime = 60 * clockTime           # 60, 59, 58... game count down
            leftCount = leftTime
            
            
            self.player.alive = True
            self.player.life = 3
            self.player.initializeKeys()
            
            self.player.showChange_ship = False
        
        # Start Game
            while self.player.alive:
                clock.tick(clockTime)
            
            # Event Handling
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT
                        or event.type == pygame.KEYDOWN
                            and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                    # Resize windowSize
                    elif (event.type == pygame.VIDEORESIZE):
                        screen_size = min(event.w, event.h)
                        if screen_size <= 400:
                            screen_size = 400
                        if screen_size >= 900:
                            screen_size = 900
                        screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                        ratio = (screen_size / 600)
                        font = pygame.font.Font(None, round(36*ratio))
                    # Player Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction.keys()):
                        self.player.horiz += direction[event.key][0] * self.player.speed
                        self.player.vert += direction[event.key][1] * self.player.speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction.keys()):
                        self.player.horiz -= direction[event.key][0] * self.player.speed
                        self.player.vert -= direction[event.key][1] * self.player.speed
                    
                    # Pause Menu
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_p):
                        pauseMenu = True
                        cnt=0
                        
                        while pauseMenu:
                            clock.tick(clockTime)

                            pause_size = (round(pause.get_width() * ratio), round(pause.get_height() * ratio))
                            screen.blit(pygame.transform.scale(pause, pause_size), (0,0))
                            pause = pygame.transform.scale(pause, (600, 600))
                            pauseRect.midtop = screen.get_rect().midtop
                            for event in pygame.event.get():
                                if (event.type == pygame.QUIT
                                    or event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_ESCAPE):
                                    pygame.quit()
                                    sys.exit()
                                # Resize windowSize
                                elif (event.type == pygame.VIDEORESIZE):
                                    screen_size = min(event.w, event.h)
                                    if screen_size <= 400:
                                        screen_size = 400
                                    if screen_size >= 900:
                                        screen_size = 900
                                    screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                                    ratio = (screen_size / 600)
                                    font = pygame.font.Font(None, round(36*ratio))
                                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) :  # unpause
                                    
                                    if pauseMenu:
                                        pauseMenu = True
                                    elif selection == 1:
                                        pauseMenu = False
                                    elif selection == 2:
                                        return 2, screen_size
                                    elif (event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_UP
                                        and selection > 1
                                        and not showlogin):
                                        selection -= 1
                                    elif (event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_DOWN
                                        and selection < len(pauseMenuDict)
                                        and not showlogin):
                                        selection += 1
                                
                            blankText=font.render('            ',1,BLACK)
                            blankPos=blankText.get_rect(topright=screen.get_rect().center)
                            continueText = font.render('CONTINUE', 1, 'white')
                            continuePos = continueText.get_rect(topleft=blankPos.bottomleft)   
                            gotoMenuText = font.render('GO TO MAIN', 1, 'white')
                            gotoMenuPos = gotoMenuText.get_rect(topleft=continuePos.bottomleft)
                            selectText = font.render('*', 1, 'white')

                            selection = 1
                            pauseMenuDict = {1: continuePos, 2: gotoMenuPos}
                            selectPos = selectText.get_rect(topright=pauseMenuDict[selection].topleft)
        
                            textOverlays = zip([blankText,continueText, gotoMenuText, selectText],
                                                    [blankPos,continuePos, gotoMenuPos, selectPos])
                            for txt, pos in textOverlays:
                                screen.blit(txt, pos)

                            alldrawings.update()
                            pygame.display.flip()
                        
                        
            # Update text overlays
                waveText = font.render("Wave: " + str(wave), 1, 'WHITE')
                leftCountText = leftCountFont.render(str(leftCount // clockTime), 1, RED)
                scoreText = font.render("Score: " + str(score), 1, 'WHITE')

                wavePos = waveText.get_rect(topleft=screen.get_rect().topleft)
                leftCountPos = leftCountText.get_rect(midtop=screen.get_rect().midtop)
                scorePos = scoreText.get_rect(topright=screen.get_rect().topright)
                
                text = [waveText, leftCountText, scoreText]
                textposition = [wavePos, leftCountPos, scorePos]    
            
                textOverlays = zip(text, textposition)
                
            # Update and draw all sprites and text                                   
                allsprites.update(screen_size)
                allsprites.draw(screen)
                alldrawings.update()
                for txt, pos in textOverlays:
                    screen.blit(txt, pos)
                
                enemy_group.draw(screen)
                enemy_group.update(Extreme)
                
                player_group.draw(screen)
                self.player.update(Extreme)

                self.bullet_group.draw(screen)
                self.bullet_group.update(Extreme)
            
            # Update life
                life1Rect.topleft = wavePos.bottomleft
                life2Rect.topleft = wavePos.bottomleft
                life3Rect.topleft = wavePos.bottomleft

                life_size = (round(life1.get_width() * ratio), round(life1.get_height() * ratio))
                if self.player.life == 3:
                    screen.blit(pygame.transform.scale(life3, life_size), life3Rect)
                elif self.player.life == 2:
                    screen.blit(pygame.transform.scale(life2, life_size), life2Rect)
                elif self.player.life == 1:
                    screen.blit(pygame.transform.scale(life1, life_size), life1Rect)
                
                pygame.display.flip()
                
            name = ''
            nameBuffer = []
                
                        
    #########################
    #    After Game Loop    #
    #########################

        while True:
            # 바로 점수 저장되게
            clock.tick(clockTime)
        # name 입력받는 부분 지우기
        # Event Handling
            for event in pygame.event.get():
                if (event.type == pygame.QUIT and event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE): # 게임 창 끔
                        return False
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                        screen_size = min(event.w, event.h)
                        if screen_size <= 400:
                            screen_size = 400
                        if screen_size >= 900:
                            screen_size = 900
                        screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                        ratio = (screen_size / 600)
                        font = pygame.font.Font(None, round(36*ratio))
                elif (event.type == pygame.KEYDOWN # 키보드를 눌렀다 떼고
                    and event.key == pygame.K_RETURN # 엔터키
                    ): # 
                    Database().setScore(Var.user_id,score)
                    Database().setCoins(Var.user_id,score)
                    return True

            
        # moving field         
            field1Rect.y += int(2 * ratio)
            field2Rect.y += int(2 * ratio)

            if field1Rect.y >= screen_size:
                field1Rect.midbottom = field2Rect.midtop
            if field2Rect.y >= screen_size:
                field2Rect.midbottom = field1Rect.midtop
                
            field_size = (round(field1.get_width() * ratio), round(field1.get_height() * ratio))
            screen.blit(pygame.transform.scale(field1, field_size), (0,field1Rect.y))
            screen.blit(pygame.transform.scale(field2, field_size), (0,field2Rect.y))

            # Update and draw all sprites
            allsprites.update(screen_size)
            allsprites.draw(screen)
            alldrawings.update()
            for txt, pos in textOverlays:
                screen.blit(txt, pos)

            pygame.display.flip()          
