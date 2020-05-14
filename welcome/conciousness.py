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
            if not creature_looking.moves:
                continue
            #checks if creature already has a focus
            if creature_looking.focus != None:
                creature_looking.active += 1
                self.decide(creature_looking,creature_looking.focus)
                dist = ((creature_looking.pos[0]-creature_looking.focus.pos[0])**2 + (creature_looking.pos[1]-creature_looking.focus.pos[1])**2)**(0.5)
                if (dist < (creature_looking.size[0]+creature_looking.size[1])/3) and creature_looking.focus.__class__ == creature_looking.i_eat:     #special average size is the 'eat range'                     
                    creature_looking.eat(creature_looking.focus)
                if creature_looking.active >= creature_looking.object_permeance or creature_looking.__class__ == creature_looking.focus.__class__:
                    creature_looking.focus = None
                    continue
            #percieve closest creatures
            closest_creature = None
            closest_dist = None
            dist = 0
            for creature_seen in self.world.life_list:       #oof O(n2)
                if creature_looking == creature_seen:
                    continue
                dist = ((creature_looking.pos[0]-creature_seen.pos[0])**2 + (creature_looking.pos[1]-creature_seen.pos[1])**2)**(0.5)
                if dist < creature_looking.percieve_dist:
                    if closest_dist == None:
                        closest_creature, closest_dist = creature_seen, dist
                    elif dist < closest_dist:
                        closest_creature, closest_dist = creature_seen, dist
            if closest_creature != None:
                if (dist < (creature_looking.size[0]+creature_looking.size[1])/3) and closest_creature.__class__ == creature_looking.i_eat:     #special average size is the 'eat range'                     
                    creature_looking.eat(closest_creature)
                    creature_looking.horny += creature_looking.breed_level * 0.2
                elif (dist < (creature_looking.size[0]+creature_looking.size[1])/2) and closest_creature.__class__ == creature_looking.__class__:
                    creature_looking.focus = closest_creature
                    self.run_from_pred(creature_looking,closest_creature)       #activates to keep same species from overlapping on top of eachother
                else:
                    self.decide(creature_looking,closest_creature)

    def decide(self,creature_looking,closest_creature):
        creature_looking.focus = closest_creature 
        if closest_creature.__class__ == creature_looking.eat_me or closest_creature.__class__ == creature_looking.__class__:
            self.run_from_pred(creature_looking, closest_creature)
        elif closest_creature.__class__ == creature_looking.i_eat:
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
 
            