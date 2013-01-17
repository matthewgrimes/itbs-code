import pygame, sys, random, itertools,map_structs,utils,item_structs
from pygame.locals import *
from utils import load_image

class Character:
    def __init__(self,stats):
        self.name = stats['name']
        self.hp = stats['hp']
        self.mp = stats['mp']
        self.strength = stats['strength']
        self.speed = stats['speed']
        self.agility = stats['agility']
        self.current_hp = self.hp
        self.current_mp = 0
        self.e_weapon=item_structs.Weapon('hands','1','b')

    def Equip_Weapon(self,weapon):
        self.e_weapon = weapon

class Actor:
    def __init__(self, image,stats,team,pos):
        images,rects = load_image(image,-1)
#        self.image,self.rect = load_image(image,-1)
        self.team = team
        self.pos = [pos[0],pos[1]]
        self.level = pos[2]
        self.mov_vector=[]
        self.moved = 0
        self.attacked = 0
        self.can_move = 1
        self.can_attack = 1
        self.character = Character(stats)
        self.font = pygame.font.Font(None, 30)
#       Motion stuff
        self.facing = 'se'
        self.animate_count = 0
        self.animate_order = [0,1,2,1]
        self.images=[]
        self.move_t=0
        self.moving=0
        self.update_position=0
        self.level_difference = 0
        self.jumping = 0
        self.animation_clock = pygame.time.Clock()
        self.last_animated=pygame.time.get_ticks()
        self.animation_frame_time = 333
        self.movement_time = 33
        self.movement_last_updated = pygame.time.get_ticks()


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
        if self.team==1: color = (0,0,250)
        elif self.team==2: color = (250,0,0)
        self.info = pygame.Surface((width-height/2,height))
        pygame.draw.rect(self.info,color,(0,0,width-height,height))
        pygame.draw.circle(self.info,color,(width-height,height/2),height/2)
        self.info.set_colorkey((0,0,0))
        self.info.set_alpha(180)
        self.offset=[0,0]



    def NewTurn(self):
        self.moved = 0
        self.attacked = 0


    def Draw(self,surface,loc,offmap=0):
        tile_width = 80
        tile_height = 40
        if pygame.time.get_ticks()-self.last_animated>=self.animation_frame_time:
            self.animate_count = (self.animate_count+1)%4
            self.animate_timer=0
            self.last_animated = pygame.time.get_ticks()

        x = loc[0]+tile_width/2-self.images[0].get_width()/2+tile_width/2*(self.pos[1]%2)+self.offset[0]
        y = loc[1]-tile_height/2*self.pos[1]-self.images[0].get_height()+10+self.offset[1]

        if offmap: 
            x = loc[0]
            y = loc[1]
        if not self.jumping:
            surface.blit(pygame.transform.flip(self.images[self.animate_order[self.animate_count]+3*(self.facing[0]=='n')],(self.facing=='ne' or self.facing=='se'),0),[x,y])
        else:
            surface.blit(pygame.transform.flip(self.images[self.animate_order[1]+3*(self.facing[0]=='n')],(self.facing=='ne' or self.facing=='se'),0),[x,y])

    def Move(self,current_map):
        if pygame.time.get_ticks() - self.movement_last_updated>=self.movement_time:
            self.movement_last_updated = pygame.time.get_ticks()
            self.move_t-=1
        if self.level_difference !=0:
            self.jumping = 1
        elif self.jumping !=0:
            self.jumping = 0
        if self.move_t<0:
            if self.mov_vector==[]:
                self.moving = 0
                self.level_difference = 0
                self.jumping = 0
            else:
                self.facing =  utils.get_direction(self.pos,self.mov_vector[0])
                self.level_difference = 0
                if self.facing[0]=='s':
                    [self.pos[0],self.pos[1]] = self.mov_vector[0]
                    if self.level != utils.top_level(current_map,self.mov_vector[0]):
                        self.level_difference = utils.top_level(current_map,self.mov_vector[0])-self.level
                        self.level = utils.top_level(current_map,self.mov_vector[0])
                    self.mov_vector.remove(self.mov_vector[0])
                    self.move_t=20
                elif self.update_position==1:
                    [self.pos[0],self.pos[1]] = self.mov_vector[0]
                    if self.level != utils.top_level(current_map,self.mov_vector[0]):
                        self.level_difference = utils.top_level(current_map,self.mov_vector[0])-self.level
                        self.level = utils.top_level(current_map,self.mov_vector[0])
                    self.mov_vector.remove(self.mov_vector[0])
                    self.offset = [0,0]
                    self.update_position = 0
                else: 
                    self.update_position = 1
                    self.move_t=20
                    self.level_difference = utils.top_level(current_map,self.mov_vector[0])-self.level
                #self.offset=[0,0]
        if self.level_difference==0:
	        if self.facing == 'se':
	            self.offset[0] = -self.move_t*2
	            self.offset[1] = -self.move_t*1
	        elif self.facing == 'sw':
	            self.offset[0] = self.move_t*2
	            self.offset[1] = -self.move_t*1
	        elif self.facing== 'nw' and self.update_position==1:
	            self.offset[0] = self.move_t*2-40
	            self.offset[1] = self.move_t*1-20
	        elif self.facing == 'ne' and self.update_position==1:
	            self.offset[0] = -self.move_t*2+40
	            self.offset[1] = self.move_t*1-20
        elif self.level_difference<0:
	        if self.facing == 'se':
	            self.offset[0] = -self.move_t*2
	            self.offset[1] = utils.parabola_down(self.level_difference,self.move_t)
	        elif self.facing == 'sw':
	            self.offset[0] = self.move_t*2
	            self.offset[1] = utils.parabola_down(self.level_difference,self.move_t)
              
	        elif self.facing== 'nw' and self.update_position==1:
	            self.offset[0] = self.move_t*2-40
	            self.offset[1] = utils.parabola_down_n(self.level_difference,self.move_t)
	        elif self.facing == 'ne' and self.update_position==1:
	            self.offset[0] = -self.move_t*2+40
	            self.offset[1] = utils.parabola_down_n(self.level_difference,self.move_t)
        elif self.level_difference>0:
            if self.facing == 'nw' and self.update_position==1:
                self.offset[0] = self.move_t*2-40
                self.offset[1] = -20-utils.parabola_up(self.level_difference,self.move_t)

            if self.facing == 'ne' and self.update_position==1:
                self.offset[0] = -self.move_t*2+40
                self.offset[1] = -20-utils.parabola_up(self.level_difference,self.move_t)


    def Create_Move_Path(self,new_pos,ancestry):
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
            text = self.font.render(str(self.character.name),1,(250,250,250))
            canvas.blit(text, [loc[0],loc[1]])
            text = self.font.render("HP:"+str(self.character.current_hp)+"/"+str(self.character.hp),1,(250,250,250))
            canvas.blit(text, [loc[0],loc[1]+20])
            text = self.font.render("MP:"+str(self.character.current_mp)+"/"+str(self.character.mp),1,(250,250,250))
            canvas.blit(text,[loc[0],loc[1]+40])
        else:
            loc[0] = loc[0]-self.info.get_width()
            canvas.blit(pygame.transform.flip(self.info,1,0),loc)
            text = self.font.render(str(self.character.name),1,(250,250,250))
            canvas.blit(text, [loc[0]+50,loc[1]])
            text = self.font.render("HP:"+str(self.character.current_hp)+"/"+str(self.character.hp),1,(250,250,250))
            canvas.blit(text, [loc[0]+50,loc[1]+20])
            text = self.font.render("MP:"+str(self.character.current_mp)+"/"+str(self.character.mp),1,(250,250,250))
            canvas.blit(text,[loc[0]+50,loc[1]+40])





class Job:
    def __init__(self):
        pass

class Knight(Job):
    def __init__(self):
        self.image_sw,self.rect_sw = load_image('Knight5m-SW.gif',-1)
