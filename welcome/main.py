import pygame as py
from world import World
from god import God
from creature import Red, Blue

class MainDisplay:
    def __init__(self):
        
        self.move_keys = [py.K_e,py.K_s,py.K_d,py.K_f]

        self.size = self.get_screen_size()
        self.fps = 2                #set frame rate, may change later
        self.clock = py.time.Clock()

        self.display_window = py.display.set_mode(self.size)
        self.background = py.Surface(self.display_window.get_size()).convert()
        self.world = World()
        self.god = God(self.world)
        self.default = {}           #will use this later to generate a specific population

    @staticmethod
    def get_screen_size():
        return (1000,500)   #temporarily overide the function
        # screen = input('[B]ig screen of [S]mall screen?').lower()
        # while screen not in ['s','b']:
        #     screen = input('[B]ig screen of [S]mall screen?').lower()
        # if screen == 'b':
        #     return (1900,1050)
        # else:
        #     return (1000,500)

    def set_bg_colour(self,colour):
        self.background.fill(colour)

    def set_title(self,title):
        py.display.set_caption(title)

    def update_objects(self):
        self.display_window.blit(self.background, (0,0))    #draws background first
        for creature in self.world.life_list:
            self.display_window.blit(creature.image, creature.pos)  #then goes through creature list and draws each one
        py.display.flip()

    def handle_event(self,event):
        if event.type == py.QUIT:       #quit simulation
            py.quit()
        elif event.type == py.MOUSEBUTTONDOWN:  #mouseclick events
            if event.button == 1:
                self.god.single_spawn(Red(event.pos))
            elif event.button == 3:          
                self.god.single_spawn(Blue(event.pos))
            else:
                self.god.holy_spirit(event.pos)
        elif event.type == py.KEYDOWN:      #keyboard events
            self.god.control_avatar(event.key)
        for key in self.move_keys:          #allow for held keys
            if py.key.get_pressed()[key]:
                self.god.control_avatar(key)



    def run(self):
        self.clock.tick(self.fps)
        while True:
            for event in py.event.get():
                self.handle_event(event)
            self.update_objects()

if __name__ == '__main__':
    sim = MainDisplay()
    sim.set_title('Welcome')
    sim.set_bg_colour((255,255,255))
    sim.run()

