import os
import pygame
import pygame
import pygame_menu

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


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


def load_image(name, colorkey=None):
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
    return image, image.get_rect()

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


    
    char=1

    lst=char1_lst # char img 초기화 

    # 메뉴 전환을 위한 변수
    go_menu=False