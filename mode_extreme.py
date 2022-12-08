import pygame
import os
import sys
from pygame.locals import *
from sprites import (MasterSprite, EPlayer, 
                     Enemy, Enemy1, Enemy2, Enemy3, Enemy4, Enemy5, Enemy6)
from database import Database
from load import load_image, load_sound, load_music,Var
from menu import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0
EXTREME = 1

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

class Extreme():
    def playGame(screen_size):
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
        
        # object
        player =  Player(screen_size)
        player.life = 3
        bullet_group = pygame.sprite.Group()
        
        enemy1 = Enemy1(screen_size)
        enemy2 = Enemy2(screen_size)
        enemy3 = Enemy3(screen_size)
        enemy4 = Enemy4(screen_size)
        enemy5 = Enemy5(screen_size)
        enemy6 = Enemy6(screen_size)
        
        initialEnemyTypes = (Enemy1, Enemy2, Enemy3, Enemy4, Enemy5, Enemy6)
        
        # Score Function
        
        # High Score
        hiScores=Database().getScores()
        highScoreTexts = [font.render("NAME", 1, RED),
                        font.render("SCORE", 1, RED)]
        highScorePos = [highScoreTexts[0].get_rect(
                        topleft=screen.get_rect().inflate(-100, -100).topleft),
                        highScoreTexts[1].get_rect(
                        midtop=screen.get_rect().inflate(-100, -100).midtop)]
        for hs in hiScores:
            highScoreTexts.extend([font.render(str(hs[x]), 1, 'WHITE')
                                for x in range(2)])
            highScorePos.extend([highScoreTexts[x].get_rect(
                topleft=highScorePos[x].bottomleft) for x in range(-2, 0)])
            
        # pause menu text  
        blankText=font.render('            ',1,'white')
        blankPos=blankText.get_rect(topright=screen.get_rect().center)
        continueText = font.render('CONTINUE', 1, 'white')
        continuePos = continueText.get_rect(topleft=blankPos.bottomleft)   
        gotoMenuText = font.render('GO TO MAIN', 1, 'white')
        gotoMenuPos = gotoMenuText.get_rect(topleft=continuePos.bottomleft)
        selectText = font.render('*', 1, 'white')
        selectPos = selectText.get_rect(topright=continuePos.topleft)
        selection = 1
        
        #########################
        #    Start Time Mode    #
        #########################

        restart = True
        while restart == True:

        # Prepare game objects : reset
            # Reset Sprite groups
            alldrawings = pygame.sprite.Group()
            allsprites = pygame.sprite.RenderPlain((player, ))
            MasterSprite.allsprites = allsprites
            MasterSprite.allsprites.add(enemy1)
            Enemy.pool = pygame.sprite.Group(
                [enemy(screen_size) for enemy in initialEnemyTypes])
            Enemy.active = pygame.sprite.Group()
            # Reset game contents
            score = 0
            wave = 1

            # speed
            speed = 1.5 * ratio
            newspeed = 2.5 * ratio
            org_speed = 1.5 * ratio
            player.speed = speed
        
            # Reset all time
            Period = clockTime // speed
            curTime = 0
            powerTime = 8 * clockTime
            powerTimeLeft = powerTime
            beforeWaveTime = 4 * clockTime      # 3, 2, 1... before game start
            beforeWaveCount = beforeWaveTime
            leftTime = 60 * clockTime           # 60, 59, 58... game count down
            leftCount = leftTime
            
            
            player.alive = True
            player.life = 3
            player.initializeKeys()
            
            player.showChange_ship = False
        
        # Start Game
            while player.alive:
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
                        leftCountFont = pygame.font.Font(None, round(60*ratio))
                    # Player Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction.keys()):
                        player.horiz += direction[event.key][0] * player.speed
                        player.vert += direction[event.key][1] * player.speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction.keys()):
                        player.horiz -= direction[event.key][0] * player.speed
                        player.vert -= direction[event.key][1] * player.speed
                    
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
                
            # Collision Detection
                # monster
                # for enemy in Enemy.active:
                #     for bomb in bombs:
                #         if pygame.sprite.collide_circle(
                #                 bomb, monster) and monster in Monster.active:
                #             if monster.pType != 'grey' :
                #                 if monster.pType == 'boss':
                #                     if boss.health >= 1 :
                #                         boss.health -= 1
                #                     else :
                #                         monster.table() 
                #                         Explosion.position(monster.rect.center)
                #                         monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                #                 else:
                #                     monster.table()
                #                     Explosion.position(monster.rect.center)
                #                     monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                #             beamFired += 1
                #             if soundFX:
                #                 bear_explode_sound.play()
                #     for beam in Beam.active:
                #         if pygame.sprite.collide_rect(
                #                 beam, monster) and monster in Monster.active:
                #             beam.table()
                #             if monster.pType != 'grey' :
                #                 beam.table()
                #                 if monster.pType == 'boss':
                #                     if boss.health >= 1 :
                #                         boss.health -= 1                        
                #                     else :         
                #                         monster.table()                  
                #                         Explosion.position(monster.rect.center)
                #                         monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                #                 else:
                #                     monster.table()
                #                     Explosion.position(monster.rect.center)
                #                     monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                #             if soundFX:
                #                 bear_explode_sound.play()
                #             if soundFX:
                #                 bear_explode_sound.play()
                #     if pygame.sprite.collide_rect(monster, player) :
                #         if player.shieldUp:
                #             monster.table()
                #             Explosion.position(monster.rect.center)
                #             monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                #             beamFired += 1
                #             player.shieldUp = False
                #         elif player.life > 1:   # life
                #             monster.table()
                #             Explosion.position(monster.rect.center)
                #             monstersLeftThisWave -= 1
                #             score += 1
                #             player.life -= 1
                #         else:
                #             restart = False
                #             player.alive = False
                #             player.remove(allsprites)
                #             Explosion.position(player.rect.center)
                #             if soundFX:
                #                 kirin_explode_sound.play() ## 변경사항
                

            # Update Monsters
                if curTime <= 0 :
                    curTime = Period
                elif curTime > 0:
                    curTime -= 1        
                        
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
                
            # leftCount - Count Down 60 to 0
                if leftCount > 0:
                    leftCount -= 1
                elif leftCount == 0:
                    restart = False
                    player.alive = False
                    player.remove(allsprites)
                    Explosion.position(player.rect.center)
                    if soundFX:
                        Database().getSound()   
            # Update and draw all sprites and text                                   
                allsprites.update(screen_size)
                allsprites.draw(screen)
                alldrawings.update()
                for txt, pos in textOverlays:
                    screen.blit(txt, pos)
            
            # Update life
                life1Rect.topleft = wavePos.bottomleft
                life2Rect.topleft = wavePos.bottomleft
                life3Rect.topleft = wavePos.bottomleft

                life_size = (round(life1.get_width() * ratio), round(life1.get_height() * ratio))
                if player.life == 3:
                    screen.blit(pygame.transform.scale(life3, life_size), life3Rect)
                elif player.life == 2:
                    screen.blit(pygame.transform.scale(life2, life_size), life2Rect)
                elif player.life == 1:
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
