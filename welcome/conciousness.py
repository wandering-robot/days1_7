import pygame as py
from world import World

class Conciousness:
    world = None

    def __init__(self):
        self.want_to_go = [0,0,0,0]
        self.i_eat = None
        self.eat_me = None
        self.percieve_dist = None

    def percieve(self):
        for creature_looking in self.world.life_list:
            closest_creature = None
            closest_dist = None
            dist = 0
            for creature_seen in self.world.life_list:       #oof O(n2)
                dist = ((creature_looking.pos[0]-creature_seen.pos[0])**2 + (creature_looking.pos[1]-creature_seen.pos[1])**2)**(0.5)
                if closest_dist == None and dist > 0:
                    closest_creature, closest_dist = creature_seen, dist
                elif dist < creature_looking.percieve_dist and dist > 0:
                    if dist < closest_dist:
                        closest_creature, closest_dist = creature_seen, dist
            if closest_creature != None:
                if closest_creature.__class__ == creature_looking.eat_me:
                    self.run_from_pred(creature_looking, closest_creature)
                else:
                    self.run_to_food(creature_looking, closest_creature)

    def run_from_pred(self, creature,other):
        if other.pos[1] > creature.pos[1]:
            creature.want_to_go[0] =  1
        else:
            creature.want_to_go[1] = 1
        if other.pos[0] > creature.pos[0]:
            creature.want_to_go[2] =  1
        else:
            creature.want_to_go[3] = 1

    def run_to_food(self,creature,other):
        self.run_from_pred(creature,other)
        for i in range(4):
            creature.want_to_go[i] = not(creature.want_to_go[i])
 
            