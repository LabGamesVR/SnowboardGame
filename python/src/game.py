import pygame as pg
import sys
import player as p
import settings as s
import cloud as c
import sprites as spr
import obstacle as obs
import os
# import arduino as ard
import time
import csv
from datetime import datetime
from datetime import date
import serial
import serial.tools.list_ports
import glob
from timeit import default_timer as timer

class Game:
    # Game flow
    
    # Class constructor
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(s.DIMENSIONS)
        self.menu_loop = True
        pg.display.set_caption(s.TITLE)
        self.clock = pg.time.Clock()
        self.setupArduino()
        # self.process = 'testing.py'
        # self.ADDCLOUD = pg.USEREVENT + 1
        # self.ADDOBSTACLE = pg.USEREVENT + 2
        # # New clouds will spawn at 1000ms intervals
        # pg.time.set_timer(self.ADDCLOUD, 1000)
        # pg.time.set_timer(self.ADDOBSTACLE, 3000)
        # self.score = 0

    # def exec_arduino(self):
    #     os.system(f'python {self.process}')

    # setup arduino connection
    def setupArduino(self):

        self.isArduino = False
        self.baud = 9600
        self.checkData = "AcknowledgeData"
        self.ports = list(serial.tools.list_ports.comports())
        
        for p in self.ports:
            # print(p)
            if 'USB' in p.description and 'CH340' not in p.description:
                print("Arduino encontrado!")
                portName = str(p)
                tmp = portName.split(" ")
                self.port = tmp[0]
                self.isArduino = True
                print(tmp)
                break;
    
        # CRIAR UM ALERTA PARA INFORMAR QUE O ARDUINO NÃO ESTÁ CONECTADO
        # CRIAR TAMBÉM UM ALERTA PARA QUANDO MASTER E SLAVE NÃO ESTAREM CONECTADOS

    # Start a new game
    def new_game(self):
        print("NEW GAME") # DEBUG
        self.player = p.Player()
        # self.arduino = ard.Arduino()
        self.clouds = pg.sprite.Group()
        self.spr = spr.Sprites()
        self.obstacles = pg.sprite.Group()
        self.layered_sprites = pg.sprite.LayeredUpdates()
        self.layered_sprites.add(self.player, layer = 1)
        self.layered_sprites.add(self.obstacles, layer = 0)
        self.layered_sprites.add(self.clouds, layer = 0)
        self.header = True
        self.countdown()
        print("Countdown end!")
        # self.tutorial()
        # self.player.resetLife()
        if self.isArduino:
            self.ser = serial.Serial(self.port, 9600, timeout=0.050)
        self.random()
                
    
    # Run game loop
    def random(self):
        
        print("RANDOM MODE") # DEBUG
        self.ADDCLOUD = pg.USEREVENT + 1
        self.ADDOBSTACLE = pg.USEREVENT + 2
        # Reset obstacle event timer
        pg.time.set_timer(self.ADDOBSTACLE, 0)
        # New clouds will spawn at 1000ms intervals
        pg.time.set_timer(self.ADDCLOUD, 1000)
        pg.time.set_timer(self.ADDOBSTACLE, 3500)
        self.score = 0
        pg.mixer.music.play(-1)
        self.playing = True
        self.set_var()
        s.score = 0
        s.obstaclesElapsed = 0
        s.scoreArr = list(map(int, str(s.score)))
        s.startTime = 0
        s.startTime = time.time()
        if self.isArduino:
            self.dataToSend = '2'
            self.ser.write(self.dataToSend.encode())
            self.ser.flush()
            print(self.dataToSend)
        self.start = timer()
        self.tmpHitTime = timer()
        
        # self.arduino.check_ports()
        # self.arduino.connect()

        while self.playing:
            self.clock.tick(s.FPS)
            if self.isArduino:
                if self.ser.inWaiting() > 0:
                    self.incomingData = self.ser.readline().decode().strip()
                    # print(self.incomingData)
                    if self.checkData in self.incomingData:
                        self.dataToCsv = list(self.incomingData.split(","))
                        # print(f"raw list {self.dataToCsv}")
                        self.x = self.dataToCsv[1]
                        self.y = self.dataToCsv[2]
                        self.z = self.dataToCsv[3]
                        self.tmpTime = timer() # marca tempo sempre que chega dado
                        self.currTime = f'{(timer() - self.start):.2f}'
                        # self.dataToCsv.append(f'{self.currTime:.2f}')
                        # self.xAcc = self.dataToCsv[4]
                        # self.yAcc = self.dataToCsv[5]
                        # self.zAcc = self.dataToCsv[6]
                        # print(self.x, self.y, self.z, self.xAcc, self.yAcc, self.zAcc)
                        # self.dataToCsv = [self.x, self.y, self.z, self.xAcc, self.yAcc, self.zAcc]
                        self.elapsedHitTime = f'{(timer() - self.tmpHitTime):.2f}'
                        self.dataToCsv = [self.x, self.y, self.z, self.elapsedHitTime ,self.currTime]
                        print(f"modified list {self.dataToCsv}")
                    # data = (f"{data[0]}")
                        if self.x != '-1':
                            if self.header:
                                with open('results\\movement_graph.csv', 'a+') as file:
                                    reader = csv.reader(file)
                                    dataWriter = csv.writer(file, lineterminator='\n')
                                    self.dataToCsv = ['X', 'Y', 'Z', 'tempo_obstaculo', 'tempo_total']
                                    dataWriter.writerow(self.dataToCsv)
                                    self.header = False
                            if not self.header:
                                with open('results\\movement_graph.csv', 'a+') as file:
                                    reader = csv.reader(file)
                                    dataWriter = csv.writer(file, lineterminator='\n')
                                    dataWriter.writerow(self.dataToCsv)

                self.ser.write(self.dataToSend.encode())
                self.ser.flush()
            # self.line = self.ser.readline()
            # print(self.line)
            # self.arduino.get_data()
            self.events()
            self.update_game_screen()

# Get the RANDOM mode game events
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                
                # Add a new cloud if the existing number of clouds is lesser than 10
                elif event.type == self.ADDCLOUD:
                    if (len(self.clouds) < s.MAX_CLOUDS):
                        new_cloud = c.Cloud()
                        self.clouds.add(new_cloud)
                        self.layered_sprites.add(new_cloud, layer = 0)
                
                elif event.type == self.ADDOBSTACLE:
                    if (len(self.obstacles) < 2):
                        self.new_obs = obs.Obstacle(mode=2)
                        # self.new_stone2 = stn.Stone()
                        self.obstacles.add(self.new_obs)
                        # self.stones.add(self.new_stone2)
                        self.layered_sprites.add(self.new_obs, layer = 0)
                        # self.layered_sprites.add(self.new_stone2, layer = 0)
                
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.mx = pg.mouse.get_pos()[0]
                    self.my = pg.mouse.get_pos()[1]
                    print(self.mx, self.my)
                
                if self.player.life_count == 0:
                    # self.player.kill()
                    s.elapsedTime = f'{(time.time() - s.startTime):.2f}'
                    print(f"Time = [{s.elapsedTime}]")
                    pg.time.set_timer(self.ADDOBSTACLE, 0)
                    if self.isArduino:
                        self.dataToSend = '1'
                        self.ser.write(self.dataToSend.encode())
                        self.ser.flush()
                        self.ser.close()
                    self.playing = False



    # Run game in tutorial mode
    '''
    The tutorial mode will send 4 obstacles, always in the same pattern:
    - Left, Right, Left, Right
    '''
    def tutorial(self):
        self.player = p.Player()
        self.clouds = pg.sprite.Group()
        self.spr = spr.Sprites()
        self.obstacles = pg.sprite.Group()
        self.layered_sprites = pg.sprite.LayeredUpdates()
        self.layered_sprites.add(self.player, layer = 1)
        self.layered_sprites.add(self.obstacles, layer = 0)
        self.layered_sprites.add(self.clouds, layer = 0)
        self.player.resetLife()
        print("TUTORIAL MODE")
        self.ADDCLOUD = pg.USEREVENT + 1
        self.ADDOBSTACLE = pg.USEREVENT + 2
        pg.time.set_timer(self.ADDOBSTACLE, 0)
        pg.time.set_timer(self.ADDCLOUD, 1000)
        pg.time.set_timer(self.ADDOBSTACLE, 5000)
        self.score = 0
        pg.mixer.music.play(-1)
        self.playingTutorial = True
        self.set_var()
        self.sideArr = [s.obs_left, s.obs_right,s.obs_left, s.obs_right]
        self.sideIndex = 0
        s.score = 0
        s.obstaclesElapsed = 0
        s.scoreArr = list(map(int, str(s.score)))
        s.startTime = 0
        s.startTime = time.time()
        
        while self.playingTutorial:
            self.clock.tick(s.FPS)
            self.tutorialEvents()
            self.update_game_screen()
        
        # Get the TUTORIAL mode game events
    def tutorialEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            
            # Add a new cloud if the existing number of clouds is lesser than 10
            elif event.type == self.ADDCLOUD:
                if (len(self.clouds) < s.MAX_CLOUDS):
                    new_cloud = c.Cloud()
                    self.clouds.add(new_cloud)
                    self.layered_sprites.add(new_cloud, layer = 0)
            
            elif event.type == self.ADDOBSTACLE:
                if (len(self.obstacles) < 2):
                    if s.score == 4:
                        print("END OF TUTORIAL")
                        self.playingTutorial = False
                        self.tela_final_tutorial()
                    else:
                        self.new_obs = obs.Obstacle(mode=1, side=self.sideArr[self.sideIndex])
                        # self.new_stone2 = stn.Stone()
                        self.obstacles.add(self.new_obs)
                        # self.stones.add(self.new_stone2)
                        self.layered_sprites.add(self.new_obs, layer = 0)
                        # self.layered_sprites.add(self.new_stone2, layer = 0)
                        self.sideIndex += 1
                        if self.sideIndex == 4:
                            self.sideIndex = 0

            
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mx = pg.mouse.get_pos()[0]
                self.my = pg.mouse.get_pos()[1]
                print(self.mx, self.my)

            if self.player.life_count == 0:
                self.player.kill()
                pg.time.set_timer(self.ADDOBSTACLE, 0)
                self.tela_final_tutorial()
                # self.playingTutorial = False

     # Tutorial over screen
    def tela_final_tutorial(self):
        print("TUTORIAL GO screen") # DEBUG
        self.final_tutorial_loop = True
        # pg.mixer.init()
        # pg.mixer.music.load('snd\\musicaMenu.mp3')
        # pg.mixer.music.play(-1)
        
        while self.final_tutorial_loop:
            
            self.screen.blit(s.fundo, (0, 0))

            s.go_draw_group.draw(self.screen)
            
            if self.hover_check(s.retry_btn1):
                s.go_retry.draw(self.screen)
            elif self.hover_check(s.go_exit_btn1):
                s.go_quit.draw(self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.type == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mx = pg.mouse.get_pos()[0]
                    self.my = pg.mouse.get_pos()[1]
                    print(self.mx, self.my)
                    
                    # Retry
                    if self.mx >= 113 and self.mx <= 113 + 300 and self.my >= 456 and self.my <= 456 + 75:
                        print("click")
                        s.click_snd.play()
                        self.screen.blit(s.retry_btn3, [113, 456])
                        pg.display.update()
                        self.player.resetLife()
                        self.final_tutorial_loop = False
                        self.tutorial()
                    
                    # Quit
                    if self.mx >= 787 and self.mx <= 787 + 300 and self.my >= 456 and self.my <= 456 + 75:
                        s.click_snd.play()
                        self.screen.blit(s.go_exit_btn3, [787, 456])
                        pg.display.update()
                        pg.time.set_timer(self.ADDOBSTACLE, 0)
                        self.playingTutorial = False
                        self.final_tutorial_loop = False
            
            pg.display.update()
        pg.mixer.music.stop()



# Run game in controlled mode
    '''
    On the controlled mode, the user can control the side where the obstacle will go
    '''
    def controlled(self):
        if self.isArduino:
            self.ser = serial.Serial(self.port, 9600, timeout=0.050)
        self.player = p.Player()
        self.clouds = pg.sprite.Group()
        self.spr = spr.Sprites()
        self.obstacles = pg.sprite.Group()
        self.layered_sprites = pg.sprite.LayeredUpdates()
        self.layered_sprites.add(self.player, layer = 1)
        self.layered_sprites.add(self.obstacles, layer = 0)
        self.layered_sprites.add(self.clouds, layer = 0)
        self.player.resetLife()
        print("CONTROLLED MODE")
        self.ADDCLOUD = pg.USEREVENT + 1
        self.ADDOBSTACLE = pg.USEREVENT + 2
        pg.time.set_timer(self.ADDOBSTACLE, 0)
        pg.time.set_timer(self.ADDCLOUD, 1000)
        pg.time.set_timer(self.ADDOBSTACLE, 5000)
        self.score = 0
        pg.mixer.music.play(-1)
        self.playingControlled = True
        self.set_var()
        self.ControlledSideArr= []
        s.score = 0
        s.obstaclesElapsed = 0
        s.scoreArr = list(map(int, str(s.score)))
        s.startTime = 0
        s.startTime = time.time()
        if self.isArduino:
            self.dataToSend = '2'
            self.ser.write(self.dataToSend.encode())
            self.ser.flush()

        self.header = True
        self.start = timer()
        self.tmpHitTime = timer()

        while self.playingControlled:
            self.clock.tick(s.FPS)
            if (len(self.obstacles) == 0) and (len(self.ControlledSideArr) == 0):
                pg.time.set_timer(self.ADDOBSTACLE, 100)
                # print("TIMER = 100")
            if len(self.obstacles) >= 1:
                pg.time.set_timer(self.ADDOBSTACLE, 2000)
                # print("TIMER = 2000")
            
            if self.isArduino:
                if self.ser.inWaiting() > 0:
                    self.incomingData = self.ser.readline().decode().strip()
                    # print(self.incomingData)
                    if self.checkData in self.incomingData:
                        self.dataToCsv = list(self.incomingData.split(","))
                        # print(f"raw list {self.dataToCsv}")
                        self.x = self.dataToCsv[1]
                        self.y = self.dataToCsv[2]
                        self.z = self.dataToCsv[3]
                        self.tmpTime = timer() # marca tempo sempre que chega dado
                        self.currTime = f'{(timer() - self.start):.2f}'
                        # self.dataToCsv.append(f'{self.currTime:.2f}')
                        # self.xAcc = self.dataToCsv[4]
                        # self.yAcc = self.dataToCsv[5]
                        # self.zAcc = self.dataToCsv[6]
                        # print(self.x, self.y, self.z, self.xAcc, self.yAcc, self.zAcc)
                        # self.dataToCsv = [self.x, self.y, self.z, self.xAcc, self.yAcc, self.zAcc]
                        self.elapsedHitTime = f'{(timer() - self.tmpHitTime):.2f}'
                        self.dataToCsv = [self.x, self.y, self.z, self.elapsedHitTime ,self.currTime]
                        print(f"modified list {self.dataToCsv}")
                    # data = (f"{data[0]}")
                        if self.x != '-1':
                            if self.header:
                                with open('results\\movement_graph.csv', 'a+') as file:
                                    reader = csv.reader(file)
                                    dataWriter = csv.writer(file, lineterminator='\n')
                                    self.dataToCsv = ['X', 'Y', 'Z', 'tempo_obstaculo', 'tempo_total']
                                    dataWriter.writerow(self.dataToCsv)
                                    self.header = False
                            if not self.header:
                                with open('results\\movement_graph.csv', 'a+') as file:
                                    reader = csv.reader(file)
                                    dataWriter = csv.writer(file, lineterminator='\n')
                                    dataWriter.writerow(self.dataToCsv)

                self.ser.write(self.dataToSend.encode())
                self.ser.flush()

            self.controlledEvents()
            self.update_game_screen()


            # if self.playingControlled == False:
                # break
        print("saiu do controlled")
        self.save_screen()
        self.tela_final_controlled()


        # Get the CONTROLLED mode game events
    def controlledEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    self.ControlledSideArr.append(s.obs_right)
                    print(self.ControlledSideArr)
                
                if event.key == pg.K_LEFT:
                    self.ControlledSideArr.append(s.obs_left)
                    print(self.ControlledSideArr)

            # Add a new cloud if the existing number of clouds is lesser than 10
            elif event.type == self.ADDCLOUD:
                if (len(self.clouds) < s.MAX_CLOUDS):
                    new_cloud = c.Cloud()
                    self.clouds.add(new_cloud)
                    self.layered_sprites.add(new_cloud, layer = 0)
            
            elif event.type == self.ADDOBSTACLE:

                if (len(self.obstacles) < 2):
                    if len(self.ControlledSideArr) == 0:
                        pass
                    else:
                        self.new_obs = obs.Obstacle(mode=1, side=self.ControlledSideArr.pop(0))
                        # self.new_stone2 = stn.Stone()
                        self.obstacles.add(self.new_obs)
                        # self.stones.add(self.new_stone2)
                        self.layered_sprites.add(self.new_obs, layer = 0)
                        print(self.ControlledSideArr)
                        print(f"objetos = {len(self.obstacles)} | array = {len(self.ControlledSideArr)}")
                        if (len(self.obstacles) == 0) and (len(self.ControlledSideArr) == 0):
                            pg.time.set_timer(self.ADDOBSTACLE, 100)
                            print("TIMER = 100")
                        if len(self.ControlledSideArr) >= 1:
                            pg.time.set_timer(self.ADDOBSTACLE, 5000)
                            print("TIMER = 5000")
                        # self.layered_sprites.add(self.new_stone2, layer = 0)

            
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mx = pg.mouse.get_pos()[0]
                self.my = pg.mouse.get_pos()[1]
                print(self.mx, self.my)

            if self.player.life_count == 0:
                self.player.kill()
                pg.time.set_timer(self.ADDOBSTACLE, 0)
                if self.isArduino:
                    self.dataToSend = '1'
                    self.ser.write(self.dataToSend.encode())
                    self.ser.flush()
                    self.ser.close()
                self.playingControlled = False

     # Tutorial over screen
    def tela_final_controlled(self):
        print("CONTROLLED GO screen") # DEBUG
        self.final_controlled_loop = True
        # pg.mixer.init()
        # pg.mixer.music.load('snd\\musicaMenu.mp3')
        # pg.mixer.music.play(-1)
        
        while self.final_controlled_loop:
            
            self.screen.blit(s.fundo, (0, 0))

            s.go_draw_group.draw(self.screen)
            
            if self.hover_check(s.retry_btn1):
                s.go_retry.draw(self.screen)
            elif self.hover_check(s.go_exit_btn1):
                s.go_quit.draw(self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.type == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mx = pg.mouse.get_pos()[0]
                    self.my = pg.mouse.get_pos()[1]
                    print(self.mx, self.my)
                    
                    # Retry
                    if self.mx >= 113 and self.mx <= 113 + 300 and self.my >= 456 and self.my <= 456 + 75:
                        print("click")
                        s.click_snd.play()
                        self.screen.blit(s.retry_btn3, [113, 456])
                        pg.display.update()
                        self.player.resetLife()
                        self.final_controlled_loop = False
                        self.controlled()
                    
                    # Quit
                    if self.mx >= 787 and self.mx <= 787 + 300 and self.my >= 456 and self.my <= 456 + 75:
                        s.click_snd.play()
                        self.screen.blit(s.go_exit_btn3, [787, 456])
                        pg.display.update()
                        pg.time.set_timer(self.ADDOBSTACLE, 0)
                        self.playingControlled = False
                        self.final_controlled_loop = False
            
            pg.display.update()
        pg.mixer.music.stop()


    # Quit game
    def quit(self):
        pg.quit()
        sys.exit()
    
    # Set variables used for perspective on camera
    def set_var(self):
        self.texture_position = s.texture_position
        self.ddz = s.ddz
        self.dz = s.dz
        self.z = s.z
        self.road_pos = s.road_pos
        self.road_acceleration = s.road_acceleration
        self.texture_position_acceleration = s.texture_position_acceleration
        self.texture_position_threshold = s.texture_position_threshold
        self.half_texture_position_threshold = s.half_texture_position_threshold
    
    
    # Update the game screen
    def update_game_screen(self):
        self.road_pos+=self.road_acceleration
        if self.road_pos>=self.texture_position_threshold:
            self.road_pos=0
        self.spr.update_sprites_pos()
                
        # Draw the road
        self.texture_position=self.road_pos
        self.dz=0
        self.z=0            
        self.screen.blit(s.bg_img, (0, 0))


        for i in range(s.HALF_SCREEN_HEIGHT-1,-1,-1):
            if self.texture_position<self.half_texture_position_threshold:
                self.screen.blit(s.light_road,(0,i+s.HALF_SCREEN_HEIGHT),(0,i,s.SCREEN_WIDTH,1))   
            else:
                self.screen.blit(s.dark_road,(0,i+s.HALF_SCREEN_HEIGHT),(0,i,s.SCREEN_WIDTH,1))
            self.spr.scale_sprites(i)
            
            self.dz+=self.ddz
            self.z+=self.dz
            self.texture_position+=self.texture_position_acceleration+self.z
            if self.texture_position>=self.texture_position_threshold:
                self.texture_position=0
        
        self.spr.blit_sprites(self.screen)
        
        self.clouds.update()
        self.obstacles.update()
        self.player.update()
        
        
        # Draw all entities from layered sprite group
        for entity in self.layered_sprites:
            self.screen.blit(entity.surf, entity.rect)
        
        self.hud()
        
        # Draw player's hitbox
        # pg.draw.rect(self.screen, s.RED, self.player.hitbox, 1)
        
        
        # Check for collisions between player and obstacle
        for obstacle in self.obstacles:
            # pg.draw.rect(self.screen, s.BLUE, obstacle.rect, 1)
            
            # Draw helping arrow on screen
            if obstacle.y > (s.SCREEN_HEIGHT*0.5) and obstacle.y < (s.SCREEN_HEIGHT*0.7):
                self.screen.blit(obstacle.helpSurf, ((s.SCREEN_WIDTH/2) - (s.helperW/2), s.SCREEN_HEIGHT*0.2))
            if self.player.hitbox.colliderect(obstacle.rect):
                if self.player.life_count == 3: # se ainda nao levou dano
                    self.elapsedHitTime = f'{(timer() - self.start):.2f}'
                    if not self.isArduino:
                        with open('results\\movement_graph.csv', 'a+') as file:
                            reader = csv.reader(file)
                            dataWriter = csv.writer(file, lineterminator='\n')
                            self.dataToCsv = ["pontuacao", "tempo_obstaculo", "tempo_total"]
                            dataWriter.writerow(self.dataToCsv)
                else:
                    self.elapsedHitTime = f'{(timer() - self.tmpHitTime):.2f}'
                self.tmpHitTime = timer() # marca tempo que levou dano
                self.player.take_damage()
                s.bonk_snd.play()
                # print("HIT")
                s.obstacleDir = None
                obstacle.kill()
                
                if not self.isArduino:
                    self.currTime = f'{(timer() - self.start):.2f}'
                    with open('results\\movement_graph.csv', 'a+') as file:
                        reader = csv.reader(file)
                        dataWriter = csv.writer(file, lineterminator='\n')
                        self.dataToCsv = [s.scoreArr,self.elapsedHitTime,self.currTime]
                        dataWriter.writerow(self.dataToCsv)
            # else:
            #     self.score += 1
            #     self.text = s.font.render(f"Pontuação: {str(self.score)}", True, s.BLACK)
        # self.text = s.font.render(f"Pontuação: {str(s.score)}", True, s.BLACK) 
        # self.score = list(str(s.score))
        # print(f"Lista = {s.scoreArr}")
        # self.screen.blit(self.text, self.textRect)
        self.show_score()
        pg.display.flip()
    
    # Shows score on screen
    def show_score(self):
        s.score_txt_draw_group.draw(self.screen)

        if len(s.scoreArr) == 1:
            self.screen.blit(s.nums[int(s.scoreArr[0])], (1050, 37))
        
        else:
            self.screen.blit(s.nums[int(s.scoreArr[0])], (1050, 37))
            self.screen.blit(s.nums[int(s.scoreArr[1])], (1085, 37))

    # Shows life count
    def hud(self):
        self.screen.blit(s.scoreboard, (10, 10)) #20 20

        for i in range(self.player.life_count):
            self.screen.blit(s.life, s.heart_pos[i])
        
        # Talvez mudar isso para cada parte do jogo, um life_count no tutorial e um no playing
        # if self.player.life_count == 0:
        #     # self.player.kill()
        #     s.elapsedTime = time.time() - s.startTime
        #     print(f"Time = [{s.elapsedTime}]")
        #     pg.time.set_timer(self.ADDOBSTACLE, 0)
        #     self.playing = False
    
    # Shows countdown screen before game
    def countdown(self):
        for i in range(3, -1, -1):
            self.screen.blit(s.blurBG, (0, 0))
            pg.display.update()
            if i > 0:
                s.count_start.play()
            else:
                s.count_end.play()
            self.screen.blit(s.numsCount[i], (s.SCREEN_WIDTH//2 - (s.countW/2), s.SCREEN_HEIGHT//2 - (s.countH/2)))
            print(f"*** COUNTING {i} ***")
            pg.display.update()
            time.sleep(1)
            

    def escreve(self, text, font, color, surface, x, y):
        self.textobj = font.render(text, 1, color)
        self.textrect = self.textobj.get_rect()
        self.textrect.topleft = (x, y)
        surface.blit(self.textobj, self.textrect)

    # Check if mouse is hovering a rect
    def hover_check(self, img):
        return img.rect.collidepoint(pg.mouse.get_pos())

    # Main menu screen
    def main_menu(self):
        print("MAIN_MENU") # DEBUG
        if self.menu_loop:
            self.menu_loop = True
            pg.mixer.init()
            pg.mixer.music.load('snd\\musicaMenu.mp3')
            pg.mixer.music.play(-1)

            while self.menu_loop:

                self.screen.blit(s.fundo, (0, 0))

                self.escreve('Pressione Esc para sair', s.fontesc, (255, 255, 255), self.screen, (s.SCREEN_WIDTH/1.19) , (s.SCREEN_HEIGHT/1.03))
                
                s.mm_draw_group.draw(self.screen)
                
                if self.hover_check(s.start_btn1):
                    s.mm_start.draw(self.screen)
                elif self.hover_check(s.training_btn1):
                    s.mm_training.draw(self.screen)
                elif self.hover_check(s.exit_btn1):
                    s.mm_quit.draw(self.screen)
                    
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.mx = pg.mouse.get_pos()[0]
                        self.my = pg.mouse.get_pos()[1]
                        print(self.mx, self.my)
                        
                        # Start
                        if self.mx >= 60 and self.mx <= 60 + 300 and self.my >= 200 and self.my <= 200 + 75:
                            print("click")
                            s.click_snd.play()
                            self.screen.blit(s.start_btn3, [60, 200])
                            pg.display.update()
                            self.menu_loop = False
                            self.new_game()

                        # Training
                        if self.mx >= 60 and self.mx <= 60 + 300 and self.my >= 285 and self.my <= 285 + 75:
                            print("click")
                            s.click_snd.play()
                            self.screen.blit(s.training_btn3, [60, 285])
                            pg.display.update()
                            self.countdown()
                            # self.tutorial()
                            # self.ser = serial.Serial(self.port, 9600, timeout=0.050)
                            self.controlled()
                        # Quit
                        if self.mx >= 60 and self.mx <= 60 + 300 and self.my >= 285 and self.my <= 370 + 75:
                            s.click_snd.play()
                            quit()

                            
                pg.display.update() 

            pg.mixer.music.stop()
    
    # Save name and score
    def save_screen(self):
        print("SAVE_SCREEN") # DEBUG
        self.score_loop = True
        self.inputRectX = 420
        self.inputRectY = 305
        self.inputRectW = 300
        self.inputRectH = 56
        self.inputRect = pg.Rect(self.inputRectX, self.inputRectY, self.inputRectW, self.inputRectH)
        self.activeColor = s.LIGHT_BLUE
        self.inactiveColor = s.BLUE
        # self.color = self.inactiveColor
        self.color = self.activeColor
        self.userTxt = ''
        self.maxLetters = 36
        self.isActive = False
        
        while self.score_loop:
            self.screen.blit(s.blurBG, (0, 0))
            
            self.escreve("Digite seu nome: ", s.font, s.WHITE, self.screen, 50, 300)
            s.score_draw_group.draw(self.screen)

            if self.hover_check(s.save_btn1):
                s.s_save.draw(self.screen)
            
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.quit()
                        
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.quit()
                        
                        # if self.isActive:
                        if event.key == pg.K_BACKSPACE:
                            self.userTxt = self.userTxt[:-1]
                        
                        elif event.key == pg.K_RETURN and self.userTxt != '':
                            # s.click_snd.play()
                            # self.results = (f"{self.userTxt}, {s.score}, {s.elapsedTime}\n")
                            # with open('results.txt', 'a+') as file:
                            #         file.write(self.results)
                            # self.score_loop = False
                            self.save_score()

                        else:
                            # if not event.key == pg.K_RETURN: # Ignore "Enter" key
                            if len(self.userTxt) <= self.maxLetters:
                                self.userTxt += event.unicode
                        
                        
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.mx = pg.mouse.get_pos()[0]
                        self.my = pg.mouse.get_pos()[1]
                        print(self.mx, self.my)
                        
                        
                        # if self.inputRect.collidepoint(event.pos):
                        #     self.isActive = True
                        # else:
                        #     self.isActive = False
                        
                        # Save
                        if (self.mx >= s.saveX and self.mx <= s.saveX + 300 and self.my >= s.saveY and self.my <= s.saveY + 75):
                            if self.userTxt != '':
                                print("click")
                                s.click_snd.play()
                                self.screen.blit(s.save_btn3, [s.saveX, s.saveY])
                                pg.display.update()
                                # self.results = (f"{self.userTxt}, {s.score}, {s.elapsedTime}\n")
                                # print(f"Name = [{self.userTxt}]\nScore = [{self.score}]\nTime = [{s.elapsedTime}]")
                                # print(self.results)
                                # with open('results.txt', 'a+') as file:
                                #     file.write(self.results)
                                # self.score_loop = False
                                
                                self.save_score()

            # if self.isActive:
            #     self.color = self.activeColor
            # else:
            #     self.color = self.inactiveColor
            
            
            pg.draw.rect(self.screen, self.color, self.inputRect)
            self.textSurface = s.font.render(self.userTxt, True, s.BLACK)
            self.screen.blit(self.textSurface, (self.inputRect.x + 5, self.inputRect.y - 5))
            self.inputRect.w = max(20, self.textSurface.get_width() + 10)
            pg.display.update()
    
    def save_score(self):
        s.click_snd.play()
        #                  Nome, Pontuação, Tempo de jogo, Obstáculos totais, Contagem de erros
        # self.results = (f"{str(self.userTxt)},{s.score},{s.elapsedTime:.2f},{s.obstaclesElapsed}")
        self.results = (f"{str(self.userTxt)},{s.score},{self.currTime},{s.obstaclesElapsed}")
        self.results = list(self.results.split(","))
        print(self.results)
        self.now = datetime.now()
        self.now.strftime("%d/%m/%Y %H:%M:%S")
        self.today = date.today()
        self.dir_path = f'.\\{self.userTxt.lower()}*.csv'
        self.files_found = glob.glob(self.dir_path)
        print(self.files_found)
        os.rename('results\\movement_graph.csv', f'results\\{self.userTxt.lower()}_{self.today}-{len(self.files_found)+1}.csv')
        with open('results\\results.csv', 'a+') as file:
            self.reader = csv.reader(file)
            self.scoreWriter = csv.writer(file, lineterminator='\n')
            self.scoreWriter.writerow(self.results)
        self.score_loop = False

    # Game over screen
    def tela_final(self):
        print("GO screen") # DEBUG
        self.final_loop = True
        # pg.mixer.init()
        # pg.mixer.music.load('snd\\musicaMenu.mp3')
        # pg.mixer.music.play(-1)
        
        while self.final_loop:
            
            self.screen.blit(s.fundo, (0, 0))

            self.escreve('Pressione Esc para sair', s.fontesc, (255, 255, 255), self.screen, (s.SCREEN_WIDTH/1.19) , (s.SCREEN_HEIGHT/1.03))

            s.go_draw_group.draw(self.screen)
            
            if self.hover_check(s.retry_btn1):
                s.go_retry.draw(self.screen)
            elif self.hover_check(s.go_exit_btn1):
                s.go_quit.draw(self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.type == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.mx = pg.mouse.get_pos()[0]
                    self.my = pg.mouse.get_pos()[1]
                    print(self.mx, self.my)
                    
                    # Retry
                    if self.mx >= 113 and self.mx <= 113 + 300 and self.my >= 456 and self.my <= 456 + 75:
                        print("click")
                        s.click_snd.play()
                        self.screen.blit(s.retry_btn3, [113, 456])
                        pg.display.update()
                        self.final_loop = False
                        self.new_game()
                    
                    # Quit
                    if self.mx >= 787 and self.mx <= 787 + 300 and self.my >= 456 and self.my <= 456 + 75:
                        s.click_snd.play()
                        self.screen.blit(s.go_exit_btn3, [787, 456])
                        pg.display.update()
                        self.quit()
            
            pg.display.update()
        pg.mixer.music.stop()