import pygame, sys, random, itertools,map_structs
from pygame.locals import *
from utils import load_image
class Character:
    def __init__(self,stats):
        self.hp = stats['hp']
        self.mp = stats['mp']
        self.speed = stats['speed']
        self.current_hp = self.hp
        self.current_mp = 0

class Actor:
    def __init__(self, image,stats):
        images,rects = load_image(image,-1)
#        self.image,self.rect = load_image(image,-1)
        self.pos = [3,3]
        self.level = 1
        self.mov_vector=[]
        self.moved = 0
        self.attacked = 0
        self.can_move = 1
        self.can_attack = 1
        self.character = Character(stats)
        self.font = pygame.font.Font(None, 30)
        self.facing = 'se'
        self.animate_count = 0
        self.animate_order = [0,1,2,1]
        self.animate_timer = 0
        self.images=[]
        rect = pygame.Rect(((0,0),(32,60)))
        for j in range(0,2):
            for i in range(0,3):
                image = pygame.Surface((32,60))
                image.fill((255,0,241))
                image.blit(images,(0,0),rect.move([32*i,60*j]))

                image.set_colorkey((255,0,241))
                image = image.convert()
                self.images.append(image)
#        2
#   3  
#           1
#     0
#


#       Displaying stats
        width = 400
        height = 150
        color = (0,0,250)
        self.info = pygame.Surface((width-height/2,height))
        pygame.draw.rect(self.info,color,(0,0,width-height,height))
        pygame.draw.circle(self.info,color,(width-height,height/2),height/2)
        self.info.set_colorkey((0,0,0))
        self.info.set_alpha(180)
        self.offset=[0,0]



    def NewTurn(self):
        self.moved = 0
        self.attacked = 0


    def Draw(self,surface,loc):
        tile_width = 80
        tile_height = 40
        self.animate_timer+=1
        if self.animate_timer==7:
            self.animate_count = (self.animate_count+1)%4
            self.animate_timer=0

        x = loc[0]+tile_width/2-self.images[0].get_width()/2+tile_width/2*(self.pos[1]%2)+self.offset[0]
        y = loc[1]-tile_height/2*self.pos[1]-self.images[0].get_height()+10+self.offset[1]
        surface.blit(pygame.transform.flip(self.images[self.animate_order[self.animate_count]+3*(self.facing[0]=='n')],(self.facing=='ne' or self.facing=='se'),0),[x,y])

    def Move(self,new_pos,ancestry):
        self.mov_vector=[new_pos]
        while self.mov_vector[0]!=self.pos :
        #  Look for parent of oldest position
            for i in range(0,len(ancestry)):
                if ancestry[i][0]==self.mov_vector[0]:
                    self.mov_vector.insert(0,ancestry[i][1])
                    break


    def Display_Info(self,canvas,loc=[0,300],mirrored=0):
        #print self.character.hp,self.character.mp,self.character.speed
        if mirrored==0:
            canvas.blit(self.info,loc)
            text = self.font.render("HP:"+str(self.character.current_hp)+"/"+str(self.character.hp),1,(250,250,250))
            canvas.blit(text, loc)
            text = self.font.render("MP:"+str(self.character.current_mp)+"/"+str(self.character.mp),1,(250,250,250))
            canvas.blit(text,[loc[0],loc[1]+20])
        else:
            loc[0] = loc[0]-self.info.get_width()
            canvas.blit(pygame.transform.flip(self.info,1,0),loc)
            text = self.font.render("HP:"+str(self.character.current_hp)+"/"+str(self.character.hp),1,(250,250,250))
            canvas.blit(text, [loc[0]+50,loc[1]])
            text = self.font.render("MP:"+str(self.character.current_mp)+"/"+str(self.character.mp),1,(250,250,250))
            canvas.blit(text,[loc[0]+50,loc[1]+20])





class Job:
    def __init__(self):
        pass

class Knight(Job):
    def __init__(self):
        self.image_sw,self.rect_sw = load_image('Knight5m-SW.gif',-1)
