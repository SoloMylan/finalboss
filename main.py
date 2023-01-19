import numpy as np
import random as rnd
import pygame
import time

#Globale functies

def get_neighbours1D(rooster, idx, reach):
    states = []
    for i in range(idx-reach, idx+reach+1):
        if i > 0 and i < rooster.size:
            states.append(rooster[i])
        else:
            states.append(0)
    return states

class CellularAutomata():
    
    def __init__(self, shape, rules):
        """Maakt een cellulaire automata aan met de shape voor de vorm van het rooster, en een functie rules met als input een cell, een index en het rooster en als output de geupdate staat van de cell"""
        self.rooster = np.zeros(shape)
        self.shape = shape
        self.rules = rules

    def update(self):
        nieuw_rooster = np.copy(self.rooster)
        for idx, cell in np.ndenumerate(self.rooster):
            nieuw_rooster[idx] = self.rules(cell, idx, self.rooster)
        self.rooster = nieuw_rooster
    
    def random(self):
        for idx, cell in np.ndenumerate(self.rooster):
            self.rooster[idx] = rnd.choice((0,1))

class Cellular1D(CellularAutomata):

    def __init__(self, size, rules):
        super().__init__((size,1), rules)
        self.size = size
        self.stored_states = []

    def start_middle(self):
        self.rooster[(self.shape[0])//2] = 1
    
    
                


    def draw(self, screen):
        self.cellsize = self.SCREEN_WIDTH//self.size
        #print(cellsize)
        screen.fill((0,0,0))
        surf = pygame.Surface((self.cellsize,self.cellsize))
        if self.rainbowmode:
            surf.fill((rnd.randint(0,255),rnd.randint(0,255),rnd.randint(0,255)))
        else:
            surf.fill((255,255,255))
        for line_idx in range(len(self.stored_states)):
            for idx, cell in np.ndenumerate(self.stored_states[line_idx]):
                if cell > 0:
                #print(idx[0],self.line_idx)
                    screen.blit(surf, (idx[0]*self.cellsize, line_idx*self.cellsize))
        pygame.display.flip()
        

    def run(self, width, height, changetime, rainbowmode):
        """start pygame visualisatie met bepaalde width en height, changetime geeft tijd tussen updates en rainbowmode is bool"""
        pygame.init()
        self.rainbowmode = rainbowmode
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        size = [self.SCREEN_WIDTH,self.SCREEN_HEIGHT]
        self.changetime = changetime #ms
        screen = pygame.display.set_mode(size)
        running = True
        last = pygame.time.get_ticks()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            now = pygame.time.get_ticks()
            if now - last > changetime:
                self.stored_states.append(self.rooster)
                self.draw(screen)
                self.update()
                if len(self.stored_states) > self.SCREEN_HEIGHT/self.cellsize:
                    self.stored_states.pop(0)
                    #changetime = 2000 #ms
                last = pygame.time.get_ticks()
                
class Cellular2D(CellularAutomata):
    
    def __init__(self, width, height, rules):
        super().__init__((width, height), rules)
        self.width = width
        self.height = height
        
    def draw(self, screen):
        self.cellsize = self.SCREEN_WIDTH//self.width
        #print(cellsize)
        screen.fill((0,0,0))
        surf = pygame.Surface((self.cellsize,self.cellsize))
        if self.rainbowmode:
            surf.fill((rnd.randint(0,255),rnd.randint(0,255),rnd.randint(0,255)))
        else:
            surf.fill((255,255,255))
        for idx, cell in np.ndenumerate(self.rooster):
            if cell > 0:
                screen.blit(surf, (idx[0]*self.cellsize, idx[1]*self.cellsize))
        pygame.display.flip()
    
    def run(self, width, height, changetime, rainbowmode):
        """start pygame visualisatie met bepaalde width en height, changetime geeft tijd tussen updates en rainbowmode is bool"""
        pygame.init()
        self.rainbowmode = rainbowmode
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        size = [self.SCREEN_WIDTH,self.SCREEN_HEIGHT]
        self.changetime = changetime #ms
        screen = pygame.display.set_mode(size)
        running = True
        last = pygame.time.get_ticks()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            now = pygame.time.get_ticks()
            if now - last > changetime:
                self.draw(screen)
                self.update()
                
                last = pygame.time.get_ticks()
        
          
def rule22(cell, idx, rooster):
    states = get_neighbours1D(rooster, idx[0], 1)
    left = states[0]
    center = states[1]
    right = states[2]
    #if idx[0] > 0:
     #   left = rooster[idx[0]-1,idx[1]] > 0
    #else: left = False
    #if idx[0] < rooster.shape[0] - 1:
    #    right = rooster[idx[0]+1,idx[1]] > 0
    #else: right = False
    #center = cell > 0

    if left and center and right:
        return 0
    elif left and center and not right:
        return 0
    elif left and not center and right:
        return 0
    elif left and not center and not right:
        return 1
    elif not left and right and center:
        return 0
    elif not left and center and not right:
        return 1
    elif not left and not center and right:
        return 1
    else: 
        return 0

    return cell

def rule54(cell, idx, rooster):
    if idx[0] > 0:
        left = rooster[idx[0]-1,idx[1]] > 0
    else: left = False
    if idx[0] < rooster.shape[0] - 1:
        right = rooster[idx[0]+1,idx[1]] > 0
    else: right = False
    center = cell > 0
    
    if left and center and right:
        return 0
    elif left and center:
        return 0
    elif left and right:
        return 1
    elif left:
        return 1
    elif center and right:
        return 0
    elif center:
        return 1
    elif right:
        return 1
    else:
        return 0
    
    return cell
    

game = Cellular1D(64, rule22)
game.start_middle()
game.run(640,640, 500, False)
