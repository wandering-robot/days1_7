import pygame as py
from conciousness import Conciousness


class Creature(Conciousness):
    def __init__(self):
        self.size = (20,20)
        self.image = py.Surface(self.size).convert()
        self.holy = False          #by possesing them, will become holy=True
        self.pos = None             #subclasses will update
        self.moving = [0,0,0,0]     #boolean up/down/left/right


    def moveup(self,speed):
        self.pos[1] -= speed
    def movedown(self,speed):
        self.pos[1] += speed
    def moveleft(self,speed):
        self.pos[0] -= speed
    def moveright(self,speed):
        self.pos[0] += speed

class Red(Creature):
    def __init__(self,pos):
        super().__init__()
        self.colour = (255,0,0)
        self.image.fill(self.colour)                        #I need some DRY in here
        w,h = pos
        self.pos = [w-self.size[0]/2, h-self.size[1]/2]

class Blue(Creature):
    def __init__(self,pos):
        super().__init__()
        self.colour = (0,0,255)
        self.image.fill(self.colour)
        w,h = pos
        self.pos = [w-self.size[0]/2, h-self.size[1]/2]        