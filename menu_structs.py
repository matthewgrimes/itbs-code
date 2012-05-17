#!/usr/bin/env python

import pygame, utils, map_structs
from pygame.locals import *

class Menu:
    def __init__(self):
        self.active = 0

class YN_Prompt(Menu):
    def __init__(self):
        self.active = 0
        self.canvas = pygame.Surface((105,85))
        self.canvas.fill((0,0,250))
        pygame.draw.rect(self.canvas,(255,215,0),((0,0),(105,85)),5)
        self.canvas.set_alpha(120)
        self.pos = [800-self.canvas.get_width(),450-self.canvas.get_height()]
        self.options = ["Yes","No"]
        self.option = 0
        self.font = pygame.font.Font(None,36)

    def Draw(self,canvas):
        pos = [(800-self.canvas.get_width())/2,(450-self.canvas.get_height())/2]

        canvas.blit(self.canvas,pos)
        color = (250,250,250)
        for index,o in enumerate(self.options):
            text = self.font.render(o,1,color)
            [text_x,text_y]=[pos[0]+20,pos[1]+20+index*35]
            canvas.blit(text,[text_x,text_y])
#       Selected Icon
        pygame.draw.circle(canvas,(0,250,0),[pos[0]+10,pos[1]+30+self.option*35],10)


    def Activate(self,actor,current_map,cursor,actors):      
        self.active = 1
#       Slide the Menu onto the screen
        self.option = 0

        
    def Handle_Input(self,events):
            #canvas = background
            for event in events:
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        self.active = 0    
                    if event.key==K_DOWN:
                        self.option=(self.option+1)%len(self.options)
                    if event.key==K_UP:
                        self.option=(self.option-1)%len(self.options)

                    if event.key==K_SPACE:
                        if self.option==0: return 1
                        else: return 0

    def Draw_Map(self,canvas,current_map,cursor,actors):
            current_map.Draw(canvas,[cursor],actors)
            self.Draw(canvas)



class Menu_Move(Menu):

    def Activate(self,actor,current_map,cursor,actors):
        self.cursors = [cursor]
        self.openList,self.ancestry = utils.draw_circle(actor,current_map,actors,actor.character.speed)
        for spot in self.openList:
            cursor = map_structs.Blue_Cursor(80,2,[])
            [cursor.pos[0],cursor.pos[1]] = spot
            self.cursors.insert(0,cursor)
        self.active = 1
        self.actor = actor

    def Handle_Input(self,events):
        for event in events:
            if event.type==KEYDOWN and not self.actor.moving:
                old_pos_x,old_pos_y = self.cursors[-1].pos
                if event.key==K_ESCAPE:
                    self.active = 0
                    return ['turn']
                if event.key==K_SPACE:
                    #if YN_Prompt().Activate(canvas,screen,current_map,cursor,self.actors)==1:

                    self.actor.moved = 1
                    self.actor.Create_Move_Path(self.cursors[-1].pos,self.ancestry)
                    self.actor.mov_vector.remove(self.actor.mov_vector[0])
                    self.actor.moving = 1
                    self.active = 0
                    return ['animating','turn']
                if event.key==K_RIGHT:
                    self.cursors[-1].Move('right')
                if event.key==K_LEFT:
                    self.cursors[-1].Move('left')
                if event.key==K_DOWN:
                    self.cursors[-1].Move('down')
                if event.key==K_UP:
                    self.cursors[-1].Move('up')
                if self.cursors[-1].pos not in self.openList: self.cursors[-1].pos = [old_pos_x,old_pos_y]

    def Draw_Map(self,canvas,current_map,cursor,actors):
            if self.actor.moving: current_map.Draw(canvas,[self.cursors[-1]],actors)
            else: current_map.Draw(canvas,self.cursors,actors)

class Player_Turn:
    def __init__(self):
        self.active = 0
        self.activating = 0
        self.activate_count = 0
        self.canvas = pygame.Surface((205,155))
        self.canvas.fill((0,0,250))
        pygame.draw.rect(self.canvas,(250,0,0),((0,10),(5,150)),5)

        pygame.draw.rect(self.canvas,(255,215,0),((0,0),(255,5)),5)
        pygame.draw.rect(self.canvas,(255,215,0),((0,150),(255,5)),5)
        self.canvas.set_alpha(120)
        self.canvas.set_colorkey((250,0,0))
        self.pos = [800-self.canvas.get_width(),450-self.canvas.get_height()]
        self.options = ["Move","Fight","Done","Back"]
        self.available_options = [1,0,1,1]
        self.option = 0
        self.font = pygame.font.Font(None,36)

    def Draw(self,canvas,pos):
        available_color = (250,250,250)
        unavailable_color = (50,50,50)
        if self.activating == 1:
            pos[0]-=self.canvas.get_width()/5
            self.activate_count-=1
            if self.activate_count==0:
                self.activating = 0
        canvas.blit(self.canvas,pos)
        for index,o in enumerate(self.options):
            if self.available_options[index]==1:
                color = available_color
            else: color = unavailable_color
            text = self.font.render(o,1,color)
            [text_x,text_y]=[pos[0]+20,pos[1]+15+index*35]
            canvas.blit(text,[text_x,text_y])
#       Selected Icon
        pygame.draw.circle(canvas,(0,250,0),[pos[0]+10,pos[1]+30+self.option*35],10)

    def Show(self,canvas,screen):
        for i in range(1,self.canvas.get_width(),10):
            background = canvas
            self.Draw(background,[self.pos[0]+self.canvas.get_width()-i,self.pos[1]])
            screen.blit(background,[0,0])
            pygame.display.flip()

    def Hide(self,canvas,screen):
        background = canvas
        for i in range(1,self.canvas.get_width(),10):
            background = canvas
            self.Draw(background,[self.pos[0]+i,self.pos[1]])
            screen.blit(background,[0,0])
            pygame.display.flip()


    def Activate(self,actor,current_map,cursor,actors):
        self.active = 1
        self.activating = 1
        self.activate_count = 5
        self.pos[0] = self.pos[0]+self.canvas.get_width()
        self.available_options=[(not actor.moved) and actor.can_move,
                (not actor.attacked) and actor.can_attack,1,1]
        self.option = 0
	while self.available_options[self.option]==0:
	    self.option = (self.option+1)%len(self.available_options)
        
    def Handle_Input(self,events):
        for event in events:
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    self.active = 0
                    return ['back']
                if event.key==K_DOWN:
                    self.option=(self.option+1)%len(self.options)
                    while self.available_options[self.option]==0:
                        self.option=(self.option+1)%len(self.options)
                if event.key==K_UP:
                    self.option=(self.option-1)%len(self.options)
                    while self.available_options[self.option]==0:
                        self.option=(self.option-1)%len(self.options)

                if event.key==K_SPACE:
                    if self.option==0:
                        #if Menu_Move().Activate(self,canvas,screen,current_map,cursor,actors)==1:
                        self.available_options[0]=0
                        self.option+=1
                        self.active = 0
                        return ['move']
                        #self.Show(canvas,screen)

                    elif self.option==1:
                            self.available_options[1]=0
                            self.option+=1
                            self.active = 0
                            return ['attack']

                    elif self.option==2:
                        self.active = 0
                        return ['done_with_turn']
                    elif self.option==3:
                        self.active = 0
                        return ['back']
            else: return []


    def Draw_Map(self,canvas,current_map,cursor,actors):
        current_map.Draw(canvas,[cursor],actors)
        self.Draw(canvas,self.pos)

class Player_Attack(Menu):

    def Activate(self,actor,current_map,cursor,actors):
        self.actor = actor
        self.actors = actors
        self.actor_positions = []
        for a in actors:
            self.actor_positions.append(a.pos)
        self.cursors = [cursor]
        if actor.character.e_weapon.attack_range==1:
            self.openList,self.ancestry = utils.draw_circle(actor,current_map,actors,2,1)
            closedList = []
        else:
            self.openList,self.ancestry = utils.draw_circle(actor,current_map,actors,actor.character.e_weapon.attack_range[1],1)
            closedList,c_ancestry = utils.draw_circle(actor,current_map,actors,actor.character.e_weapon.attack_range[0],1)
        for spot in range(1,len(self.openList)):
            if not (self.openList[spot] in closedList):
                cursor = map_structs.Red_Cursor(80,2,[])
                [cursor.pos[0],cursor.pos[1]] = self.openList[spot]
                self.cursors.insert(0,cursor)
        

        self.active = 1
    def Handle_Input(self,events):
            for event in events:
                if event.type==KEYDOWN:
                    old_pos_x,old_pos_y = self.cursors[-1].pos
                    if event.key==K_ESCAPE:
                        self.active = 0
                        return ['turn']
                    if event.key==K_SPACE and self.cursors[-1].pos in self.openList:
                        # Get Target
                        for a in self.actors:
                            if a.pos==self.cursors[-1].pos and a!=self.actor:
                                    self.actors[self.actors.index(a)].character.current_hp-=2
                                    self.actor.attacked = 1
                                    self.actor.moved = 1
                                    self.active = 0
                                    return ['turn']
                    if event.key==K_RIGHT:
                        if self.cursors[-1].pos==self.actor.pos: self.actor.facing = 'se'
                        self.cursors[-1].Move('right')
                    if event.key==K_LEFT:
                        if self.cursors[-1].pos==self.actor.pos: self.actor.facing = 'nw'
                        self.cursors[-1].Move('left')
                    if event.key==K_DOWN:
                        if self.cursors[-1].pos==self.actor.pos: self.actor.facing = 'sw'
                        self.cursors[-1].Move('down')
                    if event.key==K_UP:
                        if self.cursors[-1].pos==self.actor.pos: self.actor.facing = 'ne'
                        self.cursors[-1].Move('up')
                    #if self.cursors[-1].pos not in self.openList: self.cursors[-1].pos = [old_pos_x,old_pos_y]

    def Draw_Map(self,canvas,current_map,cursor,actors):
         current_map.Draw(canvas,self.cursors,actors)
         self.actor.Display_Info(canvas)
         if self.cursors[-1].pos in self.actor_positions:
             actors[self.actor_positions.index(self.cursors[-1].pos)].Display_Info(canvas,[800,300],1)

