import pygame
import random
import sys
from pygame.locals import *

from sprites import (MasterSprite, Ship, Alien, Missile, BombPowerup,
                     ShieldPowerup, HalfPowerup, Coin, Explosion, Siney, Spikey, Fasty,
                     Roundy, Crawly)
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
        pygame.display.set_caption("Let's Kirin!")
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
        leaf_sound = load_sound('leaf.ogg')
        bomb_sound = load_sound('bomb.ogg')
        bear_explode_sound = load_sound('bear_explode.ogg')
        kirin_explode_sound = load_sound('kirin_explode.ogg')
        load_music('menu_music_loop.ogg')
        soundFX = Database().getSound()
        music = Database().getSound(music=True)
        if music and pygame.mixer: 
            pygame.mixer.music.play(loops=-1)

        # font
        font = pygame.font.Font(None, round(36*ratio))

        # clock - 60 FPS game
        clockTime = 60  # maximum FPS
        clock = pygame.time.Clock()

        # speed
        speed = 1.5
        MasterSprite.speed = speed
        
        # object
        kirin = Kirin2(screen_size)
        kirin2 = Kirin3(screen_size) 
        minikirin = Friendkirin(screen_size)

        initialbearTypes = (Green, Brown)
        powerupTypes = (BombPowerup, ShieldPowerup, DoubleleafPowerup, FriendPowerup, LifePowerup)

        bombs = pygame.sprite.Group()
        bombs2 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        # Score Function
        def kill_bear(bear, bearsLeftThisWave, score) :
            bearsLeftThisWave -= 1
            if bear.pType == 'green':
                score += 1
            elif bear.pType == 'brown':
                score += 2
            elif bear.pType == 'sunglasses':
                score += 4
            elif bear.pType == 'panda':
                score += 8
            return bearsLeftThisWave, score

    # pause menu text
        blankText=font.render('            ',1,BLACK)
        blankPos=blankText.get_rect(topright=screen.get_rect().center)
        restartText = font.render('RESTART GAME', 1, BLACK)
        restartPos = restartText.get_rect(topleft=blankPos.bottomleft)  
        fxText = font.render('SOUND FX ', 1, BLACK)
        fxPos = fxText.get_rect(topleft=restartPos.bottomleft)
        fxOnText = font.render('ON', 1, RED)
        fxOffText = font.render('OFF', 1, RED)
        fxOnPos = fxOnText.get_rect(topleft=fxPos.topright)
        fxOffPos = fxOffText.get_rect(topleft=fxPos.topright)
        musicText = font.render('MUSIC', 1, BLACK)
        musicPos = fxText.get_rect(topleft=fxPos.bottomleft)
        musicOnText = font.render('ON', 1, RED)
        musicOffText = font.render('OFF', 1, RED)
        musicOnPos = musicOnText.get_rect(topleft=musicPos.topright)
        musicOffPos = musicOffText.get_rect(topleft=musicPos.topright)
        helpText=font.render('HELP',1,BLACK)
        helpPos=helpText.get_rect(topleft=musicPos.bottomleft)
        quitText = font.render('QUIT', 1, BLACK)
        quitPos = quitText.get_rect(topleft=helpPos.bottomleft)
        selectText = font.render('*', 1, BLACK)
        selectPos = selectText.get_rect(topright=restartPos.topleft)
        selection = 1
        showHiScores = False 
        showHelp=False


    #########################
    #    Start Pvp Loop    #
    #########################
        restart = True
        while restart == True:

        # Prepare game objects : reset
            # Reset Sprite groups
            alldrawings = pygame.sprite.Group()
            allsprites = pygame.sprite.RenderPlain((kirin,kirin2))
            MasterSprite.allsprites = allsprites
            Bear.pool = pygame.sprite.Group(
                [bear(screen_size) for bear in initialbearTypes for _ in range(5)])
            Bear.active = pygame.sprite.Group()
            Leaf.pool = pygame.sprite.Group([Leaf(screen_size) for _ in range(10)]) 
            Leaf.active = pygame.sprite.Group()
            Explosion.pool = pygame.sprite.Group([Explosion(screen_size) for _ in range(10)])
            Explosion.active = pygame.sprite.Group()

            # Reset game contents
            bearsThisWave, bearsLeftThisWave, Bear.numOffScreen = 10, 10, 10
            friendkirin1 = False
            doubleleaf = False
            bombsHeld = 3
            score = 0
            friendkirin2 = False
            doubleleaf2 = False
            bombsHeld2 = 3
            score2 = 0
            leafFired = 0
            wave = 1

            # speed
            speed = 1.5 * ratio
            MasterSprite.speed = speed

            # Reset all time
            bearPeriod = clockTime // 2
            curTime = 0
            powerupTime = 8 * clockTime
            powerupTimeLeft = powerupTime
            betweenWaveTime = 3 * clockTime
            betweenWaveCount = betweenWaveTime
            
            betweenDoubleTime = 8 * clockTime
            betweenDoubleCount = betweenDoubleTime
            betweenDoubleCount2 = betweenDoubleTime
            friendkirinTime = 8 * clockTime
            friendkirinCount = friendkirinTime
            friendkirinLeafTime = 0.2 * clockTime
            friendkirinLeafCount = friendkirinLeafTime
            
            kirin.alive = True
            kirin.life = 3
            kirin.initializeKeys()
            kirin2.alive = True
            kirin2.life = 3
            kirin2.initializeKeys()

        # Start Game
            while kirin.alive and kirin2.alive :
                clock.tick(clockTime)

            # Drop Items
                powerupTimeLeft -= 1
                if powerupTimeLeft <= 0:
                    powerupTimeLeft = powerupTime
                    random.choice(powerupTypes)(screen_size).add(powerups, allsprites)

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
                    # kirin1 Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction.keys()):
                        kirin.horiz += direction[event.key][0] * speed
                        kirin.vert += direction[event.key][1] * speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction.keys()):
                        kirin.horiz -= direction[event.key][0] * speed
                        kirin.vert -= direction[event.key][1] * speed
                    # leaf1
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE):
                        if doubleleaf :
                            Leaf.position(kirin.rect.topleft)
                            Leaf.position(kirin.rect.topright)
                            leafFired += 2
                        else : 
                            Leaf.position(kirin.rect.midtop)
                            leafFired += 1
                        if soundFX:
                            leaf_sound.play()
                    # Bomb
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_b):
                        if bombsHeld > 0:
                            bombsHeld -= 1
                            newBomb = kirin.bomb()
                            newBomb.add(bombs, alldrawings)
                            if soundFX:
                                bomb_sound.play()
                    # kirin2 Moving
                    elif (event.type == pygame.KEYDOWN
                        and event.key in direction2.keys()):
                        kirin2.horiz += direction2[event.key][0] * speed
                        kirin2.vert += direction2[event.key][1] * speed
                    elif (event.type == pygame.KEYUP
                        and event.key in direction2.keys()):
                        kirin2.horiz -= direction2[event.key][0] * speed
                        kirin2.vert -= direction2[event.key][1] * speed
                    # leaf2
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_m):
                        if doubleleaf2 :
                            Leaf.position(kirin2.rect.topleft)
                            Leaf.position(kirin2.rect.topright)
                            leafFired += 2
                        else : 
                            Leaf.position(kirin2.rect.midtop)
                            leafFired += 1
                        if soundFX:
                            leaf_sound.play()
                    # Bomb
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_l):
                        if bombsHeld2 > 0:
                            bombsHeld2 -= 1
                            newBomb = kirin2.bomb()
                            newBomb.add(bombs2, alldrawings)
                            if soundFX:
                                bomb_sound.play()
                    # Pause
                    elif (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_p):
                        pauseMenu = True
                        cnt=0
                        
                        while pauseMenu:
                            clock.tick(clockTime)

                            pause_size = (round(pause.get_width() * ratio), round(pause.get_height() * ratio))
                            screen.blit(pygame.transform.scale(pause, pause_size), (0,0))

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
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_p): 
                                    pauseMenu = False
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_RETURN):
                                    if showHelp:
                                        cnt+=1
                                        if cnt%3!=0:
                                            showHelp=True
                                        else:
                                            showHelp=False
                                    elif selection == 1:    
                                        pauseMenu = False
                                        kirin.alive = False
                                    elif selection == 2:
                                        soundFX = not soundFX
                                        if soundFX:
                                            leaf_sound.play()
                                        Database.setSound(int(soundFX))
                                    elif selection == 3 and pygame.mixer:
                                        music = not music
                                        if music:
                                            pygame.mixer.music.play(loops=-1)
                                        else:
                                            pygame.mixer.music.stop()
                                        Database.setSound(int(music), music=True)
                                    elif selection == 4:
                                        cnt+=1
                                        showHelp=True
                                    elif selection == 5:
                                        pygame.quit()
                                        sys.exit()
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_UP
                                    and selection > 1
                                    and not showHiScores):
                                    selection -= 1
                                elif (event.type == pygame.KEYDOWN
                                    and event.key == pygame.K_DOWN
                                    and selection < len(pauseMenuDict)
                                    and not showHiScores):
                                    selection += 1

                            # pause menu text
                            blankText=font.render('            ',1,BLACK)
                            blankPos=blankText.get_rect(topright=screen.get_rect().center)
                            restartText = font.render('RESTART GAME', 1, BLACK)
                            restartPos = restartText.get_rect(topleft=blankPos.bottomleft)  
                            fxText = font.render('SOUND FX ', 1, BLACK)
                            fxPos = fxText.get_rect(topleft=restartPos.bottomleft)
                            fxOnText = font.render('ON', 1, RED)
                            fxOffText = font.render('OFF', 1, RED)
                            fxOnPos = fxOnText.get_rect(topleft=fxPos.topright)
                            fxOffPos = fxOffText.get_rect(topleft=fxPos.topright)
                            musicText = font.render('MUSIC', 1, BLACK)
                            musicPos = fxText.get_rect(topleft=fxPos.bottomleft)
                            musicOnText = font.render('ON', 1, RED)
                            musicOffText = font.render('OFF', 1, RED)
                            musicOnPos = musicOnText.get_rect(topleft=musicPos.topright)
                            musicOffPos = musicOffText.get_rect(topleft=musicPos.topright)
                            helpText=font.render('HELP',1,BLACK)
                            helpPos=helpText.get_rect(topleft=musicPos.bottomleft)
                            quitText = font.render('QUIT', 1, BLACK)
                            quitPos = quitText.get_rect(topleft=helpPos.bottomleft)

                            pauseMenuDict = {1: restartPos, 2: fxPos, 3: musicPos, 4: helpPos, 5: quitPos}
                            selectText = font.render('*', 1, BLACK)
                            selectPos = selectText.get_rect(topright=pauseMenuDict[selection].topleft)

                            if showHelp:
                                if cnt%3==1:
                                    menu, menuRect = load_image("help3.png") 
                                    menuRect.midtop = screen.get_rect().midtop
                                    menu_size = (round(menu.get_width() * ratio), round(menu.get_height() * ratio))
                                    screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
                                elif cnt%3==2:
                                    menu, menuRect = load_image("help2.png") 
                                    menuRect.midtop = screen.get_rect().midtop
                                    menu_size = (round(menu.get_width() * ratio), round(menu.get_height() * ratio))
                                    screen.blit(pygame.transform.scale(menu, menu_size), (0,0))                             
                            else:
                                textOverlays = zip([blankText,restartText, helpText, fxText,
                                                    musicText, quitText, selectText,
                                                    fxOnText if soundFX else fxOffText,
                                                    musicOnText if music else musicOffText],
                                                    [blankPos,restartPos, helpPos, fxPos,
                                                    musicPos, quitPos, selectPos,
                                                    fxOnPos if soundFX else fxOffPos,
                                                    musicOnPos if music else musicOffPos])

                            for txt, pos in textOverlays:
                                screen.blit(txt, pos)

                            alldrawings.update()
                            pygame.display.flip()
                    

            # Collision Detection
                # bears
                for bear in Bear.active:
                    for bomb in bombs:
                        if pygame.sprite.collide_circle(
                                bomb, bear) and bear in Bear.active:
                            if bear.pType != 'stone' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                bearsLeftThisWave, score = kill_bear(bear, bearsLeftThisWave, score)
                            leafFired += 1
                            if soundFX:
                                bear_explode_sound.play()
                    for bomb in bombs2:
                        if pygame.sprite.collide_circle(
                                bomb, bear) and bear in Bear.active:
                            if bear.pType != 'stone' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                bearsLeftThisWave, score2 = kill_bear(bear, bearsLeftThisWave, score2)
                            leafFired += 1
                            if soundFX:
                                bear_explode_sound.play()
                    for leaf in Leaf.active:
                        if pygame.sprite.collide_rect(
                                leaf, bear) and bear in bear.active:
                            leaf.table()
                            if bear.pType != 'stone' :
                                bear.table()
                                Explosion.position(bear.rect.center)
                                if bear.rect.center[0] < 500 :
                                    bearsLeftThisWave, score = kill_bear(bear, bearsLeftThisWave, score)
                                else :
                                    bearsLeftThisWave, score2 = kill_bear(bear, bearsLeftThisWave, score2)
                            if soundFX:
                                bear_explode_sound.play()

                    if pygame.sprite.collide_rect(bear, kirin):
                        if kirin.shieldUp:
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave, score = kill_bear(bear, bearsLeftThisWave, score)
                            leafFired += 1
                            kirin.shieldUp = False
                        elif kirin.life > 1:   # life
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave -= 1
                            score += 1
                            kirin.life -= 1
                        else:
                            restart = False
                            kirin.alive = False
                            kirin.remove(allsprites)
                            Explosion.position(kirin.rect.center)
                            if soundFX:
                                kirin_explode_sound.play()
                    if pygame.sprite.collide_rect(bear, kirin2):
                        if kirin2.shieldUp:
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave, score2 = kill_bear(bear, bearsLeftThisWave, score2)
                            leafFired += 1
                            kirin2.shieldUp = False
                        elif kirin2.life > 1:   # life
                            bear.table()
                            Explosion.position(bear.rect.center)
                            bearsLeftThisWave -= 1
                            score2 += 1
                            kirin2.life -= 1
                        else:
                            restart = False
                            kirin2.alive = False
                            kirin2.remove(allsprites)
                            Explosion.position(kirin2.rect.center)
                            if soundFX:
                                kirin_explode_sound.play()

                # PowerUps
                for powerup in powerups:
                    if pygame.sprite.collide_circle(powerup, kirin):
                        if powerup.pType == 'bomb':
                            bombsHeld += 1
                        elif powerup.pType == 'shield':
                            kirin.shieldUp = True
                        elif powerup.pType == 'doubleleaf':
                            doubleleaf = True
                        elif powerup.pType == 'life':
                            if kirin.life < 3:
                                kirin.life += 1 
                        elif powerup.pType == 'friendkirin' :
                            friendkirin1 = True
                            MasterSprite.allsprites.add(minikirin) 
                            allsprites.update(screen_size)
                            allsprites.draw(screen)        
                        powerup.kill()
                    elif powerup.rect.top > powerup.area.bottom:
                        powerup.kill()
                for powerup in powerups:
                    if pygame.sprite.collide_circle(powerup, kirin2):
                        if powerup.pType == 'bomb':
                            bombsHeld2 += 1
                        elif powerup.pType == 'shield':
                            kirin2.shieldUp = True
                        elif powerup.pType == 'doubleleaf' :
                            doubleleaf2 = True
                        elif powerup.pType == 'life':
                            if kirin2.life < 3:
                                kirin2.life += 1 
                        elif powerup.pType == 'friendkirin' :
                            friendkirin2 = True
                            MasterSprite.allsprites.add(minikirin) 
                            allsprites.update(screen_size)
                            allsprites.draw(screen)   
                        powerup.kill()
                    elif powerup.rect.top > powerup.area.bottom:
                        powerup.kill()

            # Update bears
                if curTime <= 0 and bearsLeftThisWave> 0:
                    Bear.position()
                    curTime = bearPeriod
                elif curTime > 0:
                    curTime -= 1

            # Update text overlays
                waveText = font.render("Wave: " + str(wave), 1, BLACK)
                leftText = font.render("bears: " + str(bearsLeftThisWave), 1, BLACK)
                bombText = font.render("Bombs: " + str(bombsHeld), 1, BLACK)
                bombText2 = font.render("Bombs: " + str(bombsHeld2), 1, BLACK)
                kirin1winText = font.render('PLAYER 1 WIN!', 1, BLACK)
                kirin2winText = font.render('PLAYER 2 WIN!', 1, BLACK)
                drawText = font.render('DRAW!', 1, BLACK)
        
                wavePos = waveText.get_rect(topright=screen.get_rect().midtop)
                leftPos = leftText.get_rect(topleft=screen.get_rect().midtop)
                bombPos = bombText.get_rect(bottomleft=screen.get_rect().bottomleft)
                bombPos2 = bombText2.get_rect(bottomright=screen.get_rect().bottomright)
                kirin1winPos = kirin1winText.get_rect(center=screen.get_rect().center)
                kirin2winPos = kirin2winText.get_rect(center=screen.get_rect().center)
                drawPos = drawText.get_rect(center=screen.get_rect().center)

                text = [waveText, leftText, bombText, bombText2]
                textposition = [wavePos, leftPos, bombPos, bombPos2]

            # Update using items
                # item - doubleleaf
                if doubleleaf:
                    if betweenDoubleCount > 0:
                        betweenDoubleCount -= 1
                    elif betweenDoubleCount == 0:
                        doubleleaf = False
                        betweenDoubleCount = betweenDoubleTime
                
                # item - doubleleaf2
                if doubleleaf2:
                    if betweenDoubleCount2 > 0:
                        betweenDoubleCount2 -= 1
                    elif betweenDoubleCount2 == 0:
                        doubleleaf2 = False
                        betweenDoubleCount = betweenDoubleTime
                
                # item - friendkirin
                if friendkirin1 :
                    minikirin.rect.bottomright = kirin.rect.bottomleft
                else :
                    minikirin.rect.bottomright = kirin2.rect.bottomleft
                
                if friendkirin1 or friendkirin2:
                    if friendkirinCount > 0:
                        friendkirinCount -= 1
                    elif friendkirinCount == 0:
                        if friendkirin1 :
                            friendkirin1 = False
                        else :
                            friendkirin2 = False
                        minikirin.remove()
                        friendkirinCount = friendkirinTime
                    if friendkirinLeafCount > 0:
                        friendkirinLeafCount -= 1
                    elif friendkirinLeafCount == 0:
                        friendkirinLeafCount = friendkirinLeafTime
                        Leaf.position(minikirin.rect.midtop)

            # Detertmine when to move to next wave
                if bearsLeftThisWave <= 0:
                    if betweenWaveCount > 0:
                        betweenWaveCount -= 1
                        nextWaveText = font.render(
                            'Wave ' + str(wave + 1) + ' in', 1, BLACK)
                        nextWaveNum = font.render(
                            str((betweenWaveCount // clockTime) + 1), 1, BLACK)
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
                            kirin.initializeKeys()
                            kirin2.initializeKeys()
                            bearsThisWave = 10
                            bearsLeftThisWave = Bear.numOffScreen = bearsThisWave
                        else:
                            bearsThisWave *= 2
                            bearsLeftThisWave = Bear.numOffScreen = bearsThisWave
                        if wave == 1:
                            Bear.pool.add([Stone(screen_size) for _ in range(5)])
                        if wave == 2:
                            Bear.pool.add([Sunglasses(screen_size) for _ in range(5)])
                        if wave == 3:
                            Bear.pool.add([Panda(screen_size) for _ in range(5)])
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

                life_size = (round(life1.get_width() * ratio), round(life1.get_height() * ratio))
                if kirin.life == 3:
                    screen.blit(pygame.transform.scale(life3, life_size), life3Rect)
                elif kirin.life == 2:
                    screen.blit(pygame.transform.scale(life2, life_size), life2Rect)
                elif kirin.life == 1:
                    screen.blit(pygame.transform.scale(life1, life_size), life1Rect)
                
                if kirin2.life == 3:
                    screen.blit(pygame.transform.scale(life_c, life_size), life_cRect)
                elif kirin2.life == 2:
                    screen.blit(pygame.transform.scale(life_b, life_size), life_bRect)
                elif kirin2.life == 1:
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

            if kirin.alive and not kirin2.alive :
                screen.blit(kirin1winText, kirin1winPos)
            elif kirin2.alive and not kirin.alive :
                screen.blit(kirin2winText, kirin2winPos)
            elif not kirin.alive and not kirin2.alive :
                screen.blit(drawText, drawPos)

            pygame.display.flip()