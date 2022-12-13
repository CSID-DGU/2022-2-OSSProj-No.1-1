import pygame
import random
import sys
from pygame.locals import *

from sprites import (MasterSprite, 
                     Player, FriendShip, Player2, Player3, Monster, Beam, Explosion,
                     BombPower, ShieldPower, DoublebeamPower, FriendPower, LifePower, TriplecupcakePower,
                     BroccoliBeamfast,
                     Green, Yellow, Grey, Pink, Blue)
from database import Database
from load import load_image, load_sound, load_music
from menu import *

if not pygame.mixer: 
    print('Warning, sound disabled')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

direction = {None: (0, 0), pygame.K_w: (0, -2), pygame.K_s: (0, 2),
             pygame.K_a: (-2, 0), pygame.K_d: (2, 0)}

direction2 = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

class Pvp() :
    def playGame(screen_size): 
    # Initialize everything
        pygame.mixer.pre_init(11025, -16, 2, 512)
        pygame.init()
        ratio = (screen_size / 500)
        screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.set_caption("Let's Play!")
        pygame.mouse.set_visible(0)    

    # Prepare background image
        # Game field
        field1, field1Rect = load_image("field.png")
        field2, field2Rect = load_image("field.png")
        field1Rect.midtop = screen.get_rect().midtop
        field2Rect.midbottom = field1Rect.midtop

        # Menu - pause menu Highscore & help
        menu, menuRect = load_image("menu.png")
        menuRect.midtop = screen.get_rect().midtop

        # pause
        pause,pauseRect = load_image('pause.png')
        pauseRect.midtop = screen.get_rect().midtop
        pause = pygame.transform.scale(pause, (600, 600))
        pauseRect.midtop = screen.get_rect().midtop
        pauseMenu = False 

    # Prepare game objects
        # life
        life1, life1Rect = load_image('heart1.png')
        life2, life2Rect = load_image('heart2.png')
        life3, life3Rect = load_image('heart3.png')

        life_a, life_aRect = load_image('heart1.png')
        life_b, life_bRect = load_image('heart2.png')
        life_c, life_cRect = load_image('heart3.png')

        # Sounds
        missile_sound = load_sound('missile.ogg')
        bomb_sound = load_sound('bomb.ogg')
        alien_explode_sound = load_sound('alien_explode.ogg')
        ship_explode_sound = load_sound('ship_explode.ogg')
        load_music('music_loop.ogg')
        soundFX = Database().getSound()
        music = Database().getSound()
        if music and pygame.mixer: 
           pygame.mixer.music.play(loops=-1)

        # font
        font = pygame.font.Font("LeeSeoyun.ttf", round(15*ratio))
        font2 = pygame.font.Font("LeeSeoyun.ttf", round(21*ratio))

        # clock - 60 FPS game
        clockTime = 60  # maximum FPS
        clock = pygame.time.Clock()

        # speed
        speed = 1.5
        MasterSprite.speed = speed
        
        # object
        player = Player2(screen_size)
        player2 = Player3(screen_size) 
        miniPlayer = FriendShip(screen_size)

        initialmonsterTypes = (Green, Yellow)
        powerTypes = (BombPower, ShieldPower, DoublebeamPower, TriplecupcakePower, FriendPower, LifePower)

        bombs = pygame.sprite.Group()
        bombs2 = pygame.sprite.Group()
        powers = pygame.sprite.Group()

        # Score Function
        def kill_monster(monster, monstersLeftThisWave, score) :
            monstersLeftThisWave -= 1
            if monster.pType == 'green':
                score += 1
            elif monster.pType == 'yellow':
                score += 2
            elif monster.pType == 'pink':
                score += 4
            elif monster.pType == 'blue':
                score += 8
            return monstersLeftThisWave, score

    # pause menu text
        blankText=font.render('            ',1,'white')
        blankPos=blankText.get_rect(topright=screen.get_rect().center)
        continueText = font2.render('CONTINUE', 1, 'white')
        continuePos = continueText.get_rect(topleft=blankPos.bottomleft)   
        gotoMenuText = font2.render('GO TO MAIN', 1, 'white')
        gotoMenuPos = gotoMenuText.get_rect(topleft=continuePos.bottomleft)
        selectText = font2.render('*', 1, 'white')
        pauseMenuDict = {1: continuePos, 2: gotoMenuPos}
        selection = 1
        selectPos = selectText.get_rect(topright=pauseMenuDict[selection].topleft)
        

    #########################
    #    Start Pvp Loop    #
    #########################
        restart = True
        while restart == True:
            
        # Prepare game objects : reset
            # Reset Sprite groups
            alldrawings = pygame.sprite.Group()
            allsprites = pygame.sprite.RenderPlain((player,player2))
            MasterSprite.allsprites = allsprites
            Monster.pool = pygame.sprite.Group(
                [monster(screen_size) for monster in initialmonsterTypes for _ in range(5)])
            Monster.active = pygame.sprite.Group()
            Beam.pool = pygame.sprite.Group([Beam(screen_size) for _ in range(10)]) 
            Beam.active = pygame.sprite.Group()
            Explosion.pool = pygame.sprite.Group([Explosion(screen_size) for _ in range(10)])
            Explosion.active = pygame.sprite.Group()

            # Reset game contents
            monstersThisWave, monstersLeftThisWave, Monster.numOffScreen = 10, 10, 10
            friendShip1 = False
            doublebeam = False
            triplecupcake = False
            bombsHeld = 3
            score = 0
            friendShip2 = False
            doublebeam2 = False
            triplecupcake2 = False
            bombsHeld2 = 3
            score2 = 0
            beamFired = 0
            wave = 1

            # speed
            speed = 1.5 * ratio
            MasterSprite.speed = speed

            # Reset all time
            monsterPeriod = clockTime // 2
            curTime = 0
            powerTime = 8 * clockTime
            powerTimeLeft = powerTime
            betweenWaveTime = 3 * clockTime
            betweenWaveCount = betweenWaveTime
            
            betweenDoubleTime = 8 * clockTime
            betweenDoubleCount = betweenDoubleTime
            betweenDoubleCount2 = betweenDoubleTime
            betweenTripleTime = 8 * clockTime
            betweenTripleCount = betweenTripleTime
            betweenTripleCount2 = betweenTripleTime
            friendShipTime = 8 * clockTime
            friendShipCount = friendShipTime
            friendShipbeamTime = 0.2 * clockTime
            friendShipbeamCount = friendShipbeamTime
            
            player.alive = True
            player.life = 3
            player.initializeKeys()
            player2.alive = True
            player2.life = 3
            player2.initializeKeys()

        # Start Game
            while player.alive and player2.alive :
                clock.tick(clockTime)
                load_music('music_loop.ogg')

            # Drop Items
                powerTimeLeft -= 1
                if powerTimeLeft <= 0:
                    powerTimeLeft = powerTime
                    random.choice(powerTypes)(screen_size).add(powers, allsprites)

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
                        if screen_size <= 300:
                            screen_size = 300
                        screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                        ratio = (screen_size / 500)
                        font = pygame.font.Font(None, round(36*ratio))
                    # Player1 Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction.keys()):
                        player.horiz += direction[event.key][0] * speed
                        player.vert += direction[event.key][1] * speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction.keys()):
                        player.horiz -= direction[event.key][0] * speed
                        player.vert -= direction[event.key][1] * speed
                    # beam1
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE):
                        if doublebeam :
                            Beam.position(player.rect.topleft)
                            Beam.position(player.rect.topright)
                            beamFired += 2
                        elif triplecupcake:
                            Beam.position(player.rect.topleft)
                            Beam.position(player.rect.midtop)
                            Beam.position(player.rect.topright)
                            beamFired += 3
                            
                        else : 
                            Beam.position(player.rect.midtop)
                            beamFired += 1
                        if soundFX:
                            missile_sound.play()
                    # Bomb
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_b):
                        if bombsHeld > 0:
                            bombsHeld -= 1
                            newBomb = player.bomb()
                            newBomb.add(bombs, alldrawings)
                            if soundFX:
                                bomb_sound.play()
                    # Player2 Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction2.keys()):
                        player2.horiz += direction2[event.key][0] * speed
                        player2.vert += direction2[event.key][1] * speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction2.keys()):
                        player2.horiz -= direction2[event.key][0] * speed
                        player2.vert -= direction2[event.key][1] * speed
                    # beam2
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_m):
                        if doublebeam2 :
                            beam.position(player2.rect.topleft)
                            beam.position(player2.rect.topright)
                            beamFired += 2
                        elif triplecupcake2 :
                            beam.position(player2.rect.topleft)
                            beam.position(player2.rect.midtop)
                            beam.position(player2.rect.topright)
                            beamFired += 3
                        else : 
                            beam.position(player2.rect.midtop)
                            beamFired += 1
                        if soundFX:
                            missile_sound.play()
                    # Bomb
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_l):
                        if bombsHeld2 > 0:
                            bombsHeld2 -= 1
                            newBomb = player2.bomb()
                            newBomb.add(bombs2, alldrawings)
                            if soundFX:
                                bomb_sound.play()
                    # Pause
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_p):
                        pauseMenu = True
                        cnt=0
                        pauseMenuDict={1:continuePos,2:gotoMenuPos}
                        selection=1
                        while pauseMenu:
                            #clock.tick(clockTime)
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
                                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) :  #pause menu (continue, go)
                                    if selection == 1:
                                        pauseMenu = False
                                    elif selection == 2:
                                        inMenu =True
                                        return inMenu, screen_size
                                elif (event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_DOWN
                                        and selection < len(pauseMenuDict)):
                                        selection += 1
                                elif (event.type == pygame.KEYDOWN
                                        and event.key == pygame.K_UP
                                        and selection > 1):
                                        selection -= 1
                                
                                
                            blankText=font.render('            ',1,BLACK)
                            blankPos=blankText.get_rect(topright=screen.get_rect().center)
                            continueText = font2.render('CONTINUE', 1, 'white')
                            continuePos = continueText.get_rect(topleft=blankPos.bottomleft)   
                            gotoMenuText = font2.render('GO TO MAIN', 1, 'white')
                            gotoMenuPos = gotoMenuText.get_rect(topleft=continuePos.bottomleft)
                            selectText = font2.render('*', 1, 'white')
                            pauseMenuDict={1:continuePos,2:gotoMenuPos}
                            
                            selectPos = selectText.get_rect(topright=pauseMenuDict[selection].topleft)
                            textOverlays = zip([blankText,continueText, gotoMenuText, selectText],
                                                    [blankPos,continuePos, gotoMenuPos, selectPos])
                            for txt, pos in textOverlays:
                                screen.blit(txt, pos)

                            alldrawings.update()
                            pygame.display.flip()
                    

            # Collision Detection
                # monsters
                for monster in Monster.active:
                    for bomb in bombs:
                        if pygame.sprite.collide_circle(
                                bomb, monster) and monster in Monster.active:
                            if monster.pType != 'grey' :
                                monster.table()
                                Explosion.position(monster.rect.center)
                                monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                            beamFired += 1
                            if soundFX:
                                alien_explode_sound .play()

                    for bomb in bombs2:
                        if pygame.sprite.collide_circle(
                                bomb, monster) and monster in Monster.active:
                            if monster.pType != 'grey' :
                                monster.table()
                                Explosion.position(monster.rect.center)
                                monstersLeftThisWave, score2 = kill_monster(monster, monstersLeftThisWave, score2)
                            beamFired += 1
                            if soundFX:
                                alie_explode.play()
                    for beam in Beam.active:
                        if pygame.sprite.collide_rect(
                                beam, monster) and monster in Monster.active:
                            beam.table()
                            if monster.pType != 'grey' :
                                monster.table()
                                Explosion.position(monster.rect.center)
                                if monster.rect.center[0] < 500 :
                                    monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                                else :
                                    monstersLeftThisWave, score2 = kill_monster(monster, monstersLeftThisWave, score2)
                            if soundFX:
                                alien_explode_sound .play()

                    if pygame.sprite.collide_rect(monster, player):
                        if player.shieldUp:
                            monster.table()
                            Explosion.position(monster.rect.center)
                            monstersLeftThisWave, score = kill_monster(monster, monstersLeftThisWave, score)
                            beamFired += 1
                            player.shieldUp = False
                        elif player.life > 1:   # life
                            monster.table()
                            Explosion.position(monster.rect.center)
                            monstersLeftThisWave -= 1
                            score += 1
                            player.life -= 1
                        else:
                            restart = False
                            player.alive = False
                            player.remove(allsprites)
                            Explosion.position(player.rect.center)
                            if soundFX:
                                alien_explode_sound .play()
                    if pygame.sprite.collide_rect(monster, player2):
                        if player2.shieldUp:
                            monster.table()
                            Explosion.position(monster.rect.center)
                            monstersLeftThisWave, score2 = kill_monster(monster, monstersLeftThisWave, score2)
                            beamFired += 1
                            player2.shieldUp = False
                        elif player2.life > 1:   # life
                            monster.table()
                            Explosion.position(monster.rect.center)
                            monstersLeftThisWave -= 1
                            score2 += 1
                            player2.life -= 1
                        else:
                            restart = False
                            player2.alive = False
                            player2.remove(allsprites)
                            Explosion.position(player2.rect.center)
                            if soundFX:
                                alien_explode_sound .play()

                # PowerUps
                for power in powers:
                    if pygame.sprite.collide_circle(power, player):
                        if power.pType == 'bomb':
                            bombsHeld += 1
                        elif power.pType == 'shield':
                            player.shieldUp = True
                        elif power.pType == 'doublebeam':
                            doublebeam = True
                        elif power.pType == 'triplecupcake' :
                            triplecupcake = True
                        elif power.pType == 'life':
                            if player.life < 3:
                                player.life += 1 
                        elif power.pType == 'friendShip' :
                            friendShip1 = True
                            MasterSprite.allsprites.add(miniPlayer) 
                            allsprites.update(screen_size)
                            allsprites.draw(screen)        
                        power.kill()
                    elif power.rect.top > power.area.bottom:
                        power.kill()
                for power in powers:
                    if pygame.sprite.collide_circle(power, player2):
                        if power.pType == 'bomb':
                            bombsHeld2 += 1
                        elif power.pType == 'shield':
                            player2.shieldUp = True
                        elif power.pType == 'doublebeam' :
                            doublebeam2 = True
                        elif power.pType == 'triplecupcake' :
                            triplecupcake2 = True
                        elif power.pType == 'life':
                            if player2.life < 3:
                                player2.life += 1 
                        elif power.pType == 'friendShip' :
                            friendShip2 = True
                            MasterSprite.allsprites.add(miniPlayer) 
                            allsprites.update(screen_size)
                            allsprites.draw(screen)   
                        power.kill()
                    elif power.rect.top > power.area.bottom:
                        power.kill()

            # Update monsters
                if curTime <= 0 and monstersLeftThisWave> 0:
                    Monster.position()
                    curTime = monsterPeriod
                elif curTime > 0:
                    curTime -= 1

            # Update text overlays
                waveText = font.render("Wave: " + str(wave), 1, 'YELLOW')
                leftText = font.render("monsters: " + str(monstersLeftThisWave), 1, 'white')
                bombText = font.render("Bombs: " + str(bombsHeld), 1, 'white')
                bombText2 = font.render("Bombs: " + str(bombsHeld2), 1, 'white')
                Player1winText = font2.render('PLAYER 1 WIN!', 1, 'RED')
                Player2winText = font2.render('PLAYER 2 WIN!', 1, 'RED')
                drawText = font2.render('DRAW!', 1, 'RED')
        
                wavePos = waveText.get_rect(topright=screen.get_rect().midtop)
                leftPos = leftText.get_rect(topleft=screen.get_rect().midtop)
                bombPos = bombText.get_rect(bottomleft=screen.get_rect().bottomleft)
                bombPos2 = bombText2.get_rect(bottomright=screen.get_rect().bottomright)
                Player1winPos = Player1winText.get_rect(center=screen.get_rect().center)
                Player2winPos = Player2winText.get_rect(center=screen.get_rect().center)
                drawPos = drawText.get_rect(center=screen.get_rect().center)

                text = [waveText, leftText, bombText, bombText2]
                textposition = [wavePos, leftPos, bombPos, bombPos2]

            # Update using items
                # item - doublebeam
                if doublebeam:
                    if betweenDoubleCount > 0:
                        betweenDoubleCount -= 1
                    elif betweenDoubleCount == 0:
                        doublebeam = False
                        betweenDoubleCount = betweenDoubleTime
                
                # item - doublebeam2
                if doublebeam2:
                    if betweenDoubleCount2 > 0:
                        betweenDoubleCount2 -= 1
                    elif betweenDoubleCount2 == 0:
                        doublebeam2 = False
                        betweenDoubleCount = betweenDoubleTime
                
                # item - triplecupcake
                if triplecupcake:
                    if betweenTripleCount > 0:
                        betweenTripleCount -= 1
                    elif betweenTripleCount == 0:
                        triplecupcake = False
                        betweenTripleCount = betweenTripleTime
                
                # item - triplecupcake2
                if triplecupcake2:
                    if betweenTripleCount2 > 0:
                        betweenTripleCount2 -= 1
                    elif betweenTripleCount2 == 0:
                        triplecupcake2 = False
                        betweenTripleCount = betweenTripleTime
                
                # item - friendShip
                if friendShip1 :
                    miniPlayer.rect.bottomright = player.rect.bottomleft
                else :
                    miniPlayer.rect.bottomright = player2.rect.bottomleft
                
                if friendShip1 or friendShip2:
                    if friendShipCount > 0:
                        friendShipCount -= 1
                    elif friendShipCount == 0:
                        if friendShip1 :
                            friendShip1 = False
                        else :
                            friendShip2 = False
                        miniPlayer.remove()
                        friendShipCount = friendShipTime
                    if friendShipbeamCount > 0:
                        friendShipbeamCount -= 1
                    elif friendShipbeamCount == 0:
                        friendShipbeamCount = friendShipbeamTime
                        beam.position(miniPlayer.rect.midtop)

            # Detertmine when to move to next wave
                if monstersLeftThisWave <= 0:
                    if betweenWaveCount > 0:
                        betweenWaveCount -= 1
                        nextWaveText = font.render(
                            'Wave ' + str(wave + 1) + ' in', 1, 'white')
                        nextWaveNum = font.render(
                            str((betweenWaveCount // clockTime) + 1), 1, 'white')
                        text.extend([nextWaveText, nextWaveNum])
                        nextWavePos = nextWaveText.get_rect(
                            center=screen.get_rect().center)
                        nextWaveNumPos = nextWaveNum.get_rect(
                            midtop=nextWavePos.midbottom)
                        textposition.extend([nextWavePos, nextWaveNumPos])
                        if wave % 4 == 0:
                            speedUpText = font.render('SPEED UP!', 1, RED)
                            speedUpPos = speedUpText.get_rect(
                                midtop=nextWaveNumPos.midbottom)
                            text.append(speedUpText)
                            textposition.append(speedUpPos)
                    elif betweenWaveCount == 0:
                        if wave % 4 == 0:
                            speed += 0.5
                            MasterSprite.speed = speed
                            player.initializeKeys()
                            player2.initializeKeys()
                            monstersThisWave = 10
                            monstersLeftThisWave = Monster.numOffScreen = monstersThisWave
                        else:
                            monstersThisWave *= 2
                            monstersLeftThisWave = Monster.numOffScreen = monstersThisWave
                        if wave == 1:
                            Monster.pool.add([Grey(screen_size) for _ in range(5)])
                        if wave == 2:
                            Monster.pool.add([Pink(screen_size) for _ in range(5)])
                        if wave == 3:
                            Monster.pool.add([Blue(screen_size) for _ in range(5)])
                        wave += 1
                        betweenWaveCount = betweenWaveTime

                textOverlays = zip(text, textposition)

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
                pygame.draw.rect(screen, BLACK, [250*ratio,0,3,500*ratio])

            # Update and draw all sprites and text         
                allsprites.update(screen_size)
                allsprites.draw(screen)
                alldrawings.update()

                for txt, pos in textOverlays:
                    screen.blit(txt, pos)

            # Update life
                life1Rect.topright = wavePos.topleft
                life2Rect.topright = wavePos.topleft
                life3Rect.topright = wavePos.topleft

                life_aRect.topleft = leftPos.topright
                life_bRect.topleft = leftPos.topright
                life_cRect.topleft = leftPos.topright

                life_size = (round(life1.get_width() * ratio * 0.8), round(life1.get_height() * ratio * 0.8))
                if player.life == 3:
                    screen.blit(pygame.transform.scale(life3, life_size), life3Rect)
                elif player.life == 2:
                    screen.blit(pygame.transform.scale(life2, life_size), life2Rect)
                elif player.life == 1:
                    screen.blit(pygame.transform.scale(life1, life_size), life1Rect)
                
                if player2.life == 3:
                    screen.blit(pygame.transform.scale(life_c, life_size), life_cRect)
                elif player2.life == 2:
                    screen.blit(pygame.transform.scale(life_b, life_size), life_bRect)
                elif player2.life == 1:
                    screen.blit(pygame.transform.scale(life_a, life_size), life_aRect)

                pygame.display.flip()

    #########################
    #    After Game Loop    #
    #########################

        while True:
            clock.tick(clockTime)

        # Event Handling
            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    and event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    return False
                elif (event.type == pygame.VIDEORESIZE):
                    screen_size = min(event.w, event.h)
                    if screen_size <= 300:
                        screen_size = 300
                    screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    ratio = (screen_size / 500)
                    font = pygame.font.Font(None, round(36*ratio)) 
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
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
            pygame.draw.rect(screen, BLACK, [250*ratio,0,3,500*ratio])

        # Update and draw all sprites
            allsprites.update(screen_size)
            allsprites.draw(screen)
            alldrawings.update()

            if player.alive and not player2.alive :
                screen.blit(Player1winText, Player1winPos)
            elif player2.alive and not player.alive :
                screen.blit(Player2winText, Player2winPos)
            elif not player.alive and not player2.alive :
                screen.blit(drawText, drawPos)

            pygame.display.flip()