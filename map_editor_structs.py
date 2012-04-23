import pygame, sys, random, itertools, math
from pygame.locals import *
from utils import load_image
class Tile:
    def __init__(self,image,water=0):
        self.image,self.rect = load_image(image,-1)
        if water:
            self.image.set_alpha(180)
        self.sides = [pygame.Surface((40,40))]
        if water==0:
            color_left = (139,69,19)
            color_right = (92,51,23)
        else:
            color_left = (0,0,250)
            color_right = (0,0,150)
        pygame.draw.polygon(self.sides[0],color_left,((0,0),(40,20),(40,40),(0,20)))
        self.sides[0].set_colorkey((0,0,0))
        self.sides[0].set_alpha(255-water*175)
        
        self.sides.append(pygame.Surface((40,40)))
        pygame.draw.polygon(self.sides[1],color_right,((0,0),(40,20),(40,40),(0,20)))
        self.sides[1].set_colorkey((0,0,0))
        self.sides[1].set_alpha(255-water*175)

class Object:
    def __init__(self, image):
        self.image,self.rect = load_image(image,-1)

    def Draw(self,surface,loc):
        x=loc[0]
        y=loc[1]-self.image.get_height()
        surface.blit(self.image,[x,y])

class Map:
    def __init__(self, size,layout,ratio,tile_size):
        self.size = size
        self.layout = layout
        self.tiles = [Tile('cobblestone.png'),Tile('grass.png'),Tile('water.png',1),Tile('dungeon.png'),Tile('dirt.png')]
        self.objects = [Object('tree.png'),Object('log.png')]
        self.ratio = ratio
        self.tile_size = tile_size
        self.active_level = 1


        width = 800
        height = 450
        self.pos = [(width-tile_size*(self.size[0]+1))/2,
                (height-tile_size/(2*ratio)*self.size[1])/2+50]

    def Update(self,cursor):
        top_left = self.pos
        x=cursor.pos[0]*self.tile_size+top_left[0]
        y=cursor.pos[1]*self.tile_size/self.ratio+top_left[1]-self.tile_size/(2*self.ratio)#*level
        x = x+self.tile_size/2*(cursor.pos[1]%2)
        y = y-self.tile_size/(2*self.ratio)*(cursor.pos[1]+1)

        if x<0:
            self.pos[0] = self.pos[0] + self.tile_size
        if y<0:
            self.pos[1] = self.pos[1] + self.tile_size

        if x>800-self.tile_size*2:
            self.pos[0] = self.pos[0] - self.tile_size

        if y>450-self.tile_size/2:
            self.pos[1] = self.pos[1] - self.tile_size

#        if y+self.tile_size/2*(cursor.pos[1]+1)<self.tile_size:
#            self.pos[1] = self.pos[1] + self.tile_size+self.tile_size/2*(cursor.pos[1]+1)

#        if y+self.tile_size/2*(cursor.pos[1]%2)>=800:
#            self.pos[1] = self.pos[1] - self.tile_size/2*(cursor.pos[1]%2)
#,y-tile_size/(2*ratio)*(cursor.pos[1]+1)]

    def Draw(self,surface,cursor):
        self.Update(cursor)
        width = surface.get_width()
        height = surface.get_height()
        tile_size = self.tile_size
        ratio = self.ratio 
        top_left = self.pos
        font = pygame.font.Font(None,16)


        for level in range(1,self.layout[0]+1):
           
            for j in range(0, self.size[1]):
                for i in range(0, self.size[0]):
                    x=i*tile_size+top_left[0]
                    y=j*tile_size/ratio+top_left[1]-tile_size/(2*ratio)*level

                    if self.layout[level][i + j * self.size[0]]!=-1:
                        surface.blit(self.tiles[self.layout[level][i+j*self.size[0]]].image,
                                                [x+tile_size/2*(j%2),y-tile_size/(2*ratio)*(j+1)])
                        # Draw Left Side
                        surface.blit(self.tiles[self.layout[level][i+j*self.size[0]]].sides[0],
                                                [x+tile_size/2*(j%2),y-tile_size/(2*ratio)*(j)])
                        # Draw Right Side
                        surface.blit(pygame.transform.flip(self.tiles[self.layout[level][i+j*self.size[0]]].sides[1],0,1),
                                                [x+tile_size/2*(j%2)+tile_size/2,y-tile_size/(2*ratio)*(j)])
                        # Draw Objects
                        if self.layout[-1][i + j * self.size[0]]!=-1 and (self.layout[level+1][i + j * self.size[0]]==-1 or level==self.layout[0]):
                                
                            self.objects[self.layout[-1][i + j * self.size[0]]].Draw(surface,
                            [x+tile_size/2*(j%2),y-tile_size/(2*ratio)*(j)+tile_size/(4*ratio)])


                        # Draw Cursor
                    if [i,j]==cursor.pos:# and  (self.layout[level+1][i + j * self.size[0]]==-1 or level==self.layout[0]):
                            cursor.Draw(surface,[x+tile_size/2*(j%2),y-tile_size/(2*ratio)*(j+1)])
                
                    if level==self.active_level:
                        self.Draw_Grid(surface,(x+tile_size/2*(j%2),y-tile_size/(2*ratio)*(j)),tile_size,ratio)
                        text = font.render('('+str(i)+','+str(j)+')',1,(250,0,0))
                        surface.blit(text,(x+tile_size/2*(j%2)+30,y-tile_size/(2*ratio)*(j)))


    def Draw_Grid(self,surface,loc,width,ratio):
        color = (250,250,250)
        pygame.draw.line(surface,color, loc, (loc[0]+width/2,loc[1]-width/(2*ratio)))
        pygame.draw.line(surface,color, loc, (loc[0]+width/2,loc[1]+width/(2*ratio)))
        pygame.draw.line(surface,color,(loc[0]+width,loc[1]), (loc[0]+width/2,loc[1]-width/(2*ratio)))
        pygame.draw.line(surface,color,(loc[0]+width,loc[1]), (loc[0]+width/2,loc[1]+width/(2*ratio)))


class Cursor:
    def __init__(self,color,width,ratio,layout):
        self.color = color
        self.pos = [0,0]
        #self.surface = pygame.Surface((width,width/ratio))
        #self.surface.set_colorkey((0,0,0))
        #self.surface.set_alpha(220)
        self.layout = layout
        self.flash_count = 0
        #pygame.draw.polygon(self.surface,(0,128,0),(
        #    (2,width/(2*ratio)),
        #    (width/2,0),
        #    (width-2,width/(2*ratio)-2),
        #    (width/2-2,width/ratio-2)))
        #pygame.draw.polygon(self.surface,self.color,((8,width/(2*ratio)),
        #                                             (width/2,4),
        #                                             (width-8,width/(2*ratio)),
        #                                             (width/2,width/ratio-5)))
        self.surface,self.rect = load_image('cursor.png',-1)
        

    def Draw(self,surface,pos):
        self.flash_count=(self.flash_count+1)%140
        self.surface.set_alpha(105+35*math.cos(self.flash_count*2*3.14159/140))
        surface.blit(self.surface,pos)

    def Move(self,direction):
        old_pos_x,old_pos_y = self.pos
        if direction=='right':
            self.pos[1]+=1
            if self.pos[1]%2==0:
                self.pos[0]+=1
        if direction=='left':
            self.pos[1]-=1
            if self.pos[1]%2!=0:
                self.pos[0]-=1
        if direction=='down':
            self.pos[1]+=1
            if self.pos[1]%2!=0:
                self.pos[0]-=1
        if direction=='up':
            self.pos[1]-=1
            if self.pos[1]%2==0:
                self.pos[0]+=1
        if self.pos[0] + self.layout[1][0]*self.pos[1] > len(self.layout[0]) or self.pos[0]>=self.layout[1][0] or self.pos[1]>=self.layout[1][1]: self.pos = [old_pos_x,old_pos_y]
        elif self.pos[0]<0 or self.pos[1]<0: self.pos=[old_pos_x,old_pos_y]
        
        
