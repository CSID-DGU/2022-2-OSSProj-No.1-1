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
    menu_display_w=600
    menu_display_h=600
    BLACK=(0,0,0)

    mytheme=pygame_menu.themes.THEME_ORANGE.copy()                  # 메뉴 기본 테마 설정
    mytheme.widget_font_color=BLACK
    # 다 필요없고 mytheme.widget_margin이랑 widget_margin_rank 가져오기
    widget_rate_rank = 60 

    menu_image = pygame_menu.baseimage.BaseImage(
        image_path='data/menu.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL	)
    # 메뉴 위젯 폰트 컬러
    mytheme.background_color = menu_image                           # 메뉴 배경 설정
    mytheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE  # 메뉴 타이틀 바 모양 설정
    mytheme.widget_alignment=pygame_menu.locals.ALIGN_CENTER        # 메뉴 가운데 정렬 설정
    mytheme.widget_font =pygame_menu.font.FONT_NEVIS                # 메뉴 폰트 설정
    mytheme.widget_margin=(0,40)

    widget_margin_rank=(0,int((menu_display_h)/widget_rate_rank))           # 랭크 보기 화면

    #HELP 메뉴 만들
    #mytheme_help = pygame_menu.themes.THEME_ORANGE.copy()  # 메뉴 기본 테마 설정
    #mytheme_help.background_color = widget_image2  # 메뉴 배경 설정
    #mytheme_help.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE  # 메뉴 타이틀 바 모양 설정
    # ship 이미지 여따 저장하기
    path='data/'


    char1_lst=[path+'ship.png']
    char2_lst=[path+'ship2.png']
    char3_lst=[path+'ship3.png']

    # font_sub , char 관련 변수 추기
    font_rate_sub = 20           #서브 폰트들 리사이징 비율
    font_sub = int((menu_display_h) / font_rate_sub)     # 메뉴 서브 폰트 사이즈
    char=1

    lst=char1_lst

    # 메뉴 전환을 위한 변수
    go_menu=False