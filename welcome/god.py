from random import randint
import pygame as py
from creature import Red, Blue, Green
class God:
    def __init__(self,world):
        self.world = world
        self.avatar = None
        self.speed = 25
        self.moving = [0,0,0,0]     #boolean up/down/left/right, not used yet
    
    def auto_spawn(self,**kwargs):   #use a dictionary to determine starting numbers
        for colour,num in kwargs.items():
            colour = self.colour_converter(colour)
            for _ in range(num):
                pos = (randint(20,self.world.size[0]-20),randint(20,self.world.size[1]-20))
                self.single_spawn(colour(pos))           

    def single_spawn(self,creature):
        creature.world = self.world
        self.world.life_list.append(creature)

    def holy_spirit(self, pos):
        whitespace = True       #flag so that if whitespace is clicked, creatures becomes unholy and god has no avatar
        for creature in self.world.life_list:
            if (pos[0] < creature.pos[0] + creature.size[0]) and (pos[0] > creature.pos[0] - creature.size[0]) and (pos[1] < creature.pos[1] + creature.size[1]) and (pos[1] > creature.pos[1] - creature.size[1]):
                print('The power of Evan compels you!')
                creature.holy = True
                self.avatar = creature 
                whitespace = False 
        if whitespace == True:
            self.avatar = None

    def control_avatar(self,key,moving):
        if self.avatar != None:
            if key == py.K_e:
                self.moving[0] = moving
                self.avatar.moveup(self.speed)
            elif key == py.K_d:
                self.moving[1] = moving
                self.avatar.movedown(self.speed)
            elif key == py.K_f:
                self.moving[3] = moving
                self.avatar.moveright(self.speed)
            elif key == py.K_s:
                self.moving[2] = moving
                self.avatar.moveleft(self.speed)

    @staticmethod
    def colour_converter(s):
        if s == 'r':
            return Red
        elif s == 'b':
            return Blue
        elif s =='g':
            return Green

