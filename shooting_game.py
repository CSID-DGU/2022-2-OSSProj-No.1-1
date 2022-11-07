import pygame  
import sys
from pygame.locals import *
from database import Database
from menu import *
from mode_single import *
from mode_pvp import *

if not pygame.mixer:
    print('Warning, sound disablead')
if not pygame.font:
    print('Warning, fonts disabled')

BACK = 0

direction = {None: (0, 0), pygame.K_UP: (0, -2), pygame.K_DOWN: (0, 2),
             pygame.K_LEFT: (-2, 0), pygame.K_RIGHT: (2, 0)}

# Initialize everything
pygame.mixer.pre_init(11025, -16, 2, 512)
pygame.init()
screen_size = 500 # screen_size = screen_width = screen_height
screen = pygame.display.set_mode((screen_size, screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("Space War!!")
pygame.mouse.set_visible(0)

# Music Setting
soundFX = Database.getSound()
music = Database.getSound(music=True)
if music and pygame.mixer:
    pygame.mixer.music.play(loops=-1)


showSelectModes=False
showHiScores = False

#--------------------------------------------------------------------#

#########################
#    Init Menu Loop     #
#########################

# inInitMenu loop = Init_page & login_page & signup_page
# Init_page = 1. log in 2. sign up 3. Quit 
# login_page = enter ID, enter PWD, BACK
# signup_page = enter ID, enter PWD, BACK
inInitMenu=True
while inInitMenu:
    userSelection, screen_size=Menu(screen_size).init_page()
    flag=True
    while flag:   
        if userSelection==1 or userSelection==2: # log in/sign up
            pageResult, screen_size=Menu(screen_size).login_sign_page(userSelection)
            if pageResult==BACK: # back
                flag=False  
            else: 
                flag=False
                inInitMenu=False          
        elif userSelection==3: # Quit
            pygame.quit()
            sys.exit()


# After login - infinite loop
windowShow = True
while windowShow:

#########################
#    Start Menu Loop    #
#########################

    inMainMenu=True
    while inMainMenu:
        userSelection, screen_size=Menu(screen_size).inMenu_page() 
        flag=True
        while flag:
            if userSelection == 1:
                pageResult, screen_size=Menu(screen_size).select_game_page()
                if pageResult == BACK: # back
                    flag = False
                elif (pageResult == 'SingleMode' or 
                    pageResult == 'TimeMode' or
                    pageResult == 'PvpMode'):
                    flag = False
                    inMainMenu = False 
            elif userSelection == 2:
                pageResult, screen_size = Menu(screen_size).score_page()
                if pageResult == BACK:
                    flag = False
            elif userSelection == 6:
                pygame.quit()
                sys.exit()


#########################
#    Start Game Loop    #
#########################

    if pageResult == 'SingleMode': 
        print('Play Single mode')
        Single.playGame(screen_size)
    elif pageResult == 'TimeMode':
        print('Play Time mode')
        Time.playGame(screen_size)
    elif pageResult == 'PvpMode':
        print('Play Pvp mode')
        Pvp.playGame(screen_size)
    
    print("Game End")