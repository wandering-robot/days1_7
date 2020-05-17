import pygame as py
from world import World
from god import God
from creature import Red, Blue, Green
from conciousness import Conciousness

class MainDisplay:
    def __init__(self):
        
        self.running = True

        self.move_keys = [py.K_e,py.K_s,py.K_d,py.K_f]

        self.size = (1000,500)
        self.fps = 2                #set frame rate, may change later
        self.clock = py.time.Clock()

        self.offset = [0,0]          #the amount all surfaces will be offset when zoomed in
        self.zoom_og = self.size    #used to return to the original scale, initial size of background
        self.zoom_min = 1        #will never zoom out more than original setup
        self.zoom_max = 10       #can only zoom in 10x as big as original setup
        self.zoom_interval = 1.2  #how much one scoll will zoom it, should tailor this to what 'feels right'
        self.zoom_level = 1         #keep track of what zoom amount we're at right now

        self.display_window = py.display.set_mode(self.size)
        self.background = py.Surface(self.display_window.get_size()).convert()
        self.world = World(self.size)
        self.god = God(self.world)
        self.conciousness = Conciousness()
        self.conciousness.world = self.world
        self.default = {'r':5,'b':10,'g':40}           #will use this later to generate a specific population

    def pan(self,mousepos):
        activate = 0.2      #will activate when cursor within this ratio of walls
        increment = 4       #panning will move background this far per cycle
        mw,mh = mousepos
        delta = [0,0]
        dw,dh = self.display_window.get_size()
        if mw < dw * activate:  #go left
            delta[0] = -increment
        elif mw > dw * (1-activate):    #go right
            delta[0] = increment
        if mh < dh * activate:  #go up
            delta[1] = -increment
        elif mh > dh * (1-activate):    #go down
            delta[1] = increment
        self.try2pan(delta)


    def zoom(self,amount,mousepos):
        # if amount == -1, zooming out
        if self.zoom_level + amount >= self.zoom_min and self.zoom_level + amount <= self.zoom_max:
            self.zoom_level += amount
            if amount == 1:
                zoom_mod = self.zoom_interval          
            else:
                zoom_mod = 1/self.zoom_interval
            self._zoom(zoom_mod)
            self.try2pan([mousepos[0]*(zoom_mod-1), mousepos[1]*(zoom_mod-1)]) 
        else:
            if amount == -1 and self.background.get_size() != self.zoom_og: #so that zoom out level will always max out at exactly the original
                zoom_mod = self.iter_ratio(self.zoom_og, self.background.get_size())
                self._zoom(zoom_mod)
                self.offset = [0,0]

    def _zoom(self,zoom_mod):
        self.background = py.Surface(self.resize(self.background.get_size(),zoom_mod)).convert()
        self.set_bg_colour((255,255,255))
        for creature in self.world.all_creatures():
            creature.image = py.Surface(self.resize(creature.size,zoom_mod)).convert()
            creature.image.fill(creature.colour)
            creature.speed = self.resize(creature.speed,zoom_mod)
            creature.pos = self.resize(creature.pos,zoom_mod)

    def try2pan(self,delta):
        for dim in range(2):
            if self.offset[dim] + delta[dim] < 0:
                delta[dim] = -self.offset[dim]
            elif self.offset[dim] + delta[dim] > self.background.get_size()[dim] - self.display_window.get_size()[dim]:
                delta[dim] = self.background.get_size()[dim] - self.display_window.get_size()[dim] - self.offset[dim]
        self.offset = [self.offset[0]+delta[0],self.offset[1]+delta[1]]

    def apply_offset(self,tup):
        return (tup[0]-self.offset[0],tup[1]-self.offset[1])

    @staticmethod
    def resize(data,mod):
        if type(data) == int or type(data) == float:
            if type(mod) == tuple:
                return data * (mod[0]+mod[1])/2
            else:
                return data*mod
        if type(mod) == int or type(mod) == float:
            return type(data)((data[0]*mod,data[1]*mod))
        elif type(mod) == tuple:
            return type(data)((data[0]*mod[0],data[1]*mod[1]))

    @staticmethod
    def iter_ratio(tup1,tup2):          #used when trying to return to original max zoom out level
        return (tup1[0]/tup2[0],tup1[1]/tup2[1])

    def skip(self):
        self.fps = self.fps*2

    def set_default(self):
        nums = input("input desired autospan numbers for r:b:g\t")
        nums = nums.split(':')
        self.default['r'] = int(nums[0])
        self.default['b'] = int(nums[1])
        self.default['g'] = int(nums[2])

    def set_bg_colour(self,colour):
        self.background.fill(colour)

    def set_title(self,title):
        py.display.set_caption(title)

    def update_objects(self):
        self.display_window.blit(self.background, self.apply_offset((0,0)))    #draws background first
        for creature in self.world.death_list:
            self.display_window.blit(creature.image,self.apply_offset(creature.pos))
        for creature in self.world.life_list:
            self.display_window.blit(creature.image, self.apply_offset(creature.pos))  #then goes through creature list and draws each one
        py.display.flip()

    def handle_event(self,event):
        if event.type == py.QUIT:       #quit simulation
            py.quit()
            self.running = False
        elif event.type == py.MOUSEBUTTONDOWN:  #mouseclick events
            if event.button == 1: 
                self.god.single_spawn(Green(event.pos))
            elif event.button == 3:          
                self.god.single_spawn(Blue(event.pos))
            elif event.button == 2:
                self.god.holy_spirit(event.pos)
            elif event.button == 4:
                mousepos = py.mouse.get_pos()
                self.zoom(1,mousepos)
            elif event.button == 5:
                mousepos = py.mouse.get_pos()
                self.zoom(-1,mousepos)
        elif event.type == py.MOUSEMOTION:
            self.pan(event.pos)
        elif event.type == py.KEYDOWN:      #keyboard events
            if event.key == py.K_SPACE:
                self.god.auto_spawn(**self.default)
            elif event.key == py.K_n:
                self.set_default()
            elif event.key == py.K_m:
                self.skip()
            self.god.control_avatar(event.key,True)
        elif event.type == py.KEYUP:
            self.god.control_avatar(event.key,False)

    def run(self):
        self.clock.tick(self.fps)
        while self.running:
            print(self.offset)
            self.update_objects()           #redraw creation's positions
            for event in py.event.get():    #get input from god
                self.handle_event(event)    
            self.conciousness.percieve()    #get input from creations
            self.world.live()               #have creations do their thing based on what they want

if __name__ == '__main__':
    sim = MainDisplay()
    sim.set_title('Welcome')
    sim.set_bg_colour((255,255,255))
    sim.run()

