import pygame
import sys
from pygame import display
from pygame import Rect
from pygame import transform
from pygame import time
from pygame import Surface
from pygame.locals import RESIZABLE, RLEACCEL
from load import load_image,Var
from load import *
from menu import *
from database import Database

#for store setting
full_screen=False

global user_font
#global item_price_offset


scr_size=(width,height)=(600,600) # default
resized_screen = display.set_mode((scr_size), RESIZABLE)
screen=resized_screen.copy()
width_offset=0.3
resized_screen_center = (0, 0)
FPS=60
CHAR_SIZE = 60
USER_ITEM_SIZE=20
showstore=False
Black=(0,0,0)
clock=time.Clock()
instore=False
global selection
selection=1

class Store(object):
    def __init__(self,screen_size):
        
        self.screen_size=screen_size
        self.screen=pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.ratio = (self.screen_size / 500)
        self.font = pygame.font.Font("LeeSeoyun.ttf", round(21*self.ratio))
        self.clock = pygame.time.Clock()
        self.clockTime = 60
        self.main_menu, self.main_menuRect = load_image("main_menu.png")
        self.main_menu = pygame.transform.scale(self.main_menu, (500, 500))
        self.main_menuRect.midtop = self.screen.get_rect().midtop
        self.main_menu_size = (round(self.main_menu.get_width() * self.ratio), round(self.main_menu.get_height() * self.ratio))
        self.screen.blit(pygame.transform.scale(self.main_menu, self.main_menu_size), (0,0))
        self.active=False
        self.selection=1
        self.user_id=Var.user_id
        self.coin_item_count=Database().load_coin(self.user_id)
        self.width=self.screen.get_width()
        self.height=self.screen.get_height()
        
        

    def open(self):
        self.active=True
        self.selection=1

    def close(self):
        self.active=False
    
    def r_selection(self):
        self.selection+=1
        if self.selection>4:
            self.selection=1

    def l_selection(self):
        self.selection-=1
        if self.selection<1:
            self.selection=4

    
    def update_coin_text(self):
        coin_color=(255,0,0)
        self.coin_image,self.coin_rect=load_image('coin.png')
        self.coin_image=transform.scale(self.coin_image,(30,30))
        self.coin_image.set_colorkey((0,0,0))
        #self.coin_rect.centerx=self.width *0.68
        #self.coin_rect.centery=self.height*0.39
        self.coin_rect.topright=(self.width*0.7,self.height*0.2)

        
        self.coin_item_count=Database().load_coin(self.user_id)
        user_coin=self.font.render(f'X{self.coin_item_count}',True,coin_color)
        user_c_rect=user_coin.get_rect(topright=(self.width*(0.7+0.07),self.height*0.2))
        self.screen.blit(self.coin_image,self.coin_rect)
        self.screen.blit(user_coin,user_c_rect)

   
class CharStore(Store):
    def __init__(self,screen_size):
        super().__init__(screen_size)
        self.ship1_image,self.ship1_rect=load_image('ship.png')
        self.ship2_image,self.ship2_rect=load_image('ship2.png')
        self.ship3_image,self.ship3_rect=load_image('ship3.png')
        self.ship4_image,self.ship4_rect=load_image('ship4.png')
        
        
        self.s1_price=Database().load_shipprice('ship1')
        self.s2_price=Database().load_shipprice('ship2')
        self.s3_price=Database().load_shipprice('ship3')
        self.s4_price=Database().load_shipprice('ship4')
        self.char_set=False

        #갖고있으면1
        self.ship1_have=Database().check_char_have(self.user_id,'ship1')
        self.ship2_have=Database().check_char_have(self.user_id,'ship2')
        self.ship3_have=Database().check_char_have(self.user_id,'ship3')
        self.ship4_have=Database().check_char_have(self.user_id,'ship4')
        

    def update(self,price,char):
        # coin 업데이트
        Database().buy_char(self.user_id,price)
        # 캐릭터 업데이트
        Database().update_char_data(char,self.user_id)


            
    def make_selection(self):
       
        if self.selection==1 and self.coin_item_count > self.s1_price and not self.ship1_have:
            
            Var.char=1
            Var.char_lst=Var.char1_lst
            Database().update_char_have(self.user_id,'ship1') # 구매하면 1로 업데이트
            self.update(self.s1_price,1)

        elif self.selection==2 and self.coin_item_count > self.s2_price and not self.ship2_have:
            
            Var.char=2
            Var.char_lst=Var.char2_lst
            Database().update_char_have(self.user_id,'ship2')
            self.update(self.s2_price,2)

        elif self.selection==3 and self.coin_item_count>self.s3_price and not self.ship3_have:
            
            Var.char=3
            Var.char_lst=Var.char3_lst
            Database().update_char_have(self.user_id,'ship3')
            self.update(self.s3_price,3)

        elif self.selection==4 and self.coin_item_count>self.s4_price and not self.ship4_have:
            
            Var.char=4
            Var.char_lst=Var.char4_lst
            Database().update_char_have(self.user_id,'ship4')
            self.update(self.s4_price,4)

    def disp_ships(self):
       
        ship_offset=0
        text_offset=0.07
        coin_offset=0.07
        coin_text_offset=0.07
        ship_color=(120,120,230)
        ship_price_color=(0,255,0)
        buy_color=(120,120,120)
       
        self.ship1_image=transform.scale(self.ship1_image,(60,60))
        
        self.ship2_image=transform.scale(self.ship2_image,(60,60))
       
        self.ship3_image=transform.scale(self.ship3_image,(60,60))
        
        self.ship4_image=transform.scale(self.ship4_image,(60,60))

        self.ship_zips=zip([self.ship1_image,self.ship2_image,self.ship3_image,self.ship4_image],[self.ship1_rect,self.ship2_rect,self.ship3_rect,self.ship4_rect])
        for img,ship_rect in self.ship_zips:
            img.set_colorkey((0,0,0))
            (ship_rect.centerx,ship_rect.centery)=(self.width*(0.2+ship_offset),self.height*0.4)
            ship_offset+=0.18

            self.screen.blit(img,ship_rect)
        # show price
        ship_offset=0
        
        self.coin1_image,self.coin1_rect=load_image('coin.png')
        self.coin1_image=transform.scale(self.coin1_image,(30,30))
        self.coin2_image,self.coin2_rect=load_image('coin.png')
        self.coin2_image=transform.scale(self.coin1_image,(30,30))
        self.coin3_image,self.coin3_rect=load_image('coin.png')
        self.coin3_image=transform.scale(self.coin1_image,(30,30))
        self.coin4_image,self.coin4_rect=load_image('coin.png')
        self.coin4_image=transform.scale(self.coin1_image,(30,30))
        # coin img
        
        self.coin_img_zips=zip([self.coin1_image,self.coin2_image,self.coin3_image,self.coin4_image],[self.coin1_rect,self.coin2_rect,self.coin3_rect,self.coin4_rect])
       
        for img,coin_img_rect in self.coin_img_zips:
            img.set_colorkey((0,0,0))
            (coin_img_rect.centerx,coin_img_rect.centery)=(self.width*(0.18+ship_offset),self.height*(0.4+coin_offset))
            ship_offset+=0.18
            self.screen.blit(img,coin_img_rect)
        # coin price text
        ship_offset=0
        self.coin1_text=self.font.render(f'X{self.s1_price}',True,ship_price_color)
        self.coin2_text=self.font.render(f'X{self.s2_price}',True,ship_price_color)
        self.coin3_text=self.font.render(f'X{self.s3_price}',True,ship_price_color)
        self.coin4_text=self.font.render(f'X{self.s4_price}',True,ship_price_color)
        self.coin_text_list=[self.coin1_text,self.coin2_text,self.coin3_text,self.coin4_text]
        for x in self.coin_text_list:
            x_rect=x.get_rect(center=(self.width*(0.18+ship_offset+coin_text_offset),self.height*(0.4+coin_offset)))
            ship_offset+=0.18
            self.screen.blit(x,x_rect)

        self.ship1_text=self.font.render('Ship1',True,ship_color)
        self.ship1_pos=self.ship1_text.get_rect()
        
        self.ship2_text=self.font.render('Ship2',True,ship_color)
        self.ship2_pos=self.ship2_text.get_rect()

        self.ship3_text=self.font.render('Ship3',True,ship_color)
        self.ship3_pos=self.ship3_text.get_rect()
        self.ship4_text=self.font.render('Ship4',True,ship_color)
        self.ship4_pos=self.ship4_text.get_rect()

        self.buy_text=self.font.render('BUY',True,buy_color)
        ship_offset=0
        self.text_zips=zip([self.ship1_text,self.ship2_text,self.ship3_text,self.ship4_text],[self.ship1_pos,self.ship2_pos,self.ship3_pos,self.ship4_pos])
        for txt,pos in self.text_zips:
            (pos.centerx,pos.centery)=(self.width*(0.2+ship_offset),self.height*(0.4+coin_offset+text_offset))
            ship_offset+=0.18
            
            self.screen.blit(txt,pos)

        self.ship_dict={1:self.ship1_pos,2:self.ship2_pos,3:self.ship3_pos,4:self.ship4_pos}
        self.buy_pos=self.buy_text.get_rect(midbottom=self.ship_dict[self.selection].inflate(20,30).midbottom)
        self.screen.blit(self.buy_text,self.buy_pos)

    def char_store(self):
        #print('열기')
        super().open()
        main_menu, main_menuRect = load_image("main_menu.png")
        main_menu = pygame.transform.scale(main_menu, (500, 500))
        main_menuRect.midtop = self.screen.get_rect().midtop

        while self.active:
           
            self.clock.tick(self.clockTime)
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0)) 
            self.disp_ships()
          

            for event in pygame.event.get():
                if (event.type== pygame.QUIT or event.type==pygame.KEYDOWN
                and event.key==pygame.K_ESCAPE):
                    super().close()
                    pygame.quit()
                    sys.exit()
                elif  (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN and event.key==pygame.K_RETURN):
                    if self.active:
                        self.make_selection()
                        super().update_coin_text()
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT):
                    if self.active:
                        super().r_selection()

                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT):
                    if self.active:
                        super().l_selection()
                    
            self.disp_ships()
            super().update_coin_text()

            pygame.display.flip()

    # For char setting

    def disp_setting(self):
        ship_offset=0
        text_offset=0.07
       
        ship_color=(120,120,230)
       
        SET_color=(120,120,120)
        #갖고있으면 1
        self.ship1_have=Database().check_char_have(self.user_id,'ship1')
        self.ship2_have=Database().check_char_have(self.user_id,'ship2')
        self.ship3_have=Database().check_char_have(self.user_id,'ship3')
        self.ship4_have=Database().check_char_have(self.user_id,'ship4')

        self.ship1_image=transform.scale(self.ship1_image,(60,60))
        #self.ship1_image.set_colorkey((0,0,0,0))
      
        self.ship2_image=transform.scale(self.ship2_image,(60,60))
        #self.ship2_image.set_colorkey((0,0,0,0))
        
        self.ship3_image=transform.scale(self.ship3_image,(60,60))
        #self.ship3_image.set_colorkey((0,0,0,0))
       
        self.ship4_image=transform.scale(self.ship4_image,(60,60))
        #self.ship4_image.set_colorkey((0,0,0,0))

        #lock image
        self.lock1_image,self.lock1_rect=load_image('lock_icon.png')
        self.lock1_image.set_colorkey((255,255,255))
        self.lock1_image=transform.scale(self.lock1_image,(25,25)) 

        self.lock2_image,self.lock2_rect=load_image('lock_icon.png')
        self.lock2_image.set_colorkey((255,255,255))
        self.lock2_image=transform.scale(self.lock2_image,(25,25)) 
        
        self.lock3_image,self.lock3_rect=load_image('lock_icon.png')
        self.lock3_image.set_colorkey((255,255,255))
        self.lock3_image=transform.scale(self.lock3_image,(25,25)) 
        
        self.lock4_image,self.lock4_rect=load_image('lock_icon.png')
        self.lock4_image.set_colorkey((255,255,255))
        self.lock4_image=transform.scale(self.lock4_image,(25,25)) 

       

        
        
        self.ship_zips=zip([self.ship1_image,self.ship2_image,self.ship3_image,self.ship4_image],[self.ship1_rect,self.ship2_rect,self.ship3_rect,self.ship4_rect])
        for img,ship_rect in self.ship_zips:
            img.set_colorkey((0,0,0,0))
            (ship_rect.centerx,ship_rect.centery)=(self.width*(0.2+ship_offset),self.height*0.4)
            ship_offset+=0.18

            self.screen.blit(img,ship_rect)
        
        if self.ship1_have==0:
                self.ship1_image.convert_alpha()
                self.ship1_image.set_alpha(30)
                self.lock1_rect=self.ship1_rect.center
                self.screen.blit(self.lock1_image,self.lock1_rect)
        if self.ship2_have==0:
                self.ship2_image.convert_alpha()
                self.ship2_image.set_alpha(30) # 이미지 투명도
                self.lock2_rect=self.ship2_rect.center
                self.screen.blit(self.lock2_image,self.lock2_rect)
                    
        if self.ship3_have==0:
                self.ship3_image.convert_alpha()
                self.ship3_image.set_alpha(30)
                self.lock3_rect=self.ship3_rect.center
                self.screen.blit(self.lock3_image,self.lock3_rect)

        if self.ship4_have==0:
                self.ship4_image.convert_alpha()
                self.ship4_image.set_alpha(30)
                self.lock4_rect=self.ship4_rect.center
                self.screen.blit(self.lock4_image,self.lock4_rect)
        
        #Ship text
        
        self.ship1_text=self.font.render('Ship1',True,ship_color)
        self.ship1_pos=self.ship1_text.get_rect()
        
        self.ship2_text=self.font.render('Ship2',True,ship_color)
        self.ship2_pos=self.ship2_text.get_rect()

        self.ship3_text=self.font.render('Ship3',True,ship_color)
        self.ship3_pos=self.ship3_text.get_rect()
        self.ship4_text=self.font.render('Ship4',True,ship_color)
        self.ship4_pos=self.ship4_text.get_rect()

        self.SET_text=self.font.render('SET',True,SET_color)
        ship_offset=0
        self.text_zips=zip([self.ship1_text,self.ship2_text,self.ship3_text,self.ship4_text],[self.ship1_pos,self.ship2_pos,self.ship3_pos,self.ship4_pos])
        for txt,pos in self.text_zips:
            (pos.centerx,pos.centery)=(self.width*(0.2+ship_offset),self.height*(0.4+text_offset))
            ship_offset+=0.18
            
            self.screen.blit(txt,pos)

        self.ship_dict={1:self.ship1_pos,2:self.ship2_pos,3:self.ship3_pos,4:self.ship4_pos}
        self.SET_pos=self.SET_text.get_rect(midbottom=self.ship_dict[self.selection].inflate(20,30).midbottom)
        self.screen.blit(self.SET_text,self.SET_pos)

    def new_char_set(self):
        if self.selection==1 and self.ship1_have:
            Var.char=1
            Var.char_lst=Var.char1_lst
            Database().update_char_data(1,self.user_id)
        elif self.selection==2 and self.ship2_have:
            Var.char=2
            Var.char_lst=Var.char2_lst
            Database().update_char_data(2,self.user_id)
        elif self.selection==3 and self.ship3_have:
            Var.char=3
            Var.char_lst=Var.char3_lst
            Database().update_char_data(3,self.user_id)
        elif self.selection==4 and self.ship4_have:
            Var.char=4
            Var.char_lst=Var.char4_lst
            Database().update_char_data(4,self.user_id)
        


    def char_setting(self): # setting page
        # 없는건 어두운 이미지, 위에 코인이미지 코인값
       
        self.char_set=True
        main_menu, main_menuRect = load_image("main_menu.png")
        main_menu = pygame.transform.scale(main_menu, (500, 500))
        main_menuRect.midtop = self.screen.get_rect().midtop

        while self.char_set:
            self.clock.tick(self.clockTime)
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0)) 
            self.disp_setting()

            for event in pygame.event.get():
                if (event.type== pygame.QUIT or event.type==pygame.KEYDOWN
                and event.key==pygame.K_ESCAPE):
                    self.char_set=False
                    pygame.quit()
                    sys.exit()
                elif  (event.type == pygame.VIDEORESIZE):
                    self.screen_size = min(event.w, event.h)
                    if self.screen_size <= 300:
                        self.screen_size = 300
                    self.screen = pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.ratio = (self.screen_size / 500)
                    self.font = pygame.font.Font(None, round(36*self.ratio))
                elif (event.type == pygame.KEYDOWN and event.key==pygame.K_RETURN):
                    if self.char_set:
                        self.new_char_set()
                        
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT):
                    if self.char_set:
                        super().r_selection()

                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT):
                    if self.char_set:
                        super().l_selection()

            self.disp_setting()
            pygame.display.flip()

                


         

                
                    

        

        

        






       

        

            


"""
        
        
def store():

    selection=1
    global resized_screen # screen resize
    instore=True # store
    showstore=True

    # 배경이미지
    back_store,back_store_rect=load_image('main_menu.png')


    # 버튼 이미지
    char_btn_image,char_btn_rect=load_image('character.png',150,80)
    r_char_btn_image, r_char_btn_rect = load_image(*resize('character.png',150,80))

    skin_btn_image, skin_btn_rect = load_image('skin.png',150,80)
    r_skin_btn_image, r_skin_btn_rect = load_image(*resize('skin.png',150,80))

    back_btn_image, back_btn_rect = load_image('btn_back.png',100,50)
    r_back_btn_image, r_back_btn_rect = load_image(*resize('btn_back.png',100,50))

    storeopt={1:r_char_btn_rect,2:r_skin_btn_rect,3:r_back_btn_rect}

    while instore:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE and not full_screen: # full screen일 경우
                back_store_rect.bottomleft=(width * 0, height)
            if event.type==pygame.VIDEORESIZE:
                check_scr_size(event.w,event.h)
            if event.type==pygame.QUIT:
                instore=False
            if event.type==pygame.KEYDOWN:
                if event.type==pygame.K_ESCAPE:
                    return False

            if (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                if showstore: # true면
                    showstore=False
                if selection==1:
                    return 1,resized_screen
                    #char_store() # 캐릭터 상점
                elif selection==2:
                    return 2, resized_screen
                    #skin_store() # 배경이미지
                elif selection==3: # back
                    return BACK,resized_screen
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT
                    and selection>1 and not showstore ):
                    selection-=1
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT
                    and selection<len(storeopt) and not showstore ):
                    selection+=1

    # 크기 조정
        r_char_btn_rect.centerx = resized_screen.get_width() * 0.2
        r_char_btn_rect.centery = resized_screen.get_height() * 0.5

        r_skin_btn_rect.centerx = resized_screen.get_width() * (0.2 + width_offset)
        r_skin_btn_rect.centery = resized_screen.get_height() * 0.5

        r_back_btn_rect.centerx = resized_screen.get_width() * 0.1
        r_back_btn_rect.centery = resized_screen.get_height() * 0.1

        screen.blit(back_store,back_store_rect)

        disp_store_buttons(char_btn_image,skin_btn_image,back_btn_image)
        
        # buy pos
        
        storeopt={1:r_char_btn_rect,2:r_skin_btn_rect,3:r_back_btn_rect}

        selecttext=user_font.render('SELECT',True,Black)
        selecttext_rect=selecttext.get_rect(center=storeopt[selection].center)
        screen.blit(selecttext,selecttext_rect)

    
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()
        
        

def char_store():
    global resized_screen
    selection=1
    image_space=0.3
    instore=True
    showstore=True

    # 배경이미지
    back_store,back_store_rect=load_image('main_menu.png')

    # 캐릭터(우주선) 이미지
    ship1_image,ship1_rect=load_image('ship.png')
    ship1_image=transform.scale(ship1_image,(CHAR_SIZE, CHAR_SIZE))
    

    ship2_image,ship2_rect=load_image('ship2.png')
    ship2_image=transform.scale(ship2_image,(CHAR_SIZE, CHAR_SIZE))
  

    ship3_image,ship3_rect=load_image('ship3.png')
    ship3_image=transform.scale(ship3_image,(CHAR_SIZE, CHAR_SIZE))
    

    ship4_image,ship4_rect=load_image('ship4.png')
    ship4_image=transform.scale(ship4_image,(CHAR_SIZE, CHAR_SIZE))
    
    # coin
    coin_item_count=Database().load_coin(Var.user_id)
    user_coin_image,user_coin_rect=load_image('coin.png')
    user_coin_image=transform.scale(user_coin_image,(USER_ITEM_SIZE,USER_ITEM_SIZE))
    
    user_coin=user_font.render(f'X {coin_item_count}',True,Black)

    # 버튼pos
    shipopt={1:ship1_rect,2:ship2_rect,3:ship3_rect,4:ship4_rect}

    buytext=user_font.render('BUY',True,Black)
    buytext_rect=buytext.get_rect(center=shipopt[selection].center)
   # screen.blit(buytext,buytext_rect)
    #no money
    no_money_image, no_money_rect=load_image('X.png')

    # 뒤로가기
    back_btn_image,back_btn_rect=load_image('btn_back.png',100,50)
    r_back_btn_image,r_back_btn_rect=load_image(*resize('btn_back.png',100,50))

    # 가격 불러오기
    s1_price=Database().load_shipprice('ship1')
    s2_price=Database().load_shipprice('ship2')
    s3_price=Database().load_shipprice('ship3')
    s4_price=Database().load_shipprice('ship4')

    # 폰트
    ship1_price=user_font.render(f"x {s1_price}",True,Black)
    ship2_price=user_font.render(f"x {s2_price}",True,Black)
    ship3_price=user_font.render(f"x {s3_price}",True,Black)
    ship4_price=user_font.render(f"x {s4_price}",True,Black)

    # 배치
    (ship1_rect.centerx,ship1_rect.centery)=(width*0.2,height*0.37)
    ship1_price_rect=ship1_price.get_rect(center=(width*0.23,height*(0.37+item_price_offset)))
    #(no_money_rect.centerx,no_money_rect.centery)=(width*0.2,height*(0.37+item_price_offset))
    
    #
    (ship2_rect.centerx,ship2_rect.centery)=(width*0.2,height*0.37)
    ship2_price_rect=ship2_price.get_rect(center=(width*0.23,height*(0.37+item_price_offset)))
    #(no_money_rect.centerx,no_money_rect.centery)=(width*0.2,height*(0.37+item_price_offset))
    #
    (ship3_rect.centerx,ship3_rect.centery)=(width*0.2,height*0.37)
    ship3_price_rect=ship3_price.get_rect(center=(width*0.23,height*(0.37+item_price_offset)))
   # (no_money_rect.centerx,no_money_rect.centery)=(width*0.2,height*(0.37+item_price_offset))

    #
    (ship4_rect.centerx,ship4_rect.centery)=(width*0.2,height*0.37)
    ship4_price_rect=ship4_price.get_rect(center=(width*0.23,height*(0.37+item_price_offset)))
    #(no_money_rect.centerx,no_money_rect.centery)=(width*0.2,height*(0.37+item_price_offset))
   
    # back 
    r_back_btn_rect.centerx=resized_screen.get_width() * 0.1
    r_back_btn_rect.centery=resized_screen.get_height() * 0.1

    #coin 
    (user_coin_rect.centerx, user_coin_rect.centery) = (width * (0.65 + btn_offset), height * 0.08)
    user_c_rect = user_coin.get_rect(center=(width * (0.69 + btn_offset), height * 0.08))
    user_coin = user_font.render(f'X {coin_item_count}', True, Black)

    user_char=Database().load_char_data(Var.user_id)
    

    while instore:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE and not full_screen:
                back_store_rect.bottomleft = (width * 0, height)
            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)
            if event.type == pygame.QUIT:
                instore = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if (event.type == pygame.KEYDOWN
                    and event.key == pygame.K_RETURN):
                if showstore: # true면
                    showstore=False
                if selection==1 and coin_item_count >=s1_price and user_char!=1:
                    Database().update_char_data(1,Var.user_id)
                    Database().buy_char(Var.user_id,s1_price)

                elif selection==2 and coin_item_count>=s2_price and user_char!=2:
                    Database().update_char_data(2,Var.user_id)
                    Database().buy_char(Var.user_id,s2_price)

                elif selection==3 and coin_item_count>=s3_price and user_char!=3: # back
                    Database().update_char_data(3,Var.user_id)
                    Database().buy_char(Var.user_id,s3_price)

                elif selection==4 and coin_item_count>=s4_price and user_char!=4: # back
                    Database().update_char_data(4,Var.user_id)
                    Database().buy_char(Var.user_id,s4_price)

                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT
                    and selection>1 and not showstore ):
                    selection-=1
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT
                    and selection<len(shipopt) and not showstore ):
                    selection+=1
    
    #buy pos
        buytext=user_font.render('BUY',True,Black)
        buytext_rect=buytext.get_rect(center=shipopt[selection].center)
        coin_item_count=Database().load_coin(Var.user_id)
        user_coin=user_font.render(f'X {coin_item_count}',True,Black)

        screen.blit(back_store,back_store_rect)
        screen.blit(ship1_image,ship1_rect)
        screen.blit(ship2_image,ship2_rect)
        screen.blit(ship3_image,ship3_rect)
        screen.blit(ship4_image,ship4_rect)
        screen.blit(ship1_price,ship1_price_rect)
        screen.blit(ship2_price,ship2_price_rect)
        screen.blit(ship3_price,ship3_price_rect)
        screen.blit(ship4_image,ship4_price_rect)
    

    # back버튼 누르면 store page로 가게 
        screen.blit(back_btn_image,back_btn_rect)
        screen.blit(user_coin,user_c_rect)
        screen.blit(user_coin_image,user_coin_rect)
        resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_center)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()






def skin_store():
    global resized_screen
    instore=True
    selection=1

"""

