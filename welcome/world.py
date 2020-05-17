
class World:
    def __init__(self,size):
        self.life_list = []
        self.death_list = []
        self.size = size

    def all_creatures(self):
        all_creatures =  self.life_list
        all_creatures.extend(self.death_list)
        return all_creatures

    def live(self):
        for creature in self.life_list:
            creature.move()
            creature.hunger += 1
            creature.horny += 1
            if creature.horny > creature.breed_level:
                self.create(creature)
                creature.horny = 0
            if creature.hunger > creature.starve_level:
                self.death(creature)
                creature.die()
                self.death_list.append(creature)
        for creature in self.death_list:
            creature.dead4 += 1
            if creature.dead4 > 500:
                self.final_death(creature)

    def final_death(self,zombie):
        if zombie in self.death_list:
            self.death_list.remove(zombie)      
                
    def death(self,to_die):
        if to_die in self.life_list:
            self.life_list.remove(to_die)

    def create(self,parent):
        child = parent.breed()
        if child != None:
            child.world = self
            self.life_list.append(child)

if __name__ == "__main__":

    l1 = (2,2)
    l2= [3,3]
    print(type(l1)(l2))
