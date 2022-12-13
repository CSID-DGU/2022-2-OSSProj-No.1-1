import pygame
import sys
from pygame import display
from pygame import Rect
from pygame import transform
from pygame import time
from pygame import Surface
from pygame.locals import RESIZABLE, RLEACCEL
from load import load_image,Var
from load import * #skin store
from menu import *
from database import Database






FPS=75
BACK=0


class Store(object):
    def __init__(self,screen_size):
        
        self.screen_size=screen_size
        self.screen=pygame.display.set_mode((self.screen_size, self.screen_size), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.ratio = (self.screen_size / 500)
        self.font = pygame.font.Font("LeeSeoyun.ttf", round(21*self.ratio))
        self.clock = pygame.time.Clock()
        self.clockTime = FPS
        self.main_menu, self.main_menuRect = load_image("shopback.png") 
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
        if self.selection>8:
            self.selection=1

    def l_selection(self):
        self.selection-=1
        if self.selection<1:
            self.selection=8

    
    def update_coin_text(self):
        coin_color=(255,0,0)
        self.coin_image,self.coin_rect=load_image('gold_coin.png')
        self.coin_image=transform.scale(self.coin_image,(COIN_HAVE_SIZE,COIN_HAVE_SIZE))
        self.coin_image.set_colorkey((0,0,0))
        
        self.coin_rect.topright=(self.width*0.89,self.height*0.03)

        
        self.coin_item_count=Database().load_coin(self.user_id)
        user_coin=self.font.render(f'X{self.coin_item_count}',True,coin_color)
        user_c_rect=user_coin.get_rect(topright=(self.width*(0.89+0.002),self.height*0.03))
        self.screen.blit(self.coin_image,self.coin_rect)
        self.screen.blit(user_coin,user_c_rect)

   
class CharStore(Store):
    def __init__(self,screen_size):
        super().__init__(screen_size)
        self.ship1_image,self.ship1_rect=load_image('ship.png')
        self.ship2_image,self.ship2_rect=load_image('ship2.png')
        self.ship3_image,self.ship3_rect=load_image('ship3.png')
        self.ship4_image,self.ship4_rect=load_image('ship4.png')
        self.ship5_image,self.ship5_rect=load_image('ship5.png')
        self.ship6_image,self.ship6_rect=load_image('ship6.png')
        self.ship7_image,self.ship7_rect=load_image('ship7.png')

        
        
        self.s1_price=Database().load_shipprice('ship1')
        self.s2_price=Database().load_shipprice('ship2')
        self.s3_price=Database().load_shipprice('ship3')
        self.s4_price=Database().load_shipprice('ship4')
        self.s5_price=Database().load_shipprice('ship5')
        self.s6_price=Database().load_shipprice('ship6')
        self.s7_price=Database().load_shipprice('ship7')
        self.char_set=False

        #갖고있으면1
        self.ship1_have=Database().check_char_have(self.user_id,'ship1')
        self.ship2_have=Database().check_char_have(self.user_id,'ship2')
        self.ship3_have=Database().check_char_have(self.user_id,'ship3')
        self.ship4_have=Database().check_char_have(self.user_id,'ship4')
        self.ship5_have=Database().check_char_have(self.user_id,'ship5')
        self.ship6_have=Database().check_char_have(self.user_id,'ship6')
        self.ship7_have=Database().check_char_have(self.user_id,'ship7')
        
        
    def update(self,price,char):
        # coin 업데이트
        Database().buy_char(self.user_id,price)
        # 캐릭터 업데이트
        Database().update_char_data(char,self.user_id)


            
    def make_selection(self):
       
        if self.selection==1 and self.coin_item_count > self.s1_price and not self.ship1_have:
            
            Var.char=1
            Var.lst=Var.char1_lst
            Database().update_char_have(self.user_id,'ship1') # 구매하면 1로 업데이트
            self.update(self.s1_price,1)

        elif self.selection==2 and self.coin_item_count > self.s2_price and not self.ship2_have:
            
            Var.char=2
            Var.lst=Var.char2_lst
            Database().update_char_have(self.user_id,'ship2')
            self.update(self.s2_price,2)

        elif self.selection==3 and self.coin_item_count>self.s3_price and not self.ship3_have:
            
            Var.char=3
            Var.lst=Var.char3_lst
            Database().update_char_have(self.user_id,'ship3')
            self.update(self.s3_price,3)

        elif self.selection==4 and self.coin_item_count>self.s4_price and not self.ship4_have:
            
            Var.char=4
            Var.lst=Var.char4_lst
            Database().update_char_have(self.user_id,'ship4')
            self.update(self.s4_price,4)
        elif self.selection==5 and self.coin_item_count>self.s5_price and not self.ship5_have:
            
            Var.char=5
            Var.lst=Var.char5_lst
            Database().update_char_have(self.user_id,'ship5')
            self.update(self.s5_price,5)

        elif self.selection==6 and self.coin_item_count>self.s6_price and not self.ship6_have:
            
            Var.char=6
            Var.lst=Var.char6_lst
            Database().update_char_have(self.user_id,'ship6')
            self.update(self.s6_price,6)

        elif self.selection==7 and self.coin_item_count>self.s7_price and not self.ship7_have:
            
            Var.char=7
            Var.lst=Var.char7_lst
            Database().update_char_have(self.user_id,'ship7')
            self.update(self.s7_price,7)

        elif self.selection==8:
            self.active=False



    def disp_ships(self): # 상점 디스플레이
       
        ship_offset=0
        text_offset=0.07
        coin_offset=0.07
        coin_text_offset=0.07
        #ship_color=(120,120,230)
        #ship_price_color=(0,255,0)
        #buy_color=(120,120,120)
        back_color=(0,0,0)
       
        self.ship1_image=transform.scale(self.ship1_image,(CHAR_SIZE,CHAR_SIZE))
        
        self.ship2_image=transform.scale(self.ship2_image,(CHAR_SIZE,CHAR_SIZE))
       
        self.ship3_image=transform.scale(self.ship3_image,(CHAR_SIZE,CHAR_SIZE))
        
        self.ship4_image=transform.scale(self.ship4_image,(CHAR_SIZE,CHAR_SIZE))
        

        self.ship_zips=zip([self.ship1_image,self.ship2_image,self.ship3_image,self.ship4_image],[self.ship1_rect,self.ship2_rect,self.ship3_rect,self.ship4_rect])
        for img,ship_rect in self.ship_zips:
            img.set_colorkey((0,0,0)) # 뒤에 검은 배경 지우기
            (ship_rect.centerx,ship_rect.centery)=(self.width*(0.18+ship_offset),self.height*0.3)
            ship_offset+=0.2

            self.screen.blit(img,ship_rect)
        #ship5,6,7
        ship_offset=0
        self.ship5_image=transform.scale(self.ship5_image,(CHAR_SIZE,CHAR_SIZE))
        
        self.ship6_image=transform.scale(self.ship6_image,(CHAR_SIZE,CHAR_SIZE))
        
        self.ship7_image=transform.scale(self.ship7_image,(CHAR_SIZE,CHAR_SIZE))
        
        #(self.ship5_rect.centerx,self.ship5_rect.centery)=(self.width*(0.65+ship_offset),self.height)
        #self.screen.blit(self.ship5_image,self.ship5_rect)
        self.ship_zips2=zip([self.ship5_image,self.ship6_image,self.ship7_image],[self.ship5_rect,self.ship6_rect,self.ship7_rect])
        for img,ship_rect in self.ship_zips2:
            img.set_colorkey((0,0,0))
            (ship_rect.centerx,ship_rect.centery)=(self.width*(0.22+ship_offset),self.height*0.6)
            ship_offset+=0.22

            self.screen.blit(img,ship_rect)

        # show price
        ship_offset=0
        
        self.coin1_image,self.coin1_rect=load_image('coin.png')
        self.coin1_image=transform.scale(self.coin1_image,(COIN_SIZE,COIN_SIZE))
        self.coin2_image,self.coin2_rect=load_image('coin.png')
        self.coin2_image=transform.scale(self.coin2_image,(COIN_SIZE,COIN_SIZE))
        self.coin3_image,self.coin3_rect=load_image('coin.png')
        self.coin3_image=transform.scale(self.coin3_image,(COIN_SIZE,COIN_SIZE))
        self.coin4_image,self.coin4_rect=load_image('coin.png')
        self.coin4_image=transform.scale(self.coin4_image,(COIN_SIZE,COIN_SIZE))
        # coin img
        
        self.coin_img_zips=zip([self.coin1_image,self.coin2_image,self.coin3_image,self.coin4_image],[self.coin1_rect,self.coin2_rect,self.coin3_rect,self.coin4_rect])
       
        for img,coin_img_rect in self.coin_img_zips:
            img.set_colorkey((0,0,0))
            (coin_img_rect.centerx,coin_img_rect.centery)=(self.width*(0.16+ship_offset),self.height*(0.3+coin_offset))
            ship_offset+=0.2
            self.screen.blit(img,coin_img_rect)

        # show 5,6,7 price
        ship_offset=0
        self.coin5_image,self.coin5_rect=load_image('coin.png')
        self.coin5_image=transform.scale(self.coin5_image,(COIN_SIZE,COIN_SIZE))
        self.coin6_image,self.coin6_rect=load_image('coin.png')
        self.coin6_image=transform.scale(self.coin6_image,(COIN_SIZE,COIN_SIZE))
        self.coin7_image,self.coin7_rect=load_image('coin.png')
        self.coin7_image=transform.scale(self.coin7_image,(COIN_SIZE,COIN_SIZE))

        self.coin_img_zips2=zip([self.coin5_image,self.coin6_image,self.coin7_image],[self.coin5_rect,self.coin6_rect,self.coin7_rect])
        for img,coin_img_rect in self.coin_img_zips2:
            img.set_colorkey((0,0,0))
            (coin_img_rect.centerx,coin_img_rect.centery)=(self.width*(0.2+ship_offset),self.height*(0.6+coin_offset))
            ship_offset+=0.22
            self.screen.blit(img,coin_img_rect)


        # coin price text
        ship_offset=0
        self.coin1_text=self.font.render(f'X{self.s1_price}',True,ship_price_color)
        self.coin2_text=self.font.render(f'X{self.s2_price}',True,ship_price_color)
        self.coin3_text=self.font.render(f'X{self.s3_price}',True,ship_price_color)
        self.coin4_text=self.font.render(f'X{self.s4_price}',True,ship_price_color)
        self.coin_text_list=[self.coin1_text,self.coin2_text,self.coin3_text,self.coin4_text]
        for x in self.coin_text_list:
            x_rect=x.get_rect(center=(self.width*(0.16+ship_offset+coin_text_offset),self.height*(0.3+coin_offset)))
            ship_offset+=0.2
            self.screen.blit(x,x_rect)
        # coin price text 5,6,7
        ship_offset=0
        self.coin5_text=self.font.render(f'X{self.s5_price}',True,ship_price_color)
        self.coin6_text=self.font.render(f'X{self.s6_price}',True,ship_price_color)
        self.coin7_text=self.font.render(f'X{self.s7_price}',True,ship_price_color)
        self.coin_text_list2=[self.coin5_text,self.coin6_text,self.coin7_text]
        
        for x in self.coin_text_list2:
            x_rect=x.get_rect(center=(self.width*(0.2+ship_offset+coin_text_offset),self.height*(0.6+coin_offset)))
            ship_offset+=0.22
            self.screen.blit(x,x_rect)

        #ship1,2,3,4 text
        self.ship1_text=self.font.render('Ship1',True,ship_color)
        self.ship1_pos=self.ship1_text.get_rect()
        
        self.ship2_text=self.font.render('Ship2',True,ship_color)
        self.ship2_pos=self.ship2_text.get_rect()

        self.ship3_text=self.font.render('Ship3',True,ship_color)
        self.ship3_pos=self.ship3_text.get_rect()
        self.ship4_text=self.font.render('Ship4',True,ship_color)
        self.ship4_pos=self.ship4_text.get_rect()

        
        ship_offset=0
        self.text_zips=zip([self.ship1_text,self.ship2_text,self.ship3_text,self.ship4_text],[self.ship1_pos,self.ship2_pos,self.ship3_pos,self.ship4_pos])
        for txt,pos in self.text_zips:
            (pos.centerx,pos.centery)=(self.width*(0.2+ship_offset),self.height*(0.3+coin_offset+text_offset))
            ship_offset+=0.2
            
            self.screen.blit(txt,pos)

        # ship 5,6,7 text
        ship_offset=0
        self.ship5_text=self.font.render('Ship5',True,ship_color)
        self.ship5_pos=self.ship5_text.get_rect()
        self.ship6_text=self.font.render('Ship6',True,ship_color)
        self.ship6_pos=self.ship6_text.get_rect()
        self.ship7_text=self.font.render('Ship7',True,ship_color)
        self.ship7_pos=self.ship7_text.get_rect()
        self.back_text=self.font.render('BACK',True,back_color)
        self.back_pos=self.back_text.get_rect()
        self.text_zips2=zip([self.ship5_text,self.ship6_text,self.ship7_text,self.back_text],[self.ship5_pos,self.ship6_pos,self.ship7_pos,self.back_pos])

        for txt,pos in self.text_zips2:
            (pos.centerx,pos.centery)=(self.width*(0.24+ship_offset),self.height*(0.6+coin_offset+text_offset))
            ship_offset+=0.22
            
            self.screen.blit(txt,pos)


        self.ship_dict={1:self.ship1_pos,2:self.ship2_pos,3:self.ship3_pos,4:self.ship4_pos,5:self.ship5_pos,6:self.ship6_pos,7:self.ship7_pos,8:self.back_pos}
        self.buy_text=self.font.render('BUY',True,buy_color)
        self.buy_pos=self.buy_text.get_rect(midbottom=self.ship_dict[self.selection].inflate(20,30).midbottom)
        self.screen.blit(self.buy_text,self.buy_pos)

    def char_store(self):
        #print('열기')
        super().open()
        main_menu, main_menuRect = load_image("shopback.png")
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
                        if self.active:
                            super().update_coin_text()
                            return True
                        else:
                            return BACK
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT):
                    if self.active:
                        super().r_selection()

                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT):
                    if self.active:
                        super().l_selection()
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_UP):
                    self.selection=1
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_DOWN):
                    self.selection=5
                    
            self.disp_ships()
            super().update_coin_text()

            pygame.display.flip()

    # For char setting

    def disp_setting(self):
        ship_offset=0
        text_offset=0.07
       
        ship_color=(120,120,230)
        back_color=(0,0,0)
        SET_color=(120,120,120)
        
        #갖고있으면 1
        self.ship1_have=Database().check_char_have(self.user_id,'ship1')
        self.ship2_have=Database().check_char_have(self.user_id,'ship2')
        self.ship3_have=Database().check_char_have(self.user_id,'ship3')
        self.ship4_have=Database().check_char_have(self.user_id,'ship4')
        self.ship5_have=Database().check_char_have(self.user_id,'ship5')
        self.ship6_have=Database().check_char_have(self.user_id,'ship6')
        self.ship7_have=Database().check_char_have(self.user_id,'ship7')

        # ship image
        self.ship1_image=transform.scale(self.ship1_image,(CHAR_SIZE,CHAR_SIZE))
        self.ship2_image=transform.scale(self.ship2_image,(CHAR_SIZE,CHAR_SIZE))
        self.ship3_image=transform.scale(self.ship3_image,(CHAR_SIZE,CHAR_SIZE))
        self.ship4_image=transform.scale(self.ship4_image,(CHAR_SIZE,CHAR_SIZE))
        self.ship5_image=transform.scale(self.ship5_image,(CHAR_SIZE,CHAR_SIZE))
        self.ship6_image=transform.scale(self.ship6_image,(CHAR_SIZE,CHAR_SIZE))
        self.ship7_image=transform.scale(self.ship7_image,(CHAR_SIZE,CHAR_SIZE))
        

        #lock image
        self.lock1_image,self.lock1_rect=load_image('lock_icon.png')
        self.lock1_image.set_colorkey((255,255,255)) # 흰색 배경 제거
        self.lock1_image=transform.scale(self.lock1_image,(LOCK_SIZE,LOCK_SIZE)) 

        

        #ship 1,2,3,4 display
        self.ship_zips=zip([self.ship1_image,self.ship2_image,self.ship3_image,self.ship4_image],[self.ship1_rect,self.ship2_rect,self.ship3_rect,self.ship4_rect],
        [self.ship1_have,self.ship2_have,self.ship3_have,self.ship4_have])
        for img,ship_rect,ship_have in self.ship_zips:
            img.set_colorkey((0,0,0,0)) # 검은색 배경 제거
           
            (ship_rect.centerx,ship_rect.centery)=(self.width*(0.18+ship_offset),self.height*0.3)
            if ship_have==0:
                img.convert_alpha()
                img.set_alpha(30)
                self.lock1_rect=ship_rect.topleft
                self.screen.blit(img,ship_rect)
                self.screen.blit(self.lock1_image,self.lock1_rect)
           
            ship_offset+=0.2
            self.screen.blit(img,ship_rect)
        
        #ship 5,6,7 display
        ship_offset=0
        self.ship_zips2=zip([self.ship5_image,self.ship6_image,self.ship7_image],[self.ship5_rect,self.ship6_rect,self.ship7_rect],
        [self.ship5_have,self.ship6_have,self.ship7_have])
        for img,ship_rect,ship_have in self.ship_zips2:
            img.set_colorkey((0,0,0,0)) # 뒤에 검은색 배경 제거
            cnt=5
            (ship_rect.centerx,ship_rect.centery)=(self.width*(0.22+ship_offset),self.height*0.55)
            if ship_have==0:
                img.convert_alpha()
                img.set_alpha(30)
                self.lock1_rect=ship_rect.topleft
                self.screen.blit(img,ship_rect)
                self.screen.blit(self.lock1_image,self.lock1_rect)
           
            ship_offset+=0.22
            self.screen.blit(img,ship_rect)
       
        #Ship text
        
        self.ship1_text=self.font.render('Ship1',True,ship_color)
        self.ship1_pos=self.ship1_text.get_rect()
        
        self.ship2_text=self.font.render('Ship2',True,ship_color)
        self.ship2_pos=self.ship2_text.get_rect()

        self.ship3_text=self.font.render('Ship3',True,ship_color)
        self.ship3_pos=self.ship3_text.get_rect()
        self.ship4_text=self.font.render('Ship4',True,ship_color)
        self.ship4_pos=self.ship4_text.get_rect()

        
        ship_offset=0
        self.text_zips=zip([self.ship1_text,self.ship2_text,self.ship3_text,self.ship4_text],[self.ship1_pos,self.ship2_pos,self.ship3_pos,self.ship4_pos])
        for txt,pos in self.text_zips:
            (pos.centerx,pos.centery)=(self.width*(0.2+ship_offset),self.height*(0.3+text_offset))
            ship_offset+=0.2
            
            self.screen.blit(txt,pos)

        # ship 5,6,7 text
        ship_offset=0
        self.ship5_text=self.font.render('Ship5',True,ship_color)
        self.ship5_pos=self.ship5_text.get_rect()
        self.ship6_text=self.font.render('Ship6',True,ship_color)
        self.ship6_pos=self.ship6_text.get_rect()
        self.ship7_text=self.font.render('Ship7',True,ship_color)
        self.ship7_pos=self.ship7_text.get_rect()
        self.back_text=self.font.render('BACK',True,back_color)
        self.back_pos=self.back_text.get_rect()
        self.text_zips2=zip([self.ship5_text,self.ship6_text,self.ship7_text,self.back_text],[self.ship5_pos,self.ship6_pos,self.ship7_pos,self.back_pos])

        for txt,pos in self.text_zips2:
            (pos.centerx,pos.centery)=(self.width*(0.24+ship_offset),self.height*(0.55+text_offset))
            ship_offset+=0.22
            
            self.screen.blit(txt,pos)

        self.SET_text=self.font.render('SET',True,SET_color)
        self.ship_dict={1:self.ship1_pos,2:self.ship2_pos,3:self.ship3_pos,4:self.ship4_pos,5:self.ship5_pos,6:self.ship6_pos,7:self.ship7_pos,8:self.back_pos}
        self.SET_pos=self.SET_text.get_rect(midbottom=self.ship_dict[self.selection].inflate(20,30).midbottom)
        self.screen.blit(self.SET_text,self.SET_pos)

    # 유저 선택에 따라 캐릭터 세팅, db업데이트
    def new_char_set(self):
        if self.selection==1 and self.ship1_have:
            Var.char=1
            Var.lst=Var.char1_lst
            Database().update_char_data(1,self.user_id) # db업데이트 : 유저의 현재 캐릭터
        elif self.selection==2 and self.ship2_have:
            Var.char=2
            Var.lst=Var.char2_lst
            Database().update_char_data(2,self.user_id)
        elif self.selection==3 and self.ship3_have:
            Var.char=3
            Var.lst=Var.char3_lst
            Database().update_char_data(3,self.user_id)
        elif self.selection==4 and self.ship4_have:
            Var.char=4
            Var.lst=Var.char4_lst
            Database().update_char_data(4,self.user_id)

        elif self.selection==5 and self.ship5_have:
            Var.char=5
            Var.lst=Var.char5_lst
            Database().update_char_data(5,self.user_id)
        
        elif self.selection==6 and self.ship6_have:
            Var.char=6
            Var.lst=Var.char6_lst
            Database().update_char_data(6,self.user_id)
        
        elif self.selection==7 and self.ship7_have:
            Var.char=7
            Var.lst=Var.char7_lst
            Database().update_char_data(7,self.user_id)

        elif self.selection ==8:
            self.char_set=False
        
        
        


    def char_setting(self): # setting page
        # 없는건 어두운 이미지, 위에 코인이미지 코인값
       
        self.char_set=True
        main_menu, main_menuRect = load_image("shopback.png")
        main_menu = pygame.transform.scale(main_menu, (500, 500))
        main_menuRect.midtop = self.screen.get_rect().midtop
        self.disp_setting()
        while self.char_set:
            self.clock.tick(self.clockTime)#delay문제
            main_menu_size = (round(main_menu.get_width() * self.ratio), round(main_menu.get_height() * self.ratio))
            self.screen.blit(pygame.transform.scale(main_menu, main_menu_size), (0,0)) 
            #self.disp_setting()

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
                  
                    self.new_char_set()
                        
                    if self.char_set:
                        self.disp_setting()
                        return True
                    else:
                        return BACK

                        
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT):
                    if self.char_set:
                        super().r_selection()

                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT):
                    if self.char_set:
                        super().l_selection()
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_UP):
                    self.selection=1
                elif (event.type==pygame.KEYDOWN and event.key==pygame.K_DOWN):
                    self.selection=5

            self.disp_setting()
            pygame.display.flip()


    
                


         

                
                    

        

        

        






       

        

            