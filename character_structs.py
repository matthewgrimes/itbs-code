import pygame, sys, random, itertools,map_structs
from pygame.locals import *
from utils import load_image

class Actor:
    def __init__(self, image):
        self.image,self.rect = load_image(image,-1)
        self.pos = [3,3]
        self.level = 1
        self.mov_vector=[]
        self.moved = 0
        self.attacked = 0
        self.can_move = 1
        self.can_attack = 1


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


class Job:
    def __init__(self):
        pass

class Knight(Job):
    def __init__(self):
        self.image_sw,self.rect_sw = load_image('Knight5m-SW.gif',-1)
