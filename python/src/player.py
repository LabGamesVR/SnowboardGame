import pygame as pg
import time
import settings as s
from game import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = s.P_IMAGE[2]
        self.rect = self.surf.get_rect(center=(int(self.surf.get_width()/2), int(self.surf.get_height())-20))
        self.direction = None
        self.rect[0] = (s.SCREEN_WIDTH/2) - (s.P_X/2)
        self.rect[1] = s.SCREEN_HEIGHT - (s.P_Y+10)
        self.hitbox = pg.Rect((self.rect[0]+13, self.rect[1]+142), (self.rect[2]-24, 24))
        # print(self.hitbox)
        self.vel = s.VELOCITY
        self.life_count = 3
        self.keyPressedRight = False
        self.keyPressedLeft = False
        s.errorCounter = 0
        self.movementTimer = 0  # pode ser adicionado um timer para começar a contar os erros
        self.startTimer = time.time()
        self.joystick()
    
    def resetLife(self):
        self.life_count = 3
    
    def joystick(self):
        self.joystick_count = pg.joystick.get_count()
        if self.joystick_count > 0:
            for i in range(self.joystick_count):
                self.joystick = pg.joystick.Joystick(i)
                self.joystick.init()
            
            self.left_btn = self.joystick.get_button(9)
            self.right_btn = self.joystick.get_button(8)
        
    def update(self):
        # print(f"MovementTimer = {self.movementTimer}")
        # When skateboard is connected
        if self.joystick_count > 0:
            self.axis = self.joystick.get_axis(0) # Get Axis movement
            
            # Move player right
            if pg.key.get_pressed()[pg.K_d] or self.axis > 0.1 or self.right_btn == 1:
            # if self.axis < -0.01:
                self.movementElapsedTime = time.time() - self.startTimer
                self.keyPressedLeft = False
                # print(f"ElapsedTime = {self.movementElapsedTime:.2f}")
                # self.movementTimer = 0
                # self.movementTimer = time.time()
                if s.obstacleDir == "RIGHT" and self.movementElapsedTime > self.movementTimer and not(self.keyPressedRight):
                    s.errorCounter += 1
                    print(f"ERROR COUNTER: {s.errorCounter}")
                    self.startTimer = time.time()
                    self.keyPressedRight = True

                self.direction = "right"
                self.rect.move_ip(self.vel, 0)
                self.hitbox[0] = self.rect[0]-5
                self.hitbox[2] = 160
                self.surf = s.P_IMAGE[1]
            
             # Move player left
            elif pg.key.get_pressed()[pg.K_a] or self.axis < -0.1 or self.left_btn == 1:
            # elif self.axis > 0.01:
                self.movementElapsedTime = time.time() - self.startTimer
                self.keyPressedRight = False
                # print(f"ElapsedTime = {self.movementElapsedTime:.2f}")
                # self.movementTimer = 0
                # self.movementTimer = time.time()
                if s.obstacleDir == "LEFT" and self.movementElapsedTime > self.movementTimer and not(self.keyPressedLeft):
                    s.errorCounter += 1
                    print(f"ERROR COUNTER: {s.errorCounter}")
                    self.startTimer = time.time()
                    self.keyPressedLeft = True
                    
                self.direction = "left"
                self.rect.move_ip(-self.vel, 0)
                self.hitbox[0] = self.rect[0]+31
                self.hitbox[2] = 160
                self.surf = s.P_IMAGE[0]
            
             # Change sprite do idle when not moving
            else:
                self.keyPressedRight = False
                self.keyPressedLeft = False
                self.surf = s.P_IMAGE[2]
                if self.direction == "right":
                    self.hitbox[0] += 15
                    self.direction = None
                
                elif self.direction == "left":
                    self.hitbox[0] -= 13
                    self.direction = None
        
        # When skateboard is not connected
        else:
            # Move player right
            if pg.key.get_pressed()[pg.K_d]:
                self.movementElapsedTime = time.time() - self.startTimer
                self.keyPressedLeft = False
                # print(f"ElapsedTime = {self.movementElapsedTime:.2f}")
                # self.movementTimer = 0
                # self.movementTimer = time.time()
                if s.obstacleDir == "RIGHT" and self.movementElapsedTime > self.movementTimer  and not(self.keyPressedRight):
                    s.errorCounter += 1
                    print(f"ERROR COUNTER: {s.errorCounter}")
                    self.startTimer = time.time()
                    self.keyPressedRight = True
                    
                self.direction = "right"
                self.rect.move_ip(self.vel, 0)
                self.hitbox[0] = self.rect[0]-5
                self.hitbox[2] = 160
                self.surf = s.P_IMAGE[1]
            
             # Move player left
            elif pg.key.get_pressed()[pg.K_a]:
                self.movementElapsedTime = time.time() - self.startTimer
                self.keyPressedRight = False
                # print(f"ElapsedTime = {self.movementElapsedTime:.2f}")
                if s.obstacleDir == "LEFT" and self.movementElapsedTime > self.movementTimer  and not(self.keyPressedLeft):
                    s.errorCounter += 1
                    print(f"ERROR COUNTER: {s.errorCounter}")
                    # self.startTimer = 0
                    self.startTimer = time.time()
                    self.keyPressedLeft = True
                    
                self.direction = "left"
                self.rect.move_ip(-self.vel, 0)
                self.hitbox[0] = self.rect[0]+31
                self.hitbox[2] = 160
                self.surf = s.P_IMAGE[0]
            
             # Change sprite to idle when not moving
            else:
                self.keyPressedRight = False
                self.keyPressedLeft = False
                self.surf = s.P_IMAGE[2]
                if self.direction == "right":
                    self.hitbox[0] += 15
                    self.direction = None
                
                elif self.direction == "left":
                    self.hitbox[0] -= 13
                    self.direction = None

        
        # Keep player on track
        if self.rect.left < 0 + (s.SCREEN_WIDTH*0.1):
            self.rect.left = 0 + (s.SCREEN_WIDTH*0.1)
            
        if self.rect.right > s.SCREEN_WIDTH - (s.SCREEN_WIDTH*0.1):
            self.rect.right = s.SCREEN_WIDTH - (s.SCREEN_WIDTH*0.1)

        # print(self.axis)
        # print(self.rect)
    
    def take_damage(self):
        self.life_count -= 1
            
        