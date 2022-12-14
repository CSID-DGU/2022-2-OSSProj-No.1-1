import pygame


import sys
from pygame.locals import *
from load import load_image, load_sound, load_music,Var # id, 점수 자동저장을 위한 var
from database import Database

from sprites import *
from load import * 
from store import Store,CharStore

BLACK = (0, 0, 0)
Black=(0,0,0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

BACK=0
#mixer not initialized
pygame.init()
missile_sound = load_sound('missile.ogg')
bomb_sound = load_sound('bomb.ogg')
alien_explode_sound = load_sound('alien_explode.ogg')
ship_explode_sound = load_sound('ship_explode.ogg')

load_music('music_loop.ogg')

class Language_check() :  
    def __init__(self):
        self.state = False ######### False면 영어, True면 한국어
    def change_language(self) :
        self.state = not self.state
    def get_language(self) :
        return self.state


class Keyboard(object):
    keys = {pygame.K_a: 'A', pygame.K_b: 'B', pygame.K_c: 'C', pygame.K_d: 'D',
            pygame.K_e: 'E', pygame.K_f: 'F', pygame.K_g: 'G', pygame.K_h: 'H',
            pygame.K_i: 'I', pygame.K_j: 'J', pygame.K_k: 'K', pygame.K_l: 'L',
            pygame.K_m: 'M', pygame.K_n: 'N', pygame.K_o: 'O', pygame.K_p: 'P',
            pygame.K_q: 'Q', pygame.K_r: 'R', pygame.K_s: 'S', pygame.K_t: 'T',
            pygame.K_u: 'U', pygame.K_v: 'V', pygame.K_w: 'W', pygame.K_x: 'X',
            pygame.K_y: 'Y', pygame.K_z: 'Z'}


class Ship_selection_check():
    def __init__(self):
        self.ship_selection = 1
    def ship_selection_plus(self):
        self.ship_selection += 1
    def ship_selection_minus(self):
        self.ship_selection -= 1
    def get_ship_selection(self) :
        return self.ship_selection
        
class Menu:
    def __init__(self, screen_size):
        scr_x , scr_y = pygame.display.get_surface().get_size()
        self.language_checker = Language_check()
        missile_sound = load_sound('missile.ogg')
        bomb_sound = load_sound('bomb.ogg')
        alien_explode_sound = load_sound('alien_explode.ogg')
        ship_explode_sound = load_sound('ship_explode.ogg')

        load_music('music_loop.ogg')
   
        self.speed = 1.5
        self.clockTime = 60  # maximum FPS
        self.clock = pygame.time.Clock()
        self.screen_size = screen_size
        self.ratio = (self.screen_size / 500)
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.font = pygame.font.Font("LeeSeoyun.ttf", round(21*self.ratio))
        self.font2 = pygame.font.Font("LeeSeoyun.ttf", round(20*self.ratio))
        self.player = Player(screen_size)
        # For hiscore setting 
        self.hiScores=Database().getScores()
        
        self.extremeScores=Database().getScores_extreme()
        
        self.highScoreTexts = [self.font.render("NAME", 1, RED),
                        self.font.render("SCORE", 1, RED)]
        self.highScorePos = [self.highScoreTexts[0].get_rect(
                        topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                        self.highScoreTexts[1].get_rect(
                        midtop=self.screen.get_rect().inflate(-100, -100).midtop)]
        self.extremeScoreTexts= [self.font.render("NAME", 1, RED),
                        self.font.render("SCORE", 1, RED)]
        self.extremeScorePos = [self.extremeScoreTexts[0].get_rect(
                       topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                        self.extremeScoreTexts[1].get_rect(
                        midtop=self.screen.get_rect().inflate(-100, -100).midtop)
                        ]
        for hs in self.hiScores:
            self.highScoreTexts.extend([self.font.render(str(hs[x]), 1, BLACK)
                                for x in range(2)])
            self.highScorePos.extend([self.highScoreTexts[x].get_rect(
                topleft=self.highScorePos[x].bottomleft) for x in range(-2, 0)])
        for hs in self.extremeScores:
            self.extremeScoreTexts.extend([self.font.render(str(hs[x]), 1, RED)
                                for x in range(2)])
            self.extremeScorePos.extend([self.extremeScoreTexts[x].get_rect(
                topleft=self.extremeScorePos[x].bottomleft) for x in range(-2, 0)])
        
        # For init_page setting
        self.blankText=self.font.render('       ',1,BLACK)
        self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
        self.loginText = self.font.render('LOG IN', 1, 'YELLOW')
        self.loginPos = self.loginText.get_rect(topleft=self.blankPos.bottomleft)
        self.signText=self.font.render('SIGN UP',1,'YELLOW')
        self.signPos=self.signText.get_rect(topleft=self.loginPos.bottomleft)
        self.quitText=self.font.render('QUIT',1,'YELLOW')
        self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
        
        # For login_page setting
        self.id=Var.initial_id # 초기화
        self.idBuffer = []
        self.pwd=''
        self.pwdBuffer= []
        self.enterIdText=0
        self.enterIdPos=0
        self.idText =0
        self.idPos = 0
        self.enterPwdText=0
        self.enterPwdPos=0
        self.pwdText = 0
        self.pwdPos =0
        self.secretPwd=0
        

        # For select_character setting
        self.selectchar=False
        self.ship1, self.ship1Rect = load_image('ship.png')
        self.ship1Rect.bottomleft = self.screen.get_rect().inflate(-140, -350).bottomleft
        self.ship2, self.ship2Rect = load_image('ship2.png')
        self.ship2Rect.bottomleft = self.screen.get_rect().inflate(-370, -350).bottomleft 
        self.ship3, self.ship3Rect = load_image('ship3.png')
        self.ship3Rect.bottomleft = self.screen.get_rect().inflate(-600, -350).bottomleft
        self.ship4, self.ship4Rect = load_image('ship4.png')
        self.ship4Rect.bottomleft = self.screen.get_rect().inflate(-830, -350).bottomleft

        self.ship1text = self.font.render('Ship1', 1, RED)
        self.ship2text = self.font.render('Ship2', 1, RED)
        self.ship3text = self.font.render('Ship3', 1, RED)
        self.ship4text = self.font.render('Ship4', 1, RED)
        self.ship1Pos = self.ship1text.get_rect(midbottom=self.ship1Rect.inflate(0, 0).midbottom)
        self.ship2Pos = self.ship2text.get_rect(midbottom=self.ship2Rect.inflate(0, 0).midbottom)
        self.ship3Pos = self.ship3text.get_rect(midbottom=self.ship3Rect.inflate(0, 0).midbottom)
        self.ship4Pos = self.ship4text.get_rect(midbottom=self.ship4Rect.inflate(0, 0).midbottom)


        self.shipDict={1:self.ship1Pos,2:self.ship2Pos,3:self.ship3Pos,4:self.ship4Pos}
        Var.go_menu=False
        
        #For store_page setting
        self.store=False
        self.buychar=False

        # for character setting
        self.char_setting=False

        # For inMenu_page setting
        
        self.startText = self.font.render('SELECT MODE', 1, 'GREEN')
        self.startPos = self.startText.get_rect(topleft=self.blankPos.bottomleft)
        self.hiScoreText = self.font.render('HIGH SCORE', 1, 'GREEN')
        self.hiScorePos = self.hiScoreText.get_rect(topleft=self.startPos.bottomleft)
        self.fxText = self.font.render('SOUND FX ', 1, 'YELLOW')
        self.fxPos = self.fxText.get_rect(topleft=self.hiScorePos.bottomleft)
        self.fxOnText = self.font.render('ON', 1, RED)
        self.fxOffText = self.font.render('OFF', 1, RED)
        self.fxOnPos = self.fxOnText.get_rect(topleft=self.fxPos.topright)
        self.fxOffPos = self.fxOffText.get_rect(topleft=self.fxPos.topright)
        self.musicText = self.font.render('MUSIC', 1, 'YELLOW')
        self.musicPos = self.fxText.get_rect(topleft=self.fxPos.bottomleft)
        self.musicOnText = self.font.render('ON', 1, RED)
        self.musicOffText = self.font.render('OFF', 1, RED)
        self.musicOnPos = self.musicOnText.get_rect(topleft=self.musicPos.topright)
        self.musicOffPos = self.musicOffText.get_rect(topleft=self.musicPos.topright)
        self.shopText = self.font.render('SHOP', 1, 'GREEN')
        self.shopPos = self.shopText.get_rect(topleft=self.musicPos.bottomleft)
        self.charsettingText = self.font.render('CHAR SETTING', 1, 'GREEN')
        self.charsettingPos = self.charsettingText.get_rect(topleft=self.shopPos.bottomleft)
        self.helpText=self.font.render('HELP',1,'YELLOW')
        self.helpPos=self.helpText.get_rect(topleft=self.charsettingPos.bottomleft)
        self.quitText = self.font.render('QUIT', 1, 'YELLOW')
        self.quitPos = self.quitText.get_rect(topleft=self.helpPos.bottomleft)
        self.languageText = self.font2.render('언어 변경', 1, 'YELLOW')
        self.languagePos = self.languageText.get_rect(topleft=self.quitPos.bottomleft)


        # For Select Mode setting
        self.singleText = self.font.render('SINGLE MODE', 1, 'WHITE')
        self.singlePos = self.singleText.get_rect(midtop=self.screen.get_rect().center)
        self.extremeText = self.font.render('EXTREME MODE', 1, "WHITE")
        self.extremePos = self.extremeText.get_rect(topleft=self.singlePos.bottomleft)
        self.pvpText = self.font.render('PVP MODE ', 1, 'WHITE')
        self.pvpPos = self.pvpText.get_rect(topleft=self.extremePos.bottomleft)
        self.backText=self.font.render('BACK',1,'WHITE')
        self.backPos=self.backText.get_rect(topleft=self.pvpPos.bottomleft)
        self.selectText = self.font.render('*', 1, 'YELLOW')
        self.selectPos =self.selectText.get_rect(topright=self.singlePos.topleft)
        
        
        # ship change 
        self.ship1, self.ship1Rect = load_image('ship.png')
        self.ship1Rect.bottomleft = self.screen.get_rect().inflate(-112, -300).bottomleft


        self.shipCoin, self.shipCoinRect = load_image('coin.png')      #기체변경 창에서 코인 이미지
        self.shipCoinRect.bottomleft = self.screen.get_rect().inflate(-112, -100).bottomleft 
        
        # shop variable
        self.ship1Text = self.font.render('', 1, BLACK)
        self.ship2Text = self.font.render('', 1, BLACK)
        self.ship3Text = self.font.render('', 1, BLACK)
        self.ship4Text = self.font.render('', 1, BLACK)
        self.ship_selectText = self.font.render('SELECT', 1, BLACK)
       
        self.ship1Pos = self.ship1Text.get_rect(midbottom=self.ship1Rect.inflate(0, 0).midbottom)
        self.ship2Pos = self.ship2Text.get_rect(midbottom=self.ship2Rect.inflate(0, 0).midbottom)
        self.ship3Pos = self.ship3Text.get_rect(midbottom=self.ship3Rect.inflate(0, 0).midbottom)
        self.ship4Pos = self.ship4Text.get_rect(midbottom=self.ship4Rect.inflate(0, 0).midbottom)
        self.ship_selectPos = self.ship_selectText.get_rect(midbottom=self.ship1Rect.inflate(0, 60).midbottom)
      
        self.ship_menuDict = {1: self.ship1Pos, 2: self.ship2Pos, 3: self.ship3Pos, 4: self.ship4Pos}
            
        ## 상점 이미지나 배경 추가할 거면 여기 수정
        # self.title, self.titleRect = load_image('title.png')
        # self.titleRect.midtop = self.screen.get_rect().inflate(0, 0).midtop
        
        # For selection '*' setting        
        self.selectText = self.font.render('*', 1, 'YELLOW')
        self.selextPos=''
        self.selectModeDict = {1:self.singlePos,2:self.extremePos,3:self.pvpPos,4:self.backPos}
        self.menuDict = {1: self.startPos, 2: self.hiScorePos, 3:self.fxPos, 4: self.musicPos, 5:self.helpPos,6: self.quitPos}
        self.selectScoresDict = {1:self.singlePos,2:self.extremePos,3:self.backPos}
        self.menuDict = {1: self.loginPos, 2: self.signPos,3:self.quitPos}
        self.loginDict={}
        self.selection = 1
        self.ininitalMenu=True
        self.showlogin=False
        self.showsign=False
        self.textOverlays=0
        self.inMenu = False
        self.showHelp=False
        self.showSelectModes=False
        self.showHiScores = False
        self.inSelectMenu=False
        self.soundFX = Database.getSound()
        self.music = Database.getSound(music=True)
        self.showselectchar=False
        self.ship_selection = Ship_selection_check()
        self.showShop = False
        

    def init_page(self):        
        while self.ininitalMenu:
            self.clock.tick(self.clockTime) 
            
            main_menu, main_menuRect = load_image("main_menu.png")
            main_menu = pygame.transform.scale(main_menu, (500, 500))
            main_menuRect.midtop = self.screen.get_rect().midtop
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))

            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 350:
                        self.screen_size = 350
                    if self.screen_size >= 900:
                        self.screen_size = 900
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if self.showlogin:
                        self.showlogin = False
                    elif self.selection == 1:
                        self.showlogin=True 
                        self.ininitalMenu = False
                        return 1, self.screen_size
                    elif self.selection == 2:
                        return 2, self.screen_size
                    elif self.selection == 3:
                        return 3, self.screen_size
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not self.showlogin):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(menuDict)
                    and not self.showlogin):
                    self.selection += 1
            self.blankText=self.font.render('       ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.loginText = self.font.render('LOG IN', 1, 'YELLOW')
            self.loginPos = self.loginText.get_rect(topleft=self.blankPos.bottomleft)
            self.signText=self.font.render('SIGN UP',1,'YELLOW')
            self.signPos=self.signText.get_rect(topleft=self.loginPos.bottomleft)
            self.quitText=self.font.render('QUIT',1,'YELLOW')
            self.quitPos=self.quitText.get_rect(topleft=self.signPos.bottomleft)
            menuDict = {1: self.loginPos, 2: self.signPos,3:self.quitPos}
            self.selectPos = self.selectText.get_rect(topright=menuDict[self.selection].topleft)
            self.textOverlays = zip([self.blankText,self.loginText, self.signText,self.quitText,self.selectText],
                                [self.blankPos,self.loginPos, self.signPos,self.quitPos,self.selectPos])

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()
    

    def login_sign_page(self,userSelection):
        self.showlogin=True
        self.ininitalMenu=False
        while self.showlogin:
            self.clock.tick(self.clockTime) 

            main_menu, main_menuRect = load_image("main_menu.png")
            main_menu = pygame.transform.scale(main_menu, (600, 600))
            main_menuRect.midtop = self.screen.get_rect().midtop
            self.ratio = (self.screen_size / 600)
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))

            for event in pygame.event.get():
                scr_x , scr_y = pygame.display.get_surface().get_size()
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 350:
                        self.screen_size = 350
                    if self.screen_size >= 900:
                        self.screen_size = 900
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 600)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if (self.selection==1
                    or self.selection==2) :
                        
                        if userSelection==1: # login
                            if Database().id_not_exists(self.id):
                                print("아이디 없음")
                            else:  #로그인 시 캐릭터 불러오기
                                if Database().compare_data(self.id, self.pwd):
                                    Var.char=Database().load_char_data(self.id)
                                    print("로그인 성공")
                                    #print(Var.lst)
                                    Var.user_id=self.id    # 아이디 저장
                                    if Var.char==1:
                                        Var.lst=Var.char1_lst
                                    elif Var.char==2:
                                        Var.lst=Var.char2_lst
                                    elif Var.char==3:
                                        Var.lst=Var.char3_lst
                                    elif Var.char==4:
                                        Var.lst=Var.char4_lst
                                    elif Var.char==5:
                                        Var.lst=Var.char5_lst
                                    elif Var.char==6:
                                        Var.lst=Var.char6_lst
                                    elif Var.char==7:
                                        Var.lst=Var.char7_lst
                                    return self.id, self.screen_size
                                else:
                                    print("비번 확인")
                        elif userSelection==2: # signup
                            if Database().id_not_exists(self.id):
                                print("아이디 없음")
                                if self.pwd!='':
                                    Database().add_id_data(self.id)
                                    Database().add_password_data(self.pwd, self.id)
                                    Var.user_id=self.id
                                    print("회원가입 성공")
        
                                    print('Select your ship')
                                    
                                    return self.id, self.screen_size
                            else:
                                print("아이디 존재함")
                    
                    elif self.selection == 3:
                        return False, self.screen_size
                    
                elif (event.type == pygame.KEYDOWN
                    and self.selection==1
                    and event.key in Keyboard.keys.keys()
                    and len(self.idBuffer) < 9):
                    self.idBuffer.append(Keyboard.keys[event.key])
                    self.id = ''.join(self.idBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==1
                    and event.key == pygame.K_BACKSPACE
                    and len(self.idBuffer) > 0):
                    self.idBuffer.pop()
                    self.id = ''.join(self.idBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==2
                    and event.key in Keyboard.keys.keys()
                    and len(self.pwdBuffer) < 9):
                    self.pwdBuffer.append(Keyboard.keys[event.key])
                    self.pwd = ''.join(self.pwdBuffer)
                elif (event.type == pygame.KEYDOWN
                    and self.selection==2
                    and event.key == pygame.K_BACKSPACE
                    and len(self.pwdBuffer) > 0):
                    self.pwdBuffer.pop()
                    self.pwd = ''.join(self.pwdBuffer)
                    
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.loginDict)):
                    self.selection += 1

            self.blankText=self.font.render('     ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.enterIdText=self.font.render('ID  ',1,BLACK)
            self.enterIdPos=self.enterIdText.get_rect(topleft=self.blankPos.bottomleft)
            self.idText = self.font.render(str(self.id), 1, WHITE) #??
            self.idPos = self.idText.get_rect(topleft=self.enterIdPos.bottomleft)
            self.enterPwdText=self.font.render('PWD',1,BLACK)
            self.enterPwdPos=self.enterPwdText.get_rect(topleft=self.idPos.bottomleft)
            self.secretPwd='*'*len(self.pwd)
            self.pwdText = self.font.render(self.secretPwd, 1, WHITE)
            self.pwdPos = self.pwdText.get_rect(topleft=self.enterPwdPos.bottomleft)
            self.backText = self.font.render('BACK', 1, BLACK)
            self.backPos = self.backText.get_rect(topleft=self.pwdPos.bottomleft)
            self.selectText = self.font.render('*', 1, BLACK)
            self.loginDict={1:self.idPos,2:self.pwdPos,3:self.backPos}
            self.selectPos = self.selectText.get_rect(topright=self.loginDict[self.selection].topleft)
            self.textOverlays = zip([self.blankText,self.enterIdText, self.idText,self.enterPwdText,self.pwdText,self.selectText,self.backText],
                                [self.blankPos,self.enterIdPos, self.idPos,self.enterPwdPos,self.pwdPos,self.selectPos,self.backPos])

            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()
    
    
    
    def set_character(self):
        self.selectchar=True
        
        while self.selectchar:
            self.clock.tick(self.clockTime) 
            self.flag=True
            main_menu, main_menuRect = load_image("main_menu.png")
            main_menu = pygame.transform.scale(main_menu, (500, 500))
            main_menuRect.midtop = self.screen.get_rect().midtop
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))

            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 350:
                        self.screen_size = 350
                    if self.screen_size >= 900:
                        self.screen_size = 900
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if self.showselectchar:
                        self.showselectchar=False
                    elif self.selection==1:
                        Var.char=1
                        Var.lst=Var.char1_lst
                        Database().update_char_have(Var.user_id,'ship1') # char_have테이블 갱신
                        
                        #Var.user_id=self.id
                        Var.go_menu=True
                        Database().update_char_data(Var.char,Var.user_id)
                        return Var.go_menu
                    elif self.selection==2:
                        Var.char=2
                        
                        Var.lst=Var.char2_lst
                        Database().update_char_have(Var.user_id,'ship2')
                     
                        Var.go_menu=True
                        Database().update_char_data(Var.char,Var.user_id)
                        return Var.go_menu
                    elif self.selection==3:
                        Var.char=3
                        
                        Var.lst=Var.char3_lst
                       
                        Database().update_char_have(Var.user_id,'ship3')
                        Var.go_menu=True
                        Database().update_char_data(Var.char,Var.user_id)
                        return Var.go_menu
                    elif self.selection==4:
                        Var.char=4
                        
                        Var.lst=Var.char4_lst
                        
                        Database().update_char_have(Var.user_id,'ship4')
                        Database().update_char_data(Var.char,Var.user_id)
                        Var.go_menu=True
                        
                        return Var.go_menu
                    

                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT
                    and self.selection>1 and not self.showselectchar ):
                        self.selection-=1
                
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT

                    and self.selection<len(self.shipDict) and not self.showselectchar ):
                        self.selection+=1

            #self.blankText=self.font.render('           ',1,BLACK)
            #self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            # image는 로드만, text로 선택
            self.ship1, self.ship1Rect = load_image('ship.png')
            self.ship1.set_colorkey((0,0,0,0))
            self.ship1Rect.bottomleft = self.screen.get_rect().inflate(-140, -350).bottomleft
            self.ship2, self.ship2Rect = load_image('ship2.png')
            self.ship2.set_colorkey((0,0,0,0))
            self.ship2Rect.bottomleft = self.screen.get_rect().inflate(-370, -350).bottomleft 
            self.ship3, self.ship3Rect = load_image('ship3.png')
            self.ship3.set_colorkey((0,0,0,0))
            self.ship3Rect.bottomleft = self.screen.get_rect().inflate(-600, -350).bottomleft
            self.ship4, self.ship4Rect = load_image('ship4.png')
            self.ship4.set_colorkey((0,0,0,0))
            self.ship4Rect.bottomleft = self.screen.get_rect().inflate(-830, -350).bottomleft

            self.ship1text = self.font.render('Ship1', 1, RED)
            self.ship2text = self.font.render('Ship2', 1, RED)
            self.ship3text = self.font.render('Ship3', 1, RED)
            self.ship4text = self.font.render('Ship4', 1, RED)
            self.ship1Pos = self.ship1text.get_rect(midbottom=self.ship1Rect.inflate(0, 0).midbottom)
            self.ship2Pos = self.ship2text.get_rect(midbottom=self.ship2Rect.inflate(0, 0).midbottom)
            self.ship3Pos = self.ship3text.get_rect(midbottom=self.ship3Rect.inflate(0, 0).midbottom)
            self.ship4Pos = self.ship4text.get_rect(midbottom=self.ship4Rect.inflate(0, 0).midbottom)


            self.screen.blit(self.ship1, self.ship1Rect)
            self.screen.blit(self.ship2, self.ship2Rect)
            self.screen.blit(self.ship3, self.ship3Rect)
            self.screen.blit(self.ship4, self.ship4Rect)

            self.shipDict={1:self.ship1Pos,2:self.ship2Pos,3:self.ship3Pos,4:self.ship4Pos}
            self.selectText = self.font.render('SELECT', 1, RED)
            self.selectPos = self.selectText.get_rect(midbottom=self.shipDict[self.selection].inflate(0,60).midbottom)

            self.textOverlays=zip([self.ship1text,self.ship2text,self.ship3text,self.ship4text,self.selectText],
            [self.ship1Pos,self.ship2Pos,self.ship3Pos,self.ship4Pos,self.selectPos])
            for txt,pos in self.textOverlays:
                self.screen.blit(txt,pos)
            pygame.display.flip()
                    
    


    
    def inMenu_page(self):
        load_music('music_loop.ogg')
        self.inMenu = True
        cnt=0
        scr_x , scr_y = pygame.display.get_surface().get_size()
        while self.inMenu:
            self.clock.tick(self.clockTime) 
            self.flag=True
            main_menu, main_menuRect = load_image("main_menu.png")
            main_menu = pygame.transform.scale(main_menu, (500, 500))
            main_menuRect.midtop = self.screen.get_rect().midtop
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))
 
            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 350:
                        self.screen_size = 350
                    if self.screen_size >= 900:
                        self.screen_size = 900
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN and not self.showShop):
                    if self.showSelectModes:
                        self.showSelectModes = False
                    elif self.showHelp:
                        cnt+=1
                        if cnt%2!=0:
                            self.showHelp=True
                        else:
                            self.showHelp=False
                    elif self.selection == 1:
                        return 1, self.screen_size
                    elif self.selection == 2:
                        return 2, self.screen_size
                    elif self.selection == 3:
                        self.soundFX = not self.soundFX
                        if self.soundFX:
                            missile_sound.play()  ## 수정해야함
                        Database.setSound(int(self.soundFX))
                    elif self.selection == 4 and pygame.mixer:
                        self.music = not self.music
                        if self.music:
                            pygame.mixer.music.play(loops=-1)
                        else:
                            pygame.mixer.music.stop()
                        Database.setSound(int(self.music), music=True)
                    elif self.selection == 5:
                        self.store=True
                        return 5, self.screen_size
                        
                    elif self.selection==6: # character setting page 
                        self.char_setting=True
                        return 6,self.screen_size
                    elif self.selection == 7:
                        cnt+=1
                        self.showHelp=True                                        
                    elif self.selection == 8:
                        return 8, self.screen_size
                    elif self.selection == 9:
                        self.language_checker.change_language()
                    elif self.selection == 9:
                        self.showlogin=True
                        self.inSelectMenu=True
                        
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not self.showHiScores
                    and not self.showSelectModes
                    and not self.showHelp
                    and not self.store
                    and not self.char_setting):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.menuDict)
                    and not self.showHiScores
                    and not self.showSelectModes
                    and not self.store
                    and not self.char_setting):
                    self.selection += 1
                #ship 고르기
               
            
            if not self.language_checker.get_language():
                self.blankText=self.font.render('           ',1,BLACK)
                self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
                self.startText = self.font.render('SELECT MODE', 1, 'GREEN')
                self.startPos = self.startText.get_rect(topleft=self.blankPos.bottomleft)
                self.hiScoreText = self.font.render('HIGH SCORE', 1, 'GREEN')
                self.hiScorePos = self.hiScoreText.get_rect(topleft=self.startPos.bottomleft)
                self.fxText = self.font.render('SOUND FX ', 1, 'YELLOW')
                self.fxPos = self.fxText.get_rect(topleft=self.hiScorePos.bottomleft)
                self.fxOnText = self.font.render('ON', 1, RED)
                self.fxOffText = self.font.render('OFF', 1, RED)
                self.fxOnPos = self.fxOnText.get_rect(topleft=self.fxPos.topright)
                self.fxOffPos = self.fxOffText.get_rect(topleft=self.fxPos.topright)
                self.musicText = self.font.render('MUSIC', 1, 'YELLOW')
                self.musicPos = self.fxText.get_rect(topleft=self.fxPos.bottomleft)
                self.musicOnText = self.font.render('ON', 1, RED)
                self.musicOffText = self.font.render('OFF', 1, RED)
                self.musicOnPos = self.musicOnText.get_rect(topleft=self.musicPos.topright)
                self.musicOffPos = self.musicOffText.get_rect(topleft=self.musicPos.topright)
                self.shopText = self.font.render('SHOP', 1, 'GREEN')
                self.shopPos = self.shopText.get_rect(topleft=self.musicPos.bottomleft)
                self.charsettingText = self.font.render('CHAR SETTING', 1, 'GREEN')
                self.charsettingPos = self.charsettingText.get_rect(topleft=self.shopPos.bottomleft)
                self.helpText=self.font.render('HELP',1,'YELLOW')
                self.helpPos=self.helpText.get_rect(topleft=self.charsettingPos.bottomleft)
                self.quitText = self.font.render('QUIT', 1, 'YELLOW')
                self.quitPos = self.quitText.get_rect(topleft=self.helpPos.bottomleft)
                self.languageText = self.font2.render('언어 변경', 1, 'YELLOW')
                self.languagePos = self.languageText.get_rect(topleft=self.quitPos.bottomleft)


            else:
                self.blankText=self.font.render('           ',1,BLACK)
                self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
                self.startText = self.font2.render('모드 설정', 1, 'GREEN')
                self.startPos = self.startText.get_rect(topleft=self.blankPos.bottomleft)
                self.hiScoreText = self.font2.render('점수 기록', 1, 'GREEN')
                self.hiScorePos = self.hiScoreText.get_rect(topleft=self.startPos.bottomleft)
                self.fxText = self.font2.render('효과음   ', 1, 'YELLOW')
                self.fxPos = self.fxText.get_rect(topleft=self.hiScorePos.bottomleft)
                self.fxOnText = self.font2.render('켜짐', 1, RED)
                self.fxOffText = self.font2.render('꺼짐', 1, RED)
                self.fxOnPos = self.fxOnText.get_rect(topleft=self.fxPos.topright)
                self.fxOffPos = self.fxOffText.get_rect(topleft=self.fxPos.topright)
                self.musicText = self.font2.render('음악', 1, 'YELLOW')
                self.musicPos = self.fxText.get_rect(topleft=self.fxPos.bottomleft)
                self.musicOnText = self.font2.render('켜짐', 1, RED)
                self.musicOffText = self.font2.render('꺼짐', 1, RED)
                self.musicOnPos = self.musicOnText.get_rect(topleft=self.musicPos.topright)
                self.musicOffPos = self.musicOffText.get_rect(topleft=self.musicPos.topright)
                self.shopText = self.font2.render('상점', 1,'GREEN')
                self.shopPos = self.shopText.get_rect(topleft=self.musicPos.bottomleft)
                self.charsettingText = self.font.render('캐릭터 변경', 1, 'GREEN')
                self.charsettingPos = self.charsettingText.get_rect(topleft=self.shopPos.bottomleft)
                self.helpText=self.font2.render('도움말',1,'YELLOW')
                self.helpPos=self.helpText.get_rect(topleft=self.charsettingPos.bottomleft)
                self.quitText = self.font2.render('게임 종료', 1, 'YELLOW')
                self.quitPos = self.quitText.get_rect(topleft=self.helpPos.bottomleft)
                self.languageText = self.font2.render('LANGUAGE CHANGE', 1, 'YELLOW')
                self.languagePos = self.languageText.get_rect(topleft=self.quitPos.bottomleft)


            self.menuDict = {1: self.startPos, 2: self.hiScorePos, 3:self.fxPos, 4: self.musicPos, 5:self.shopPos,6:self.charsettingPos, 7:self.helpPos, 8: self.quitPos, 9: self.languagePos}

            self.ship_selectPos = self.ship_selectText.get_rect(midbottom=self.ship_menuDict[self.ship_selection.get_ship_selection()].inflate(0,60).midbottom)
            self.selectPos = self.selectText.get_rect(topright=self.menuDict[self.selection].topleft)


            if self.showHelp:
                if cnt%2==1:
                    menu, menuRect = load_image("help1.png")
                    menuRect.midtop = self.screen.get_rect().midtop
                    menu_size = (600,600)
                    self.screen.blit(pygame.transform.scale(menu, menu_size), (0,0))

                    
           # elif self.char_setting:
            #    CharStore(self.screen_size).char_setting()
            elif self.showShop:
                # self.screen.blit(self.title,self.titleRect)
                self.screen.blit(self.ship1, self.ship1Rect)
                self.screen.blit(self.ship2, self.ship2Rect)
                self.screen.blit(self.ship3, self.ship3Rect)
                self.screen.blit(self.ship4, self.ship4Rect)
                self.screen.blit(self.shipCoin, self.shipCoinRect)
                self.textOverlays = zip([self.ship1Text,self.ship2Text,self.ship3Text,self.ship4Text,self.ship_selectText,self.shipUI_coinText,self.shipUnlockText],[self.ship1Pos,self.ship2Pos,self.ship3Pos,self.ship4Pos,self.ship_selectPos,self.shipUI_coinPos,self.shipUnlockPos])
            
            else:
                self.textOverlays = zip([self.blankText,self.startText, self.hiScoreText, self.helpText, self.fxText,
                                    self.musicText, self.shopText, self.charsettingText,self.quitText, self.selectText,
                                    self.fxOnText if self.soundFX else self.fxOffText,
                                    self.musicOnText if self.music else self.musicOffText,self.languageText],
                                [self.blankPos,self.startPos, self.hiScorePos, self.helpPos, self.fxPos,
                                    self.musicPos, self.shopPos, self.charsettingPos,self.quitPos, self.selectPos,
                                    self.fxOnPos if self.soundFX else self.fxOffPos,
                                    self.musicOnPos if self.music else self.musicOffPos,self.languagePos])
            for txt, pos in self.textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()

    def select_game_page(self):
        main_menu, main_menuRect = load_image("main_menu.png")
        main_menu = pygame.transform.scale(main_menu, (500, 500))
        main_menuRect.midtop = self.screen.get_rect().midtop
        inSelectMenu=True
        showSingleMode = False
        showExtremeMode = False
        showPvpMode = False
        
        while inSelectMenu:
            self.clock.tick(self.clockTime)
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))

            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 350:
                        self.screen_size = 350
                    if self.screen_size >= 900:
                        self.screen_size = 900
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if showSingleMode:
                        showSingleMode = False
                    elif showExtremeMode:
                        showExtremeMode = False
                    elif showPvpMode:
                        showPvpMode = False
                    elif self.selection == 1:
                        inSelectMenu = False
                        selectMode = 'SingleMode'
                        return selectMode, self.screen_size
                    elif self.selection == 2:
                        inSelectMenu = False
                        selectMode = 'ExtremeMode'
                        return selectMode, self.screen_size
                    elif self.selection == 3:
                        inSelectMenu = False
                        selectMode = 'PvpMode'
                        return selectMode, self.screen_size
                    elif self.selection == 4:
                        inSelectMenu = False
                        return BACK, self.screen_size
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not showSingleMode
                    and not showExtremeMode
                    and not showPvpMode):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.selectModeDict)
                    and not showSingleMode
                    and not showExtremeMode
                    and not showPvpMode):
                    self.selection += 1
            
            self.blankText=self.font.render('       ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.singleText = self.font.render('SINGLE', 1, 'WHITE')
            self.singlePos = self.singleText.get_rect(topleft=self.blankPos.bottomleft)
            self.extremeText = self.font.render('EXTREME', 1, 'WHITE')
            self.extremePos = self.extremeText.get_rect(topleft=self.singlePos.bottomleft)
            self.pvpText = self.font.render('PVP', 1, 'WHITE')
            self.pvpPos = self.pvpText.get_rect(topleft=self.extremePos.bottomleft)
            self.backText=self.font.render('BACK',1,'WHITE')
            self.backPos=self.backText.get_rect(topleft=self.pvpPos.bottomleft)
            
            self.selectModeDict = {1:self.singlePos,2:self.extremePos,3:self.pvpPos,4:self.backPos}
            self.selectText = self.font.render('*', 1, 'WHITE')
            self.selectPos = self.selectText.get_rect(topright=self.selectModeDict[self.selection].topleft)

            textOverlays = zip([self.blankText,self.singleText,self.extremeText,self.pvpText,self.selectText,self.backText],
            [self.blankPos,self.singlePos,self.extremePos,self.pvpPos,self.selectPos,self.backPos])
            for txt, pos in textOverlays:
                self.screen.blit(txt, pos)
            
            pygame.display.flip()
    

    def score_page(self):
        main_menu, main_menuRect = load_image("main_menu.png")
        main_menu = pygame.transform.scale(main_menu, (500, 500))
        main_menuRect.midtop = self.screen.get_rect().midtop

        inScoreMenu=True
        showSingleScores =False
        showextremeScores=False

        while inScoreMenu:
            self.clock.tick(self.clockTime)
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0))
            for event in pygame.event.get():
                if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Resize windowSize
                elif (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                    if showSingleScores:
                        showSingleScores = False
                    elif showextremeScores:
                        showextremeScores = False
                    elif self.selection == 1:
                        showSingleScores=True 
                    elif self.selection == 2:
                        showextremeScores = True
                    elif self.selection == 3:
                        return BACK, self.screen_size 
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_UP
                    and self.selection > 1
                    and not showSingleScores
                    and not showextremeScores):
                    self.selection -= 1
                elif (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_DOWN
                    and self.selection < len(self.selectScoresDict)
                    and not showSingleScores
                    and not showextremeScores):
                    self.selection += 1 

            self.blankText=self.font.render('      ',1,BLACK)
            self.blankPos=self.blankText.get_rect(topright=self.screen.get_rect().center)
            self.singleText=self.font.render('SINGLE  ',1,'WHITE')
            self.singlePos=self.singleText.get_rect(topleft=self.blankPos.bottomleft)
            self.extremeText = self.font.render('EXTREME', 1, "WHITE")
            self.extremePos = self.extremeText.get_rect(topleft=self.singlePos.bottomleft)
            self.backText = self.font.render('BACK', 1, 'WHITE')
            self.backPos = self.backText.get_rect(topleft=self.extremePos.bottomleft)

            selectScoresDict = {1:self.singlePos,2:self.extremePos,3:self.backPos}
            self.selectPos= self.selectText.get_rect(topright=selectScoresDict[self.selection].topleft)

            self.highScoreTexts = [self.font.render("NAME", 1, RED), #폰트 렌터
                            self.font.render("SCORE", 1, RED)]
            self.highScorePos = [self.highScoreTexts[0].get_rect(
                            topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                            self.highScoreTexts[1].get_rect(
                            midtop=self.screen.get_rect().inflate(-100, -100).midtop)]
            self.extremeScoreTexts= [self.font.render("NAME", 1, RED), #폰트 렌터
                            self.font.render("SCORE", 1, RED)
                            ]
            self.extremeScorePos = [self.extremeScoreTexts[0].get_rect(
                            topleft=self.screen.get_rect().inflate(-100, -100).topleft),
                            self.extremeScoreTexts[1].get_rect(
                            midtop=self.screen.get_rect().inflate(-100, -100).midtop)
                            ]

            #single score page
            self.hiScores=Database().getScores()
            for hs in self.hiScores:
                self.highScoreTexts.extend([self.font.render(str(hs[x]), 1, RED)
                                    for x in range(2)]) 
                self.highScorePos.extend([self.highScoreTexts[x].get_rect(
                    topleft=self.highScorePos[x].bottomleft) for x in range(-2, 0)])
            #extreme score page
            self.extremeScores=Database().getScores_extreme()
            for hs in self.extremeScores:
                self.extremeScoreTexts.extend([self.font.render(str(hs[x]), 1, RED)
                                    for x in range(2)])
                self.extremeScorePos.extend([self.extremeScoreTexts[x].get_rect(
                    topleft=self.extremeScorePos[x].bottomleft) for x in range(-2, 0)])

            if showSingleScores:
                menu, menuRect = load_image("menu.png")
                menuRect.midtop = self.screen.get_rect().midtop
                menu_size = (round(menu.get_width() * self.ratio), round(menu.get_height() * self.ratio))
                self.screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
                textOverlays = zip(self.highScoreTexts, self.highScorePos)
            elif showextremeScores:
                menu, menuRect = load_image("menu.png")
                menuRect.midtop = self.screen.get_rect().midtop
                menu_size = (round(menu.get_width() * self.ratio), round(menu.get_height() * self.ratio))
                self.screen.blit(pygame.transform.scale(menu, menu_size), (0,0))
                textOverlays = zip(self.extremeScoreTexts, self.extremeScorePos)
            else:
                textOverlays = zip([self.blankText,self.singleText, self.extremeText,self.backText,self.selectText],
                                [self.blankPos,self.singlePos, self.extremePos,self.backPos, self.selectPos])
            for txt, pos in textOverlays:
                self.screen.blit(txt, pos)
            pygame.display.flip()