import pygame as pg
import settings as s
import random
from game import *

class Obstacle(pg.sprite.Sprite):
    '''
    Modes:
    * 1 - Tutorial mode / Controlled mode
    * 2 - Random mode
    '''
    def __init__(self, mode=1, side=s.obs_left):
        super(Obstacle, self).__init__()
        self.score = 0
        self.speed = s.obsSpeed
        self.mov = s.obsMov
        self.i = 0
        s.obstaclesElapsed += 1

        print(f"score {s.score} | obsToSpeedUp {s.obsToSpeedUp}")

        # if (s.score) == s.obsToSpeedUp and s.obstaclesElapsed >= s.obsToSpeedUp:
        #     s.obsToSpeedUp += s.obsCount
        #     s.obsSpeed += s.obsSpeedUpValue
        #     s.obsMov += s.obsSpeedUpValue
        #     s.obsScale += 0.001
        #     s.OBSTIME -= s.obsSpeedUpTime




        print(f"Obstacle speed: {self.speed}")

        # Randomize obstacle direction (left, middle, right)
        # self.x = random.choice([int(s.HALF_SCREEN_WIDTH-10), s.HALF_SCREEN_WIDTH, int(s.HALF_SCREEN_WIDTH+1)])
        if mode == 1:
            self.x = side
            s.obsIndex += 1
            if s.obsIndex >= s.obsMaxIndex:
                s.obsIndex = 0

        elif mode == 2:
            self.x = s.obsArr[s.obsIndex]
            s.obsIndex += 1
            if s.obsIndex >= s.obsMaxIndex:
                s.obsIndex = 0
        
        
        self.y = s.HALF_SCREEN_HEIGHT
        if self.x < s.HALF_SCREEN_WIDTH:
            s.obstacleDir = "LEFT"
            self.obj = "trunk"
            self.surf = s.trunk
            self.mov_x = -self.mov
            # print("< half") 
        elif self.x > s.HALF_SCREEN_WIDTH:
            s.obstacleDir = "RIGHT"
            self.obj = "trunk"
            self.surf = s.trunk
            self.mov_x = self.mov
            # print("> half")

        print(f"*** Obstacle direction: {s.obstacleDir} ***")
        
        
        # Object on middle of screen
        # elif self.x == s.HALF_SCREEN_WIDTH:
        #     self.obj = "rock"
        #     self.surf = s.rock
        #     self.mov_x = 0
        #     print("half")
        
        self.original_height = self.surf.get_height()
        self.original_width = self.surf.get_width()
        self.scaling_num = 1.05
        self.rect = self.surf.get_rect(
            center = (
                self.x,
                self.y
            )
        )
        if mode == 1:
            self.helper()
    
    def scale_sprite(self):
        if self.obj == "trunk":
            self.scaled_width = int(self.original_width * self.scaling_num) * 3
        else:
            self.scaled_width = int(self.original_width * self.scaling_num)
        self.scaled_height = int(self.original_height * self.scaling_num)

        self.rect.width = self.scaled_width
        self.rect.height = self.scaled_height

        if self.obj == "trunk":
            self.surf = pg.transform.scale(s.trunk, (int(self.scaled_width), self.scaled_height))
        else:
            self.surf = pg.transform.scale(s.rock, (int(self.scaled_width), self.scaled_height))
        self.rect.center = (self.x-1, self.y-1)
        
        ###############################
        # Move obstacle on y axis
        self.y += self.speed

        ###############################
        # Move obstacle on x axis
        self.x += self.mov_x
        ###############################
        
        # print(f"(width, height): {self.surf.get_width()}, {self.surf.get_height()}")
        # print(f"(width, height): {self.surf}")
        
        if self.scaling_num < 2.5:
            self.scaling_num += s.obsScale     
         

    def helper(self):
        self.helpX = s.HALF_SCREEN_WIDTH
        self.helpY = s.HALF_SCREEN_HEIGHT
        s.helper_sound.play()
        if self.x < s.HALF_SCREEN_WIDTH:
            self.helpSurf = s.right_arrow
        else:
            self.helpSurf = s.left_arrow
        self.helpRect = self.helpSurf.get_rect(
            center = (
                self.helpX,
                self.helpY
            )
        )
            
    
    def update(self):
        # print(self.rect)
        self.scale_sprite()
        self.rect.move_ip(self.mov_x, self.speed)
        if self.rect.top > s.SCREEN_HEIGHT:
            
            # s.obstacleDir = None
            # if s.obstacleDir == None:
                # print("*** Obstacle: None ***")
            self.kill()
            s.score += 1
            s.scoreArr = list(map(int, str(s.score)))
            print(f"Score: [{s.score}]")
            # print(f"Lista = {s.scoreArr}")
            s.score_snd.play()
            # g.Game().text = s.font.render(f"Pontuação: {str(self.score)}", True, s.BLACK)
            