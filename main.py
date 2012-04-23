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
    from socket import *
    from pygame.locals import *
    import map_structs
    import character_structs
    import menu_structs
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

demo_map = [4, # number of levels
    # level 0
    [-1,-1,-1,1,0,0,0,0,
     -1,-1, 1,0,0,0,0,0,
     -1,-1, 1,0,0,0,0,0,
     -1, 1, 0,0,0,0,0,0,
     -1, 1, 0,0,0,0,0,0,
      1, 0, 0,0,0,0,0,0,
      1, 0, 0,0,3,2,0,0,
      0, 0, 0,0,2,2,0,1,
     
     -1,-1,-1,1,0,0,0,0,
     -1,-1, 1,0,0,0,0,0,
     -1,-1, 1,0,0,0,0,0,
     -1, 1, 0,0,0,0,0,0,
     -1, 1, 0,0,0,0,0,0,
      1, 0, 0,0,0,0,0,0,
      1, 0, 0,0,0,2,0,0,
      0, 0, 0,0,2,2,0,1,
     ],
    # level 1
    [-1,-1,-1, 1,-1,-1,-1,-1,
     -1,-1, 1,-1,-1,-1,-1,-1,
     -1,-1, 1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,1,-1,-1,
     -1,-1,-1,-1,0,0,-1,-1,
     -1,-1,-1,-1,0,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,

     -1,-1,-1, 1,-1,-1,-1,-1,
     -1,-1, 1,-1,-1,-1,-1,-1,
     -1,-1, 1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,1,-1,-1,
     -1,-1,-1,-1,0,0,-1,-1,
     -1,-1,-1,-1,0,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1],
    # level 2
    [-1,-1,-1, 1,-1,-1,-1,-1,
     -1,-1, 1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,

     -1,-1,-1, 1,-1,-1,-1,-1,
     -1,-1, 1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1],
    # level 3
    [-1,-1,-1, 1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,

     -1,-1,-1, 1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1],
    # objects
    [0,-1,-1,-1,-1,-1,-1,-1,
     -1,0,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1, 0,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
      1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,

     0,-1,-1,-1,-1,-1,-1,-1,
     -1,0,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1, 0,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1,
     -1,-1,-1,-1,-1,-1,-1,-1],
    ]
tile_size = 80
map_size = [8,16]
ISO_RATIO = 2
class MainGame:
    def __init__(self,size):
        self.size = size
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.canvas = pygame.Surface(self.size)
        # Set Background to White
        self.canvas.fill((250,250,250))
        self.maps=[map_structs.Map(map_size,demo_map,ISO_RATIO,tile_size)]
        self.cursor = map_structs.Cursor((0,250,0),tile_size,2,
                [demo_map[1],map_size])
        self.actors=[character_structs.Actor('characters/Knight5M-SW.gif'),character_structs.Actor('mario.png')]

        self.menus=[menu_structs.Menu_Move()]

    def run(self):
            # Keep Track of current player
            current_actor = 0
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
                        if event.key==K_a:
                            [self.cursor.pos[0],self.cursor.pos[1]]=self.actors[current_actor].pos
                        if event.key==K_SPACE:
                            for actor in self.actors:
                                if self.cursor.pos==actor.pos:
                                    if actor==self.actors[current_actor]:
                                        #menu_structs.Menu_Move().Activate(actor,self.canvas,self.screen,self.maps[0],self.cursor,self.actors)
                                        if menu_structs.Player_Turn().Activate(actor,self.canvas,self.screen,
                                                                                self.maps[0],self.cursor,self.actors)==1:
                                            current_actor=(current_actor+1)%len(self.actors)
                                            [self.cursor.pos[0],self.cursor.pos[1]]=self.actors[current_actor].pos
                                        break
                           
                self.canvas.fill((0,0,0))
                self.maps[0].Draw(self.canvas,[self.cursor],self.actors)
                self.screen.blit(self.canvas,[0,0])
                pygame.display.flip()




if __name__ == '__main__':
    game = MainGame((800,450))
    game.run()
