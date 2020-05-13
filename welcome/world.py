
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
            if creature.horny > creature.breed_level:
                self.create(creature)

    def death(self,to_die):
        if to_die in self.life_list:
            self.life_list.remove(to_die)

    def create(self,parent):
        pass