import os
import pygame
import pygame
from pygame import display

from pygame import transform
from pygame import Rect
from pygame import Surface

from pygame.locals import RESIZABLE, RLEACCEL



main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#store.py
scr_size=(width,height)=(600,600) # default
resized_screen = display.set_mode((scr_size), RESIZABLE)
screen=resized_screen.copy()
width_offset=0.3
item_price_offset = 0.18
resized_screen_center = (0, 0)
btn_offset=0.25
CHAR_SIZE=58
COIN_SIZE=30
COIN_HAVE_SIZE=38
LOCK_SIZE=27
white = (255, 255, 255)
USER_ITEM_SIZE=20

ship_color=(120,120,230)
ship_price_color=(0,255,0)
buy_color=(120,120,120)






def check_scr_size(eventw, eventh): # resized screen
    if (eventw < width and eventh < height) or (eventw < width) or (eventh < height):
        # 최소해상도
        resized_screen = display.set_mode((scr_size), RESIZABLE)
    else:
        if (eventw / eventh) != (width / height):
            # 고정화면비
            adjusted_height = int(eventw / (width / height))
            resized_screen = display.set_mode((eventw, adjusted_height), RESIZABLE)





def resize(name, w, h):
    global width, height, resized_screen
    print("resized_screen: (", resized_screen.get_width(),
          ",", resized_screen.get_height(), ")")
    return (name, w * resized_screen.get_width() // width,
            h * resized_screen.get_height() // height)

def load_music(name):
    pygame.init()
    pygame.mixer.music.load(os.path.join(data_dir, name))


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound: %s' % fullname)
        raise SystemExit(str(pygame.get_error()))
    return sound


def load_image(name,sizex=-1,sizey=-1, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(pygame.get_error()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    if sizex!=-1 or sizey!=-1:
        image=transform.scale(image,(sizex,sizey))
    return image, image.get_rect()


# for skin store
field1, field1Rect = load_image("field.png") # skin
field2, field2Rect = load_image("field.png") #skin

class Var:
    user_id=''
    initial_id=0
    ## mode_single.py에서 게임이 종료되었음을 어떻게 알릴것인지
    # 게임이 종료됐을 때 무조건 setScore 함수가 호출되게 해야함
    # pygame.event로 알릴것인가? or game_over() 함수를 사용..? 
    # tongsan 에서 game_over() 함수는 board. py에저장 어떻게 작성했는지 확인

     #메뉴 기본 테마 만들기
   
    path='data/'

    char1_lst=['ship.png']
    char2_lst=['ship2.png']
    char3_lst=['ship3.png']
    char4_lst=['ship4.png']
    char5_lst=['ship5.png']
    char6_lst=['ship6.png']
    char7_lst=['ship7.png']
    
    

    char=1
    lst=char1_lst # char img 초기화 
    # 메뉴 전환을 위한 변수
    go_menu=False
    # 상점기능
    #char1_price=50
    #char2_price=70
    #char3_price=100
    #char4_price=200
    # for char_setting
    char_have=[]

    coin=0
