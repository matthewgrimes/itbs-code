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
    import map_structs
    import character_structs
    import menu_structs
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

tile_size = 80
map_size = [16,16]
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
        f = open('maps/testmap002.map','r')
        demo_map = pickle.load(f)
        f.close()
        self.maps=[map_structs.Map(map_size,demo_map,ISO_RATIO,tile_size)]
        self.cursor = map_structs.Cursor((0,250,0),tile_size,2,
                [demo_map[1],map_size])
        self.actors=[#character_structs.Actor('characters/Knight5M-SW.gif',{'hp':15,'mp':8,'speed':2}),
                character_structs.Actor('characters/assassin.png',{'name':'Assassin','hp':12,'mp':10,'speed':4,'agility':3},1),
                character_structs.Actor('characters/sniper.png',{'hp':12,'mp':10,'speed':5,'agility':2,'name':'Sniper'},2)
                ]
        self.actors[0].pos=[4,3]

        self.menus=[menu_structs.Menu_Move()]

    def run(self):
            turn = 0
            # Keep Track of current player
            turn_list=[]
            while 1:
                 # Create Turn List
                if turn_list==[]:
                    turn+=1
                    turn_list = utils.sort_actors(self.actors)
                    [self.cursor.pos[0],self.cursor.pos[1]]=self.actors[turn_list[0]].pos
                    for actor in self.actors:
                        actor.NewTurn()
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
                            [self.cursor.pos[0],self.cursor.pos[1]]=self.actors[turn_list[0]].pos
                        if event.key==K_SPACE:
                            for actor in self.actors:
                                if self.cursor.pos==actor.pos:
                                    try:
                                        if actor==self.actors[turn_list[0]]:
                                        #menu_structs.Menu_Move().Activate(actor,self.canvas,self.screen,self.maps[0],self.cursor,self.actors)
                                            if menu_structs.Player_Turn().Activate(actor,self.canvas,self.screen,
                                                                                self.maps[0],self.cursor,self.actors)==1:
                                                turn_list.remove(turn_list[0])
                                                try: [self.cursor.pos[0],self.cursor.pos[1]]=self.actors[turn_list[0]].pos
                                                except IndexError: pass
                                            break
                                    except IndexError: 
                                        turn_list = []
                           
                self.canvas.fill((0,0,0))
                self.maps[0].Draw(self.canvas,[self.cursor],self.actors)
                text=pygame.font.Font(None,36).render('Turn '+str(turn),1,(250,250,250))
                self.canvas.blit(text,(700,0))
                self.screen.blit(self.canvas,[0,0])
                pygame.display.flip()




if __name__ == '__main__':
    game = MainGame((800,450))
    game.run()
