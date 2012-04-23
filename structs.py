import pygame, sys, random, itertools
from pygame.locals import *
from utils import load_image
class Level:
    def __init__(self,floor_image,background_image):
        self.floor_image = floor_image
        self.background_image = load_image(background_image)
        self.floors = []

    def add_floor(self):
        self.floors.append(Floor(self.floor_image))

    def remove_floor(self):
        self.floors.remove(self.floors[0])

class Background:
    def __init__self(self,type,background):
        if type=='color':
            self.color = background
        if type=='color with objects':
            self.color = background[0]
            self.object= background[1]
            self.objects=[]
        if type=='image':
            self.image = load_image(background)


        
class Object:
    def __init__(self,images,loc):
        self.images = []
        for image in images:
            self.images.append(load_image(image,-1))
        self.timer = 0
        self.frequency = 60
        self.image = 0
        self.loc = loc

    def update(self,speed=[0,0]):
        self.timer+=1
        if self.timer>self.frequency:
            self.timer = 0
            self.image +=1
            self.image = self.image%2
        self.loc[0] += speed[0]
        self.loc[1] += speed[1]
           
    def draw(self,surface):
        surface.blit(self.images[self.image][0],self.loc)
    
class MainGame:
    def __init__(self,size):
        self.size = size
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.canvas = pygame.Surface((640,480))
        self.player = Player('ball.png')
        # Set Background to White
        self.canvas.fill((250,250,250))
        self.score = Status_Box(self.player.score)
        self.difficulty = 10



    def run(self):
        self.floors = []
        self.menus = []
        self.levels=[Level('cloud_flat','cartoon-clouds.png'), Level('rock_flat','rock_background.png')]
        self.parallax = 0
        self.level = 0
        while 1:
            if self.player.transition == -1: sys.exit()
            if self.player.transition == 1:
                if self.level+1 == len(self.levels):
                    self.menus.append(Menu(['You win!'],'The End',(300,150)))
                    self.menus[-1].activate(self.screen,self)
                    sys.exit()
                else:
                    self.level+=1
                    self.player.rect = self.player.rect.move([0,-400])
                    self.player.transition = 0
            self.clock.tick(60)
            self.player.score+=self.difficulty/10
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_RIGHT]: self.player.move(1)
            elif pressed_keys[K_LEFT]: self.player.move(-1)
            for event in pygame.event.get():
                if event.type == QUIT: sys.exit()
                if event.type == KEYDOWN:
                #    if event.key == K_RIGHT: self.player.move(1)
                #    if event.key == K_LEFT: self.player.move(-1)
                    if event.key == K_SPACE: self.player.jump()
                    if event.key == K_m: 
                        if len(self.menus)==0:
                            self.menus.append(Menu(['New Game','Options','Quit'],'Main Menu',(300,150)))
                            self.menus[-1].activate(self.screen,self)
                            self.menus.remove(self.menus[-1])
                if event.type == KEYUP:
                    if event.key == K_RIGHT: self.player.move(0)
                    if event.key == K_LEFT: self.player.move(0)


            # Count floors
            min_floor_height = 0
            for floor in self.levels[self.level].floors:
                floor.update()
                min_floor_height = max(min_floor_height,floor.rect[0].bottom)
                if floor.loc < -40: self.levels[self.level].remove_floor()
            if min_floor_height < 380 + self.difficulty:
                self.levels[self.level].add_floor()
            self.player.update(list(itertools.chain.from_iterable([floor.rect for floor in self.levels[self.level].floors])))
            self.score.update(self.player.score)


#           Drawing stuff
            self.canvas.fill((0,0,250))
#           Draw Background
            for i in range(0,640,167):
                for j in range(-168, 480, 167):
                    self.canvas.blit(self.levels[self.level].background_image[0],(i,j+self.parallax))
            self.parallax = (self.parallax - 1)%168
            self.player.draw(self.canvas)
            for floor in self.levels[self.level].floors:
                floor.draw(self.canvas)
            self.score.draw(self.canvas)

            self.screen.blit(self.canvas,[0,0])
            pygame.display.flip()

class Player:
    def __init__(self,image,loc=[0,0]):
        self.image,self.rect=load_image(image,-1)
        self.speed=[0,0]
        self.direction=1
        self.score = 0
        self.jumping = 0
        self.transition = 0
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def jump(self):
        if self.speed[1]==-2:
            self.speed[1] = -12
            self.jumping = 1
    def move(self,direction):
        self.direction=direction
        self.speed[0]= 5*direction

    def update(self,floors):
        if self.rect.bottom < 0: self.transition = -1
        if self.rect.top > 480: self.transition = 1
        c = self.rect.collidelist(floors)
#        if c==-1: 
#            if self.jumping==0:
#                self.speed[1]=5
#            else: self.speed[1]+=1
#            self.speed[0]=0
#        else:
#            self.jumping = 0
#            self.speed[1]=-2
        if self.jumping==1:
            self.speed[1]+=1
            if self.speed[1]==5:
                self.jumping = 0
        else:
            if c==-1:
                self.speed[1] = 5
            else:
                self.jumping = 0
                self.speed[1] = -2

        self.rect = self.rect.move(self.speed)

class Floor:
    def __init__(self,floor_image,objects=0):
        self.loc = 490
        self.speed = [0,-2]
        self.hole = random.randrange(0,550,50)
        self.hole_width = 100
        self.rect = [pygame.Rect((0, self.loc, self.hole, 20)),pygame.Rect((self.hole+self.hole_width, self.loc, 640-self.hole-self.hole_width, 20))]
        self.image = [load_image(floor_image+"_left.png",-1),load_image(floor_image+"_middle.png",-1),load_image(floor_image+"_right.png",-1)]
        self.objects = []
        if objects==0 and random.randrange(1,16,1)==1:
            self.objects.append(Object(['alien1.png','alien2.png'],[self.hole,390]))

    def draw(self,surface):
        #surface.fill((0,0,0), self.rect[0])
        #surface.fill((0,0,0), self.rect[1])
#       Draw Left Side
        for o in self.objects:
            o.draw(surface)
        for i in range(0,self.hole,50):
            surface.blit(self.image[1][0],self.rect[0].move([i,-10]))
        surface.blit(self.image[2][0],self.rect[0].move([self.hole,-10]))
#       Draw Right Side
        for i in range(self.hole+150,640,50):
            surface.blit(self.image[1][0],self.rect[0].move([i,-10]))
        surface.blit(self.image[0][0],self.rect[0].move([self.hole+100,-10]))

    def update(self):
        self.loc = self.loc - 2
        self.rect[0] = (self.rect)[0].move(self.speed)
        self.rect[1] = (self.rect)[1].move(self.speed)
        for o in self.objects:
            o.update(self.speed)

class Menu:
    def __init__(self,options,title,loc=[0,0]):
        self.options = options
        self.active = 0
        self.title = title
        self.width = max(len(option) for option in options)
        self.width = max(self.width,len(self.title))
        self.width = self.width * 15 + 30
        self.font = pygame.font.Font(None, 36)
        self.loc = loc
        self.background = pygame.Surface((640,480))

#       Figure out height
        self.height = (len(options)+1)*32 + 25
        self.surface = pygame.Surface((self.width, self.height))
        self.cursor = 0

    def activate(self,surface,player):
#       Create Background
        self.background.blit(surface,(0,0))
        self.active = 1
        self.draw(surface)
        while self.active == 1:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_m:
                        self.active = 0
                    if event.key==K_DOWN:
                        self.cursor= (self.cursor+1) % len(self.options)
                    if event.key==K_UP:
                        self.cursor= (self.cursor-1) % len(self.options)
                    if event.key==K_RETURN:
                        self.run_option(surface,player)
            surface.blit(self.background,(0,0))
            self.draw(surface)
                   
    def run_option(self,surface,player):
        if self.cursor==2: sys.exit()
        if self.cursor==1: 
            difficulty = Difficulty_Menu(['1 - Easy','2 - Normal','3 - Challenging','4 - Hard','5 - Are you serious?'],'Difficulty',(300,100))
            difficulty.activate(surface,player)

    def draw(self,surface):
        normal_background = (10,10,10)
        selected_background = (250,250,250)
        self.surface.fill((0,0,250))
        pygame.draw.rect(self.surface,(0,0,0),(0,0,self.width,self.height),5)
        pygame.draw.rect(self.surface,(0,0,139),(5,5,self.width-10,self.height-10),5)


        text = self.font.render(self.title,1,normal_background)
        textpos = [10, 12]
        self.surface.blit(text,textpos)
        pygame.draw.line(self.surface,(0,0,0),(10,40),(self.width-12,40),3)
        for index,option in enumerate(self.options):
            if index==self.cursor: background = selected_background
            else: background = normal_background
            text = self.font.render(option,1,background) # text, antialias, background
            textpos = [10,32*(index+1)+12]
            self.surface.blit(text,textpos)
        x = surface.get_width()/2-self.width/2
        y = surface.get_height()/2-self.height/2
        surface.blit(self.surface,(x,y))
        pygame.display.flip()

class Status_Box:
    def __init__(self,data):
        self.data = data
        self.surface = pygame.Surface((50,20))
        self.font = pygame.font.Font(None, 32)
        self.bg_color = (150,150,150)

    def update(self,data):
        self.data = data
    
    def draw(self,surface):
        self.surface.fill(self.bg_color)
        text = self.font.render(str(self.data),1,(0,0,0))
        self.surface.blit(text,(0,0))
        surface.blit(self.surface,(0,480-20))

class Difficulty_Menu(Menu):
    def run_option(self,surface,player):
        player.difficulty = (self.cursor+1)*10
        self.active = 0

