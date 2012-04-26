#!/usr/bin/env python

VERSION = "0.4"

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import utils
    import pickle
    from socket import *
    from pygame.locals import *
    import map_editor_structs
    import character_structs
    import menu_structs
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

empty_map = [8, # number of levels
    # level0
    [
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
     
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
     ],
    # level 1
    [
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,

   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1],
    # level 2
    [
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,

   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1],
    # level 3
    [
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,

   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1],
    # objects
    [
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,

   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1,
   -1, -1, -1, -1, -1, -1, -1, -1],
    ]
tile_size = 80
map_size = [16,26]
ISO_RATIO = 2
class MainGame:
    def __init__(self,size,input_map=0):
        # Generate Empty Map
        self.empty_map=[5]
        for lev in range(0,5+1):
            level = []
            for j in range(0,map_size[1]):
                for i in range(0,map_size[0]):
                    level.append(-1)
            self.empty_map.append(level)
        if input_map!=0:
            f = open(input_map,'r')
            self.empty_map = pickle.load(f)
            f.close()
        self.size = size
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.canvas = pygame.Surface(self.size)
        # Set Background to White
        self.canvas.fill((250,250,250))
        self.maps=[map_editor_structs.Map(map_size,self.empty_map,ISO_RATIO,tile_size)]
        self.cursor = map_editor_structs.Cursor((0,250,0),tile_size,2,
                [self.empty_map[1],map_size])
        self.font = pygame.font.Font(None,36)
        self.tiles = [map_editor_structs.Tile('cobblestone.png'),map_editor_structs.Tile('grass.png'),map_editor_structs.Tile('water.png',1),map_editor_structs.Tile('dungeon.png'),map_editor_structs.Tile('dirt.png')]
        self.objects = [map_editor_structs.Object('tree.png'),map_editor_structs.Object('log.png')]
        self.current_tile = 0
        self.current_object=0

    def run(self):
            while 1:
                self.clock.tick(60)
                for event in pygame.event.get():
                    if event.type==KEYDOWN:
                        if event.key==K_ESCAPE: sys.exit()
                        if event.key==K_RIGHT:
                            self.cursor.Move('right')
                        if event.key==K_LEFT:
                            self.cursor.Move('left')
                        if event.key==K_DOWN:
                            self.cursor.Move('down')
                        if event.key==K_UP:
                            self.cursor.Move('up')
                        if event.key==K_SPACE:
                            self.maps[0].active_level = (self.maps[0].active_level+1)%5
                            if self.maps[0].active_level==0: self.maps[0].active_level+=1
                        if event.key==K_TAB:
                            self.current_tile+=1
                            self.current_tile=self.current_tile%len(self.tiles)
                        if event.key==K_o:
                            self.current_object+=1
                            self.current_object=self.current_object%len(self.objects)
                        if event.key==K_RETURN:
                            self.maps[0].layout[self.maps[0].active_level][self.cursor.pos[0]+16*self.cursor.pos[1]]=self.current_tile
                        if event.key==K_s:
                            #print self.maps[0].layout
                            f = open('new.map','w')
                            pickle.dump(self.maps[0].layout,f)
                            f.close()
                        if event.key==K_SLASH:
                            self.maps[0].layout[-1][self.cursor.pos[0]+16*self.cursor.pos[1]]=self.current_object
                        if event.key==K_BACKSPACE:
                            self.maps[0].layout[self.maps[0].active_level][self.cursor.pos[0]+16*self.cursor.pos[1]]=-1
                            self.maps[0].layout[-1][self.cursor.pos[0]+16*self.cursor.pos[1]]=-1


                           
                self.canvas.fill((0,0,0))
                self.maps[0].Draw(self.canvas,self.cursor)
                # Info
                text=self.font.render('Current level:'+str(self.maps[0].active_level),1,(250,250,250))
                self.canvas.blit(text,[0,0])
                text=self.font.render('Current tile:',1,(250,250,250))
                self.canvas.blit(text,[0,20])
                self.canvas.blit(self.tiles[self.current_tile].image,[150,20])
                text=self.font.render('Current Object:',1,(250,250,250))
                self.canvas.blit(text,[200,0])
                self.objects[self.current_object].Draw(self.canvas,[400,50])


                self.screen.blit(self.canvas,[0,0])
                pygame.display.flip()




if __name__ == '__main__':
    if len(sys.argv)<=1:
        game = MainGame((800,450))
    elif len(sys.argv)>1:
        game = MainGame((800,450),str(sys.argv[1]))
    print str(sys.argv[0])
    game.run()

