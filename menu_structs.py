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


    def Activate(self,canvas,screen,current_map,cursor,actors):      
        self.active = 1
#       Slide the Menu onto the screen
        background = canvas
        self.option = 0

        
        while 1:
            #canvas = background
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        return 0
                    if event.key==K_DOWN:
                        self.option=(self.option+1)%len(self.options)
                    if event.key==K_UP:
                        self.option=(self.option-1)%len(self.options)

                    if event.key==K_SPACE:
                        if self.option==0: return 1
                        else: return 0

            #current_map.Draw(canvas,[cursor],actors)
            canvas.blit(background,(0,0)) 
            self.Draw(canvas)
            screen.blit(canvas,[0,0])
            pygame.display.flip()



class Menu_Move(Menu):

    def Activate(self,actor,canvas,screen,current_map,cursor,actors):
        OpenList = [actor.pos]
        cursors = [cursor]
        openList,ancestry = utils.draw_circle(actor,current_map,actors,3)
        for spot in openList:
            cursor = map_structs.Blue_Cursor(80,2,[])
            [cursor.pos[0],cursor.pos[1]] = spot
            cursors.insert(0,cursor)
#        for spot in ['up','down','left','right']:
#            cursor = map_structs.Blue_Cursor(80,2,[])
#            [cursor.pos[0],cursor.pos[1]]=cursors[-1].pos
#            cursor.pos = utils.move_in_coords(cursor.pos,spot,
#                [current_map.layout,[8,16]])
#            if utils.check_for_water(current_map,cursor.pos)==0:
#                cursors.insert(0,cursor)
#                openList.append(cursor.pos)

        self.active = 1
        choosing_facing = 0
        moving = 0
        while 1:
            if moving==1 and actor.mov_vector==[]:
                moving = 0
                choosing_facing = 1
            for event in pygame.event.get():
                if event.type==KEYDOWN and not moving:
                    old_pos_x,old_pos_y = cursors[-1].pos
                    if event.key==K_ESCAPE:
                        self.active = 0
                        return 0
                    if event.key==K_SPACE:
                        if not choosing_facing:
                            if YN_Prompt().Activate(canvas,screen,current_map,cursor,actors)==1:
                                #[actor.pos[0],actor.pos[1]] = cursors[-1].pos
                                #actor.level = 1
                                # Get Appropriate Level
                                #for level in range(1,current_map.layout[0]):
                                #    if current_map.layout[level+1][actor.pos[0]+current_map.size[0]*actor.pos[1]]!=-1:
                                #        actor.level+=1
                                actor.moved = 1
                                actor.Move(cursors[-1].pos,ancestry)
                                moving = 1
                        else:
                            return 1
                    if event.key==K_RIGHT:
                        if choosing_facing: actor.facing = 'se'
                        else: cursors[-1].Move('right')
                    if event.key==K_LEFT:
                        if choosing_facing: actor.facing = 'nw'
                        else: cursors[-1].Move('left')
                    if event.key==K_DOWN:
                        if choosing_facing: actor.facing = 'sw'
                        else: cursors[-1].Move('down')
                    if event.key==K_UP:
                        if choosing_facing: actor.facing = 'ne'
                        else: cursors[-1].Move('up')
                    if cursors[-1].pos not in openList: cursors[-1].pos = [old_pos_x,old_pos_y]

            canvas.fill((0,0,0))
            if (not moving) and (not choosing_facing): current_map.Draw(canvas,cursors,actors)
            elif not moving: current_map.Draw(canvas,[cursors[-1]],actors)
            else: current_map.Draw(canvas,[cursors[-1]],actors)
            screen.blit(canvas,[0,0])
            pygame.display.flip()

class Player_Turn:
    def __init__(self):
        self.active = 0
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
        canvas.blit(self.canvas,pos)
        available_color = (250,250,250)
        unavailable_color = (50,50,50)
        for index,o in enumerate(self.options):
            if self.available_options[index]==1:
                color = available_color
            else: color = unavailable_color
            text = self.font.render(o,1,color)
            [text_x,text_y]=[pos[0]+20,pos[1]+20+index*35]
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


    def Activate(self,actor,canvas,screen,current_map,cursor,actors):
        actor.Display_Info(canvas)
        self.active = 1
#       Slide the Menu onto the screen
        background = canvas
        self.available_options=[(not actor.moved) and actor.can_move,
                (not actor.attacked) and actor.can_attack,1,1]
        self.option = 0
        while self.available_options[self.option]==0:
            self.option = (self.option+1)%len(self.options)

        self.Show(canvas,screen)
        
        while 1:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        return
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
                            if Menu_Move().Activate(actor,canvas,screen,current_map,cursor,actors)==1:
                                self.available_options[0]=0
                                self.option+=1
                            self.Show(canvas,screen)

                        elif self.option==1:
                            if Player_Attack().Activate(actor,canvas,screen,current_map,cursor,actors)==1:
                                self.available_options[1]=0
                                self.option+=1

                        elif self.option==2:
                                return 1
                        elif self.option==3:
                            return 0



            canvas.fill((0,0,0))
            current_map.Draw(canvas,[cursor],actors)
            actor.Display_Info(canvas)
            self.Draw(canvas,self.pos)
            screen.blit(canvas,[0,0])
            pygame.display.flip()

    
        #Menu_Move().Activate(actor,canvas,screen,current_map,cursor,actors)



class Player_Attack(Menu):

    def Activate(self,actor,canvas,screen,current_map,cursor,actors):
        actor_positions = []
        for a in actors:
            actor_positions.append(a.pos)
        OpenList = [actor.pos]
        cursors = [cursor]
        openList,ancestry = utils.draw_circle(actor,current_map,actors,2,1)
                                                   #radius=1,people ok
        for spot in range(1,len(openList)):
            cursor = map_structs.Red_Cursor(80,2,[])
            [cursor.pos[0],cursor.pos[1]] = openList[spot]
            cursors.insert(0,cursor)
#        for spot in ['up','down','left','right']:
#            cursor = map_structs.Blue_Cursor(80,2,[])
#            [cursor.pos[0],cursor.pos[1]]=cursors[-1].pos
#            cursor.pos = utils.move_in_coords(cursor.pos,spot,
#                [current_map.layout,[8,16]])
#            if utils.check_for_water(current_map,cursor.pos)==0:
#                cursors.insert(0,cursor)
#                openList.append(cursor.pos)

        self.active = 1
        while 1:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    old_pos_x,old_pos_y = cursors[-1].pos
                    if event.key==K_ESCAPE:
                        self.active = 0
                        return 0
                    if event.key==K_SPACE:
                        # Get Target
                        for a in actors:
                            if a.pos==cursors[-1].pos and a!=actor:
                                if YN_Prompt().Activate(canvas,screen,current_map,cursor,actors)==1:
                                    actors[actors.index(a)].character.current_hp-=2
                                    actor.attacked = 1
                                    self.active = 0
                                    return 1
                    if event.key==K_RIGHT:
                        cursors[-1].Move('right')
                    if event.key==K_LEFT:
                        cursors[-1].Move('left')
                    if event.key==K_DOWN:
                        cursors[-1].Move('down')
                    if event.key==K_UP:
                        cursors[-1].Move('up')
                    if cursors[-1].pos not in openList: cursors[-1].pos = [old_pos_x,old_pos_y]

            canvas.fill((0,0,0))
            current_map.Draw(canvas,cursors,actors)
            actor.Display_Info(canvas)
            if cursors[-1].pos in actor_positions:
                actors[actor_positions.index(cursors[-1].pos)].Display_Info(canvas,[800,300],1)
            screen.blit(canvas,[0,0])
            pygame.display.flip()

