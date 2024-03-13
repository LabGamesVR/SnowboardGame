import pygame as pg
import settings as s
import math

class Sprites():
    
    def __init__(self):
        self.scaling_z_map = []
        self.scale_down_factor = 1/20
        self.y_world = -10  #change this value if the sprites moves wrongly
        self.fov = 60
        self.dist = s.HALF_SCREEN_WIDTH/math.tan(math.radians(self.fov/2))
        self.z_map = []
        self.make_z_map()
        self.load_sprites()
    
    def make_z_map(self):
        for i in range(s.HALF_SCREEN_HEIGHT-1, -1, -1):
            self.y_screen = i
            self.z = self.y_world / (self.y_screen - s.HALF_SCREEN_HEIGHT)
            self.z_map.append(self.z)
            self.scaling_z_map.append(1/self.z*self.scale_down_factor)
            
        self.z_map_lenght = len(self.z_map)
        self.speed_z_map = self.z_map.copy()
        self.speed_z_map.reverse()
        self.offroad_color = s.light_road.get_at((0, 0))
        self.road_width = s.light_road.get_width()
        
        self.point_1 = [0, 0]
        while s.light_road.get_at(self.point_1) == self.offroad_color:
            self.point_1[0] += 1
            if self.point_1[0] > self.road_width:
                break
                
        self.point_2 = [self.road_width-1, 0]
        while s.light_road.get_at(self.point_2) == self.offroad_color:
            self.point_2[0] -= 1
            if self.point_2[0] < 0:
                break
            
        self.road_end_width = self.point_2[0] - self.point_1[0]
        self.road_start_width = self.road_width
        self.road_start_y = s.light_road.get_height()
        self.road_end_y = 0
        self.increment = (self.road_end_width - self.road_start_width) / (self.road_end_y - self.road_start_y)
        self.road_half_width = []
        self.z_map = []
        self.scaling_z_map = []
        self.speed_z_map = []

        for y in range(s.HALF_SCREEN_HEIGHT):
            self.width = self.road_start_width + ((y - self.road_start_y) * self.increment)
            self.road_half_width.append(int(self.width/2))
            self.z_map.append(self.road_start_width/self.width)
            self.scaling_z_map.append(self.width/self.road_start_width)
            self.speed_z_map.append((self.width/self.road_start_width/6))
        
        
    def load_sprites(self):
        self.sprites = [
            {'image': s.snowman, 'scaled_image': None, 'track_pos': 10, 'pos': [0, 0],
                'width': s.snowman.get_width(), 'height': s.snowman.get_height(),
                'side': 'right', 'scaled_width': 0, 'scaled_height': 0, 'mirrored': True},
            {'image': s.snow_tree, 'scaled_image': None, 'track_pos': 40, 'pos': [0, 0],
                'width': s.snow_tree.get_width(), 'height': s.snow_tree.get_height(),
                'side': 'right', 'scaled_width': 0, 'scaled_height': 0, 'mirrored': True},
            {'image': s.snowman, 'scaled_image': None, 'track_pos': 70 ,'pos': [0, 0],
                'width': s.snowman.get_width(), 'height': s.snowman.get_height(),
                'side': 'right', 'scaled_width': 0, 'scaled_height': 0, 'mirrored': True},
            {'image': s.snow_tree, 'scaled_image': None, 'track_pos': 100 ,'pos': [0,0],
                'width': s.snow_tree.get_width(), 'height': s.snow_tree.get_height(),
                'side': 'right', 'scaled_width': 0, 'scaled_height': 0, 'mirrored': True}
        ]
    
    def update_sprites_pos(self):
        for sprite in self.sprites:
            sprite['track_pos'] += s.road_acceleration * self.speed_z_map[int(sprite['track_pos'])]
            if sprite['track_pos'] > self.z_map_lenght:
                sprite['track_pos'] = 10
                self.sprites.insert(0, self.sprites.pop())
    
    def scale_sprites(self, i):
        for sprite in self.sprites:
            if int(sprite['track_pos']) == i:
                sprite['scaled_width'] = int(sprite['width'] * self.scaling_z_map[i])
                sprite['scaled_height'] = int(sprite['height'] * self.scaling_z_map[i])
                sprite['scaled_image'] = pg.transform.scale(sprite['image'], (sprite['scaled_width'], sprite['scaled_height']))
                if sprite['side'] == 'right':
                    sprite['pos'][0] = s.HALF_SCREEN_WIDTH + self.road_half_width[i]
                    sprite['pos'][1] = i + s.HALF_SCREEN_HEIGHT - sprite['scaled_height']
                
                elif sprite['side'] == 'left':
                    sprite['scaled_image'] = pg.transform.flip(sprite['scaled_height'], True, False)
                    sprite['pos'][0] = s.HALF_SCREEN_WIDTH - self.road_half_width[i] - sprite['scaled_width']
                    # sprite['pos'][0] = s.HALF_SCREEN_WIDTH - sprite['scaled_width']
                    sprite['pos'][1] = i + s.HALF_SCREEN_HEIGHT - sprite['scaled_height']
    
    def blit_sprites(self, screen):
        for sprite in self.sprites:
            screen.blit(sprite['scaled_image'], sprite['pos'])
            if sprite['mirrored']:
                if sprite['side'] == 'right':
                    sprite['pos'][0] = s.HALF_SCREEN_WIDTH - self.road_half_width[int(sprite['track_pos'])] - sprite['scaled_width']
                    # sprite['pos'][0] = s.HALF_SCREEN_WIDTH - sprite['scaled_width']

                elif sprite['side'] == 'left':
                    sprite['pos'][0] = s.HALF_SCREEN_WIDTH + self.road_half_width[int(sprite['track_pos'])]

                sprite['scaled_image'] = pg.transform.flip(sprite['scaled_image'], True, False)
                screen.blit(sprite['scaled_image'], sprite['pos'])