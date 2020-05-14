
class World:
    def __init__(self,size):
        self.life_list = []
        self.size = size

    def live(self):
        for creature in self.life_list:
            creature.move()
            creature.hunger += 1
            creature.horny += 1
            if creature.hunger > creature.starve_level:
                self.death(creature)
                print(f'Creature {creature.__class__!r} died of hunger. World now has {len(self.life_list)} creatures')
            if creature.horny > creature.breed_level:
                self.create(creature)
                creature.horny = 0

    def death(self,to_die):
        if to_die in self.life_list:
            self.life_list.remove(to_die)

    def create(self,parent):
        child = parent.breed()
        if child != None:
            child.world = self
            self.life_list.append(child)