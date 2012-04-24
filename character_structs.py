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
        self.image,self.rect = load_image(image,-1)
        self.pos = [3,3]
        self.level = 1
        self.mov_vector=[]
        self.moved = 0
        self.attacked = 0
        self.can_move = 1
        self.can_attack = 1
        self.character = Character(stats)
        self.font = pygame.font.Font(None, 30)


#       Displaying stats
        width = 400
        height = 150
        color = (0,0,250)
        self.info = pygame.Surface((width-height/2,height))
        pygame.draw.rect(self.info,color,(0,0,width-height,height))
        pygame.draw.circle(self.info,color,(width-height,height/2),height/2)
        self.info.set_colorkey((0,0,0))
        self.info.set_alpha(180)



    def NewTurn(self):
        self.moved = 0
        self.attacked = 0


    def Draw(self,surface,loc):
        tile_width = 80
        tile_height = 40

        x = loc[0]+tile_width/2-self.image.get_width()/2+tile_width/2*(self.pos[1]%2)
        y = loc[1]-tile_height/2*self.pos[1]-self.image.get_height()+10
        surface.blit(self.image,[x,y])

    def Move(self):
        if self.mov_vector!=[]:
            self.pos = self.mov_vector=[0]
            self.mov_vector.remove(self.move_vector[0])

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
            canvas.blit(text, loc)
            text = self.font.render("MP:"+str(self.character.current_mp)+"/"+str(self.character.mp),1,(250,250,250))
            canvas.blit(text,[loc[0],loc[1]+20])





class Job:
    def __init__(self):
        pass

class Knight(Job):
    def __init__(self):
        self.image_sw,self.rect_sw = load_image('Knight5m-SW.gif',-1)
