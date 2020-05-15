from random import randint, shuffle
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
        self.moves = True
        self.momentum = False

        self.focus = None

        self.eat_me = None
        self.i_eat = None

        self.hunger = 0
        self.starve_level = None

        self.horny = 0
        self.breed_level = None

    def die(self):
        self.colour = (51,17,0)
        self.image.fill(self.colour) 
        self.moves = False
        self.dead4 = 0

    def forget_focus(self):
        self.focus = None

    def is_starving(self):
        if self.hunger/self.starve_level > 0.8:
            return True

    def eat(self,other):
        if self.hunger/self.starve_level >= 0.1:      #so they feel satisfied for a bit
            self.world.death(other)
            self.focus = None
            self.hunger = 0
            self.horny += self.breed_level * 0.2      #reward for eating
        else:
            self.focus = other

    def move(self):
        if not(self.holy) and self.moves:
            if self.focus != None:
                self.decide2move()
            else:
                self.aimless_move()

    def aimless_move(self):
        i = randint(0,20)
        if i == 0:
            n = randint(0,3)
            self.want_to_go[n] = True
            self.momentum = self.want_to_go
            self.decide2move()
        elif i >= 18 and self.momentum != False:
            self.want_to_go = self.momentum
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
        self.percieve_dist = 50
        self.i_eat = Blue

        self.starve_level = 7000
        self.breed_level = 13000

    def breed(self):
        return Red(self.pos)

class Blue(Creature):
    def __init__(self,pos):
        super().__init__()
        self.colour = (0,0,255)
        self.image.fill(self.colour)
        w,h = pos
        self.pos = [w-self.size[0]/2, h-self.size[1]/2]        

        self.speed = 4
        self.percieve_dist = 35
        self.i_eat = Green
        self.eat_me = Red

        self.starve_level = 5000
        self.breed_level = 5001

    def breed(self):
        return Blue(self.pos)

class Green(Creature):
    patch = set()
    def __init__(self,pos):
        super().__init__()
        self.colour = (0,255,0)
        self.image.fill(self.colour)
        w,h = pos
        self.pos = [w-self.size[0]/2, h-self.size[1]/2]        
        self.patch.add(tuple(self.pos))

        self.speed = 10
        self.percieve_dist = 2*self.size[0]
        self.eat_me = Blue  #this might be redundant

        self.starve_level = 100000
        self.breed_level = 2000

    def breed(self):
        dir = list(range(-1,2))
        shuffle(dir)
        if dir[0] == 0:
            for d1 in dir:
                for d2 in dir:
                    pos = (self.pos[0]+d1*self.size[0],self.pos[1]+d2*self.size[1])
                    if pos not in self.patch:
                        return Green(pos)
                



if __name__ == '__main__':
    b =  Blue((12,12))
    r = Red((12,12))
    print(b.eat_me)
    print(r.__class__)