
class World:
    def __init__(self,size):
        self.life_list = []
        self.size = size

    def live(self):
        for creature in self.life_list:
            creature.move()
            # creature.try_to_eat
            # creature.try_to_breed

    def death(self,other):
        if other in self.life_list:
            self.life_list.remove(other)