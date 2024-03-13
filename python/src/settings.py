import pygame as pg
import math
import time

def make_rect(group, path, l, t, w, h,scale=False, nW=0, nH=0):
    temp = pg.sprite.Sprite(group)
    temp.image = pg.image.load(path).convert_alpha()
    temp.rect = pg.Rect(l, t, w, h)
    if scale == True:
        temp.image = pg.transform.scale(temp.image, [nW, nH])

    return temp

pg.init()
pg.mixer.init()

# Colors
BLACK = (0, 0, 0)
BLUE = (40, 30, 70)
LIGHT_BLUE = (30,189,255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Game Settings
FPS = 60
TITLE = "Snowboard"
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
HALF_SCREEN_HEIGHT = int(SCREEN_HEIGHT/2)
HALF_SCREEN_WIDTH = int(SCREEN_WIDTH/2)
VELOCITY = 7
MAX_CLOUDS = 10
screen = pg.display.set_mode(DIMENSIONS)

# Sound
bonk_snd = pg.mixer.Sound('snd\\bonk.ogg')
click_snd = pg.mixer.Sound('snd\\btn_click.ogg')
score_snd = pg.mixer.Sound('snd\\scoreSound.ogg')
count_start = pg.mixer.Sound('snd\\count_start.ogg')
count_end = pg.mixer.Sound('snd\\count_end.ogg')
helper_sound = pg.mixer.Sound('snd\\blink.ogg')


# Variables
texture_position = 0  #this is used to draw the road
# those variables are used to increment texture_position
ddz = 0.001
dz = 0
z = 0
road_pos = 0  #this is to remember our position on the road
road_acceleration = 50 #this is the speed at witch we traverse the road
texture_position_acceleration = 4  #this determine how much the strips will stretch forward
texture_position_threshold = SCREEN_HEIGHT/2  #this determine how much the road will be divided into strips
half_texture_position_threshold = int(texture_position_threshold/2) #this is used to know what road to draw from (light or dark road)

# Hud
heart_pos = [(30, 60), (110, 60), (190, 60)]
life = pg.image.load('img\\vida.png')
scoreboard = pg.image.load('img\\placar.png')

fontesc = pg.font.SysFont('sans',(int(SCREEN_WIDTH/70)))
font = pg.font.SysFont('sans',(int(SCREEN_WIDTH/25)))
score = 0
scoreArr = [str(score)]
startTime = 0
elapsedTime = 0
errorCounter = 0 # store the number of error of the player || the variable is inside player.py
# A error is when the player move to the wrong direction when a obstacle is coming,
# The player *doesn't* need to be hit to count as an error, just move to the wrong direction at the wrong time


# Draw Groups

## Menu
mm_draw_group = pg.sprite.Group()
mm_start = pg.sprite.Group()
mm_training = pg.sprite.Group()
mm_quit = pg.sprite.Group()

## Game Over
go_draw_group = pg.sprite.Group()
go_quit = pg.sprite.Group()
go_retry = pg.sprite.Group()

## Training over
tr_yes = pg.sprite.Group()
tr_no = pg.sprite.Group()

## Save
score_txt_draw_group = pg.sprite.Group()
score_draw_group = pg.sprite.Group()
s_save = pg.sprite.Group()

buttonW = 300
buttonH = 75
saveX = (SCREEN_WIDTH / 2) - (buttonW / 2) 
saveY = (SCREEN_HEIGHT) - (SCREEN_HEIGHT*0.1 + buttonH)

# Images

# * Menu *

# mm_draw_group
start_btn1 = make_rect(mm_draw_group, "img\\start1.png", 60, 200, buttonW, buttonH, True, buttonW, buttonH)
start_btn2 = make_rect(mm_start, "img\\start2.png", 60, 200, buttonW, buttonH, True, buttonW, buttonH)
start_btn3 = pg.image.load("img\\start3.png")
start_btn3 = pg.transform.scale(start_btn3, [300, 75])

training_btn1 = make_rect(mm_draw_group, "img\\treino1.png", 60, 285, buttonW, buttonH, True, buttonW, buttonH)
training_btn2 = make_rect(mm_training, "img\\treino2.png", 60, 285, buttonW, buttonH, True, buttonW, buttonH)
training_btn3 = pg.image.load("img\\treino3.png")
training_btn3 = pg.transform.scale(training_btn3, [300, 75])

exit_btn1 = make_rect(mm_draw_group, "img\\exit1.png", 60, 370, buttonW, buttonH, True, buttonW, buttonH)
exit_btn2 = make_rect(mm_quit, "img\\exit2.png", 60, 370, buttonW, buttonH, True, buttonW, buttonH)
exit_btn3 = pg.image.load("img\\exit3.png")
exit_btn3 = pg.transform.scale(exit_btn3, [300, 75])

tittle = make_rect(mm_draw_group, "img\\tittle.png", 400, 112, 256, 76, True, 768, 228)


# Score
nums = [pg.image.load('img\\num_0.png'), pg.image.load('img\\num_1.png'), pg.image.load('img\\num_2.png'), pg.image.load('img\\num_3.png'), pg.image.load('img\\num_4.png'), pg.image.load('img\\num_5.png'), pg.image.load('img\\num_6.png'), pg.image.load('img\\num_7.png'), pg.image.load('img\\num_8.png'), pg.image.load('img\\num_9.png')]
numsCount = []

countW = 90
countH = 150
for i in range(4):
    numsCount.append(pg.transform.scale(nums[i], [countW, countH]))

for i in range(len(nums)):
    nums[i] = pg.transform.scale(nums[i], [30, 50])
score_text = make_rect(score_txt_draw_group, "img\\pontuacao.png", 786, 20, 256, 76, True, 256, 76)

# def first_digit(num):
    
#     return make_rect(score_txt_draw_group, nums[num], 1051, 46, 50, 76, True, 50, 76)
    

## save
save_btn1 = make_rect(score_draw_group, "img\\save1.png", saveX, saveY, buttonW, buttonH, True, buttonW, buttonH)
save_btn2 = make_rect(s_save, "img\\save2.png", saveX, saveY, buttonW, buttonH, True, buttonW, buttonH)
save_btn3 = pg.image.load("img\\save3.png")
save_btn3 = pg.transform.scale(save_btn3, [300, 75])


## go_draw_group
retry_btn1 = make_rect(go_draw_group, "img\\restart1.png", 113, 456, buttonW, buttonH, True, buttonW, buttonH)
retry_btn2 = make_rect(go_retry, "img\\restart2.png", 113, 456, buttonW, buttonH, True, buttonW, buttonH)
retry_btn3 = pg.image.load("img\\restart3.png")
retry_btn3 = pg.transform.scale(retry_btn3, [300, 75])

go_exit_btn1 = make_rect(go_draw_group, "img\\exit1.png", 787, 456, buttonW, buttonH, True, buttonW, buttonH)
go_exit_btn2 = make_rect(go_quit, "img\\exit2.png", 787, 456, buttonW, buttonH, True, buttonW, buttonH)
go_exit_btn3 = pg.image.load("img\\exit3.png")
go_exit_btn3 = pg.transform.scale(go_exit_btn3, [300, 75])


fundo = pg.image.load("img\\snow_bg.jpg")
fundo = pg.transform.scale(fundo, DIMENSIONS)
blurBG = pg.image.load("img\\snow_bg_blur.jpg")
blurBG = pg.transform.scale(blurBG, DIMENSIONS)



# init1 = pg.image.load("img\\init1.png")
# init2 = pg.image.load("img\\init2.png")
# grav1 = pg.image.load("img\\grav1.png")
# grav2 = pg.image.load("img\\grav2.png")
# sair1 = pg.image.load("img\\sair1.png")
# sair2 = pg.image.load("img\\sair2.png")
# final180, 260
# final1 = pg.transform.scale(final1, DIMENSIONS)
# final2 = pg.image.load("img\\final2.png")
# final2 = pg.transform.scale(final2, DIMENSIONS)
# final3 = pg.image.load("img\\final3.png")
# final3 = pg.transform.scale(final3, DIMENSIONS)

light_road = pg.image.load('img\\light_snow.png').convert()
dark_road = pg.image.load('img\\dark_snow.png').convert()
bg_img = pg.image.load('img\\sky.png').convert()
snowman = pg.image.load('img\\boneco_de_neve.png')
snow_tree = pg.image.load('img\\snow_tree.png')
trunk = pg.image.load('img\\trunk.png')
right_arrow = pg.image.load('img\\arrow.png')
helperW = 150
helperH = 150
right_arrow = pg.transform.scale(right_arrow, (helperW, helperH))
left_arrow = pg.image.load('img\\arrow.png')
left_arrow = pg.transform.flip(left_arrow, True, False)
left_arrow = pg.transform.scale(left_arrow, (helperW, helperH))
# rock = pg.image.load('img\\rock.png')
# rock = pg.transform.scale(rock, (100, 34))

light_road = pg.transform.scale(light_road, (SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
dark_road = pg.transform.scale(dark_road, (SCREEN_WIDTH, HALF_SCREEN_HEIGHT)) 
bg_img = pg.transform.scale(bg_img, (SCREEN_WIDTH, HALF_SCREEN_HEIGHT))


# Player Images
P_X = int((SCREEN_WIDTH/16) * 2.5)
P_Y = int((SCREEN_HEIGHT/9) * 2.5)
P_IDLE = pg.image.load('img\\p_idle.png')
P_IDLE = pg.transform.scale(P_IDLE, (P_X, P_Y))
P_IMAGE = pg.image.load('img\\p_left.png')
P_IMAGE = pg.transform.scale(P_IMAGE, (P_X, P_Y))
P_IMAGE = (P_IMAGE, pg.transform.flip(P_IMAGE, True, False), P_IDLE)

# Cloud Images
clouds = [pg.image.load('img\\cloud1.png'), pg.image.load('img\\cloud2.png'), pg.image.load('img\\cloud3.png'), pg.image.load('img\\cloud4.png')]
for i in range(4):
    clouds[i] = pg.transform.scale(clouds[i], (int(P_X/2), int(P_Y/2)))

# Obstacle direction    
obstacleDir = None
obstaclesElapsed = 0
obs_left = int(HALF_SCREEN_WIDTH-1)
obs_right = int(HALF_SCREEN_WIDTH+1)




