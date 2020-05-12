import pygame as py
class God:
    def __init__(self,world):
        self.world = world
        self.avatar = None
        self.speed = 25
        self.moving = [0,0,0,0]     #boolean up/down/left/right, not used yet
    
    def auto_spawn(self,**kwargs):   #use a dictionary to determine starting numbers
        pass

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

