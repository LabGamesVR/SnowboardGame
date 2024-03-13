import pygame as pg
import settings as s
import random
from game import *

class Cloud(pg.sprite.Sprite):
    
    def __init__(self):
        super(Cloud, self).__init__()
        self.speed = random.choice([-2, -1, 1, 2]) # Random speed between -3 and 3
        self.surf = s.clouds[random.choice([0, 1, 2, 3])] # Random sprite between 4 models

        # Change spawning x position according to movement direction defined on self.speed 
        # (self.speed < 0 = left; self.speed > 0 = right)
        if self.speed < 0:
            self.x = s.SCREEN_WIDTH+20
        else:
            self.x = 0-20
        self.rect = self.surf.get_rect(
            center = (
                self.x,
                random.randint(0, s.SCREEN_HEIGHT/3)
            )
        )
        
    
    def update(self):
        # Move the cloud and kill it when out of screen
        self.rect.move_ip(self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        elif self.rect.left > s.SCREEN_WIDTH:
            self.kill()

            