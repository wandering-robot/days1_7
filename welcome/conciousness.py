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
        for creature_looking in self.world.life_list:   #will iterate through all creatures
            if not creature_looking.moves:
                continue
            #checks if creature already has a focus
            if creature_looking.focus != None:
                dist = self.dist_between(creature_looking,creature_looking.focus)
                if not(self.can_see(creature_looking,creature_looking.focus,dist)):
                    creature_looking.forget_focus()
                    continue
                self.engage(creature_looking,creature_looking.focus,dist)
                continue
            #percieve closest creatures
            closest_creature = None
            closest_dist = None
            dist = 0
            for creature_seen in self.world.life_list:       #oof O(n2)
                if creature_looking == creature_seen:
                    continue
                if self.can_see(creature_looking,creature_seen):
                    if closest_dist == None:
                        closest_creature, closest_dist = creature_seen, dist
                    elif dist < closest_dist:
                        closest_creature, closest_dist = creature_seen, dist
            if closest_creature != None:
                self.engage(creature_looking,closest_creature,dist)
            if creature_looking.i_eat == None:      #spreads plants out for their first move, then makes them dormant
                creature_looking.moves = False

    def can_see(self,looking,seen,dist=None):
        if dist == None:
            dist = self.dist_between(looking,seen)
        return dist < looking.percieve_dist

    @staticmethod
    def same_class(creature1,creature2):
        return creature1.__class__ == creature2.__class__
    
    @staticmethod
    def dist_between(creature1,creature2):
        return ((creature1.pos[0]-creature2.pos[0])**2 + (creature1.pos[1]-creature2.pos[1])**2)**(0.5)

    def avoid_family(self,looking,seen,dist=None):
        if dist == None:
            dist = self.dist_between(looking,seen)
        if (dist < (looking.size[0]+looking.size[1])/2) and seen.__class__ == looking.__class__:
            self.run_from_pred(looking,seen)       #activates to keep same species from overlapping on top of eachother
            return True
        return False

    def engage(self,looking,seen,dist=None):
        if dist == None:
            dist = self.dist_between(looking,seen)
        if not(self.avoid_family(looking,seen,dist)):
            if not(self.try2eat(looking,seen,dist)):
                self.decide(looking,seen)

    def try2eat(self,looking,seen,dist=None):
        if dist == None:
            dist = self.dist_between(looking,seen)
        if (dist < (looking.size[0]+looking.size[1])*2/3) and seen.__class__ == looking.i_eat:     #special average size is the 'eat range'                     
            looking.eat(seen)
            return True
        return False

    def decide(self,creature_looking,closest_creature): 
        if closest_creature.__class__ == creature_looking.eat_me or closest_creature.__class__ == creature_looking.__class__:
            self.run_from_pred(creature_looking, closest_creature)
        elif closest_creature.__class__ == creature_looking.i_eat:
            creature_looking.focus = closest_creature
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
 
            