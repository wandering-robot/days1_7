from random import randint
import pygame as py
from conciousness import Conciousness


class Creature(Conciousness):
    world = None
    
    def __init__(self):
        super().__init__()
        self.size = (20,20)
        self.image = py.Surface(self.size).convert()
        self.holy = False          #by possesing them, will become holy=True
        self.pos = None             #subclasses will update
        self.speed = None

        self.focus = None
        self.active = 0                 #active describes the creatures ability to remember that it was trying to do something, and will do that thing for permeance ammount of turns
        self.object_permeance = None

    def eat(self,other):
        self.world.death(other)

    def move(self):
        if not(self.holy):
            if self.focus != None:
                self.decide2move()
            else:
                self.aimless_move()

    def aimless_move(self):
        i = randint(0,5)
        if i == 0:
            n = randint(0,3)
            self.want_to_go[n] = True
            self.decide2move()

    def decide2move(self):
        if self.want_to_go[0]:
            self.moveup(self.speed)
        elif self.want_to_go[1]:
            self.movedown(self.speed)
        if self.want_to_go[2]:
            self.moveleft(self.speed)
        elif self.want_to_go[3]:
            self.moveright(self.speed)
        self.want_to_go = [0,0,0,0]

    def moveup(self,speed):
        if (self.pos[1] - speed) >= (0 + self.size[1]/2):
            self.pos[1] -= speed
    def movedown(self,speed):
        if (self.pos[1] + speed) <= (self.world.size[1] - self.size[1]/2):
            self.pos[1] += speed
    def moveleft(self,speed):
        if (self.pos[0] - speed) >= (0 + self.size[0]/2):
            self.pos[0] -= speed
    def moveright(self,speed):
        if (self.pos[0] + speed) <= (self.world.size[0] - self.size[0]/2):
            self.pos[0] += speed

class Red(Creature):
    def __init__(self,pos):
        super().__init__()
        self.colour = (255,0,0)
        self.image.fill(self.colour)                        #I need some DRY in here
        w,h = pos
        self.pos = [w-self.size[0]/2, h-self.size[1]/2]

        self.speed = 1
        self.percieve_dist = 70
        self.i_eat = Blue

        self.object_permeance = 5

class Blue(Creature):
    def __init__(self,pos):
        super().__init__()
        self.colour = (0,0,255)
        self.image.fill(self.colour)
        w,h = pos
        self.pos = [w-self.size[0]/2, h-self.size[1]/2]        

        self.speed = 2
        self.percieve_dist = 50
        self.i_eat = Green
        self.eat_me = Red

        self.object_permeance = 10

class Green(Creature):
    def __init__(self,pos):
        super().__init__()
        self.colour = (0,255,0)
        self.image.fill(self.colour)
        w,h = pos
        self.pos = [w-self.size[0]/2, h-self.size[1]/2]        

        self.eat_me = Blue  #this might be redundant

if __name__ == '__main__':
    b =  Blue((12,12))
    r = Red((12,12))
    print(b.eat_me)
    print(r.__class__)