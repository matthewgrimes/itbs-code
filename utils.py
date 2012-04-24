import os,pygame
from pygame.constants import *
from global_vars import *

def load_image(name, colorkey=None):
	fullname = os.path.join('data',name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', name
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

#def normal_to_iso(coords)
#    iso 
def move_in_coords(pos,direction,layout):
        old_pos_x,old_pos_y = pos
        pos_x=pos[0]
        pos_y=pos[1]
        if direction=='right':
            pos_y+=1
            if pos_y%2==0:
                pos_x+=1
        if direction=='left':
            pos_y-=1
            if pos_y%2!=0:
                pos_x-=1
        if direction=='down':
            pos_y+=1
            if pos_y%2!=0:
                pos_x-=1
        if direction=='up':
            pos_y-=1
            if pos_y%2==0:
                pos_x+=1
        #if pos_x + layout[1][0]*pos_y > len(layout[0]) or pos_x>=layout[1][0] or pos_y>=layout[1][1]: pos = [old_pos_x,old_pos_y]
        if pos_x<0 or pos_y<0: 
            [pos_x,pos_y]=[old_pos_x,old_pos_y]
        #elif layout[0][pos_x + layout[1][0]*pos_y]==-1: pos = [old_pos_x,old_pos_y]
        return [pos_x,pos_y]

def check_for_water(current_map,pos):
    for level in range(1,current_map.layout[0]):
        try:
            if current_map.layout[level][pos[0]+current_map.size[0]*pos[1]]==2:
                return 1
        except IndexError:
            return 0

    return 0

def top_level(current_map,loc):
    top = 0
    for level in range(1,current_map.layout[0]):
        try:
            if current_map.layout[level][loc[0]+current_map.size[0]*loc[1]]!=-1:
                top = level
        except IndexError:
            return 1
    return top

def draw_circle(actor,current_map,actors,radius,people_ok=0):
    agility = 1
    # Add center
    openList=[actor.pos]
    childList=[]
    for i in range(0,radius):
        for parent in openList:
            for direction in ['up','down','left','right']:
                node = move_in_coords(parent,direction,[current_map.layout,[8,16]])
                if check_for_water(current_map,node)==0:
                    if top_level(current_map,node)-top_level(current_map,parent)<= agility:
                        try:
                            if current_map.layout[-1][node[0]+current_map.size[0]*node[1]]==-1 and current_map.layout[1][node[0]+current_map.size[0]*node[1]]!=-1:
                                add=1
                                for a in actors:
                                    if a.pos==node and people_ok==0:
                                        add = 0
                                if add==1: 
                                    childList.append(node)
                        except IndexError:
                            pass
        for node in childList:
            openList.append(node)
    output = openList
    openList = []
    for node in output:
        if node not in openList:
            openList.append(node)
    return openList


def sort_actors(actors):
    return range(0,len(actors))
