<<<<<<< HEAD
import pygame  
import sys
from pygame.locals import *
from database import Database
from menu import *
from mode_single import *
from mode_pvp import *
from mode_extreme import *
from load import Var # id, 점수 자동저장을 위한 var
from store import Store,CharStore
from load import * 


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
screen_size = 600 # screen_size = screen_width = screen_height
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
# inInitMenu : 맨 처음 페이지 
# userSelction 1부터 3까지 
inselectchar=False
inInitMenu=True
while inInitMenu:
    userSelection, screen_size=Menu(screen_size).init_page()
    flag=True
    while flag:   
        if userSelection==1: # log in/sign up
            pageResult, screen_size=Menu(screen_size).login_sign_page(userSelection)
            # DB 연결 수정되면 Menu(screen_size).login_sign_page(userSelection)으로 변경
            if pageResult==BACK: # back
                flag=False  
            else: 
                flag=False
                inInitMenu=False
        elif userSelection==2:
            pageResult, screen_size=Menu(screen_size).login_sign_page(userSelection)
            if pageResult==BACK: # back
                flag=False
            else:
                flag=False
                inInitMenu=False
                inselectchar=True
                while inselectchar:
                    pageResult=Menu(screen_size).set_character()
                    if pageResult==True:
                        inselectchar=False
                  

                
                          
        elif userSelection==3: # Quit
            pygame.quit()
            sys.exit()


    
# After login - infinite loop
windowShow = True
while windowShow:

#########################
#    Start Menu Loop    #
#########################
    # 로그인 후
    # userSelection 1부터 6까지
    inMainMenu=True
    instore=False
    incharsetting=False
    while inMainMenu:
        userSelection, screen_size=Menu(screen_size).inMenu_page() 
        flag=True
        while flag:
            if userSelection == 1:
                pageResult, screen_size=Menu(screen_size).select_game_page()
                if pageResult == BACK: # back
                    flag = False
                elif (pageResult == 'SingleMode' or  # select mode결과 
                    pageResult == 'ExtremeMode' or # time mode 삭제
                    pageResult == 'PvpMode'):
                    flag = False
                    inMainMenu = False # 게임 화면 접속
            elif userSelection == 2: # score 보는 페이지
                pageResult, screen_size = Menu(screen_size).score_page()
                if pageResult == BACK:
                    flag = False
            elif userSelection==5:
                pageResult=CharStore(screen_size).char_store()
                if pageResult==BACK:
                    flag=False
               
            elif userSelection==6:
                pageResult=CharStore(screen_size).char_setting()
                if pageResult==BACK:
                    flag=False
                
            
               # incharSetting=True
            elif userSelection == 8: # main menu에서 quit 버튼 
                pygame.quit() # pygame 자체를 종료
                sys.exit()
            elif userSelection == 9:
                pageResult, screen_size=Menu(screen_size).login_sign_page(userSelection)
                

#########################
#    store and character setting    #
#########################



#########################
#    Start Game Loop    #
#########################
    if pageResult == 'SingleMode': 
        print('Play Single mode')
        Single.playGame(screen_size)
    elif pageResult == 'ExtremeMode':
        print('Play Extreme mode')
        Extreme.playGame(screen_size)
    elif pageResult == 'PvpMode':
        print('Play Pvp mode')
        Pvp.playGame(screen_size)
    
=======
import pygame  
import sys
from pygame.locals import *
from database import Database
from menu import *
from mode_single import *
from mode_pvp import *
from load import Var # id, 점수 자동저장을 위한 var


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
screen_size = 600 # screen_size = screen_width = screen_height
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
# inInitMenu : 맨 처음 페이지 
# userSelction 1부터 3까지 
inselectchar=False
inInitMenu=True
while inInitMenu:
    userSelection, screen_size=Menu(screen_size).init_page()
    flag=True
    while flag:   
        if userSelection==1: # log in/sign up
            pageResult, screen_size=Menu(screen_size).login_sign_page(userSelection)
            # DB 연결 수정되면 Menu(screen_size).login_sign_page(userSelection)으로 변경
            if pageResult==BACK: # back
                flag=False  
            else: 
                flag=False
                inInitMenu=False
        elif userSelection==2:
            pageResult, screen_size=Menu(screen_size).login_sign_page(userSelection)
            if pageResult==BACK: # back
                flag=False
            else:
                flag=False
                inInitMenu=False
                inselectchar=True
                while inselectchar:
                    pageResult=Menu(screen_size).set_character()
                    if pageResult==True:
                        inselectchar=False
                  
                
        elif userSelection==3: # Quit
            pygame.quit()
            sys.exit()


    
# After login - infinite loop
windowShow = True
while windowShow:

#########################
#    Start Menu Loop    #
#########################
    # 로그인 후
    # userSelection 1부터 6까지
    inMainMenu=True
    while inMainMenu:
        userSelection, screen_size=Menu(screen_size).inMenu_page() 
        flag=True
        while flag:
            if userSelection == 1:
                pageResult, screen_size=Menu(screen_size).select_game_page()
                if pageResult == BACK: # back
                    flag = False
                elif (pageResult == 'SingleMode' or  # select mode결과 
                    pageResult == 'TimeMode' or # time mode 삭제
                    pageResult == 'PvpMode'):
                    flag = False
                    inMainMenu = False # 게임 화면 접속
            elif userSelection == 2: # score 보는 페이지
                pageResult, screen_size = Menu(screen_size).score_page()
                if pageResult == BACK:
                    flag = False
            elif userSelection == 6: # main menu에서 quit 버튼 
                pygame.quit() # pygame 자체를 종료
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
    
>>>>>>> feature/DB
    print("Game End")