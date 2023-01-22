import numpy as np
import random as rnd
import pygame
import time

#Globale functies

def get_neighbours1D(grid: np.ndarray, idx: list, reach: int) -> list:
    """Geeft een lijst met de staten van horizontale buren met reach voor verschillende 'groottes' van buurten. Bedoeld voor 1D, maar kan ook voor meerdere dimensies gebruikt worden. Dan kijkt het alleen naar buren in 1 dimensie (de 1e)"""
    states = []
    for i in range(idx-reach, idx+reach+1):
        #check dat de index bestaat, anders 0 toevoegen
        if i > 0 and i < grid.size:
            states.append(grid[i])
        else:
            states.append(0)
    return states

def get_neighbours1D_wraparound(grid: np.ndarray, idx: list, reach: int) -> list:
    states = []
    for i in range(idx-reach, idx+reach+1):
        #voeg waarde van de cell toe, mod grid.size voor de wrap-around (aangepast voor mogelijk negatieve getallen als uitkomst)
        states.append(grid[(i - int(i/grid.size)*grid.size)])
    return states

class CellularAutomata():
    
    def __init__(self, shape, rules):
        """Maakt een cellulaire automata aan met de shape voor de vorm van het grid, en een functie rules met als input een cell, een index en het grid en als output de geupdate staat van de cell"""
        self.grid = np.zeros(shape) #grid begint met allemaal nullen
        self.shape = shape
        self.rules = rules

    def update(self):
        """update het hele grid door voor elke cel de rules functie op te roepen om te bepalen wat zijn nieuwe staat moet zijn"""
        nieuw_grid = np.copy(self.grid)
        for idx, cell in np.ndenumerate(self.grid):
            nieuw_grid[idx] = self.rules(cell, idx, self.grid)
        self.grid = nieuw_grid
    
    def setcells(self, coordinates: list, value: int):
        """verandert de waarden van cellen met de gegeven coordinaten naar de gegeven waarde"""
        for idx in coordinates:
            self.grid[idx] = value

    def setzeros(self):
        """verandert alle waarden naar 0"""
        for idx, cell in np.ndenumerate(self.grid):
            self.grid[idx] = 0

    def random(self):
        """vult grid met random 0 of 1"""
        for idx, cell in np.ndenumerate(self.grid):
            self.grid[idx] = rnd.choice((0,1))

class Cellular1D(CellularAutomata):

    def __init__(self, size: int, rules):
        super().__init__((size), rules)
        self.size = size
        #stored states word gebruikt voor rijen die worden getekend
        self.stored_states = []

    def start_middle(self):
        """"maakt het middelste element van het grid gelijk aan 1"""
        self.grid[(self.shape[0])//2] = 1
    
    
                


    def draw(self, screen: pygame.Surface, cellsize: int, surf: pygame.Surface):
        """"tekent het grid op een screen, scrollt automatisch mee als onderkant van scherm wordt bereikt"""
        
        #update de lijst van te tekenen rijen met de huidige staat
        self.stored_states.append(self.grid)
        
        screen.fill((0,0,0))
        

        
        #kies de kleur van surf
        if self.rainbowmode:
            surf.fill((rnd.randint(0,255),rnd.randint(0,255),rnd.randint(0,255)))
        

        #ga alle cellen bij langs en kleur ze in als de staat > 0  
        for line_idx in range(len(self.stored_states)):
            for idx, cell in np.ndenumerate(self.stored_states[line_idx]):
                if cell > 0 and idx[0]*cellsize - (self.size*cellsize/2 - self.SCREEN_WIDTH/2) >= 0 and idx[0]*cellsize - (self.size*cellsize/2 - self.SCREEN_WIDTH/2) <= self.SCREEN_WIDTH:
                    #tekent vierkant op de correcte lijn door de line_idx die de correcte line aangeeft. Deze kan niet groter worden dan self.SCREEN_HEIGHT/cellsize doordat ongebruikte rijen verwijdert worden
                    screen.blit(surf, ((idx[0]*cellsize - (self.size*cellsize/2 - self.SCREEN_WIDTH/2)), line_idx*cellsize))

        #update het hele scherm
        pygame.display.flip()

        #zorgt ervoor dat niet getekende (te hoge) rijen uit de lijst verwijdert worden
        if len(self.stored_states) > self.SCREEN_HEIGHT/cellsize:
                    self.stored_states.pop(0)
        

    def run(self, width: int, height: int, changetime: int, cellsize: int, rainbowmode: bool):
        """start pygame visualisatie met bepaalde width en height in pixels, changetime geeft tijd in ms tussen updates en rainbowmode zorgt voor random kleuren"""
        
        #variabelen initialiseren, en pygame configureren
        pygame.init()
        self.rainbowmode = rainbowmode
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        size = [self.SCREEN_WIDTH,self.SCREEN_HEIGHT]
        self.changetime = changetime #ms
        screen = pygame.display.set_mode(size)
        surf = pygame.Surface((cellsize, cellsize))
        surf.fill((255,255,255))
        running = True

        #main loop, gebruik pygame.time ipv sleep voor betere event handling
        last = pygame.time.get_ticks()
        while running:

            #event handling, alleen gebruikt zodat je normaal kunt sluiten
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            #huidige tijd wordt vergeleken met de tijd sinds de laatste update
            now = pygame.time.get_ticks()
            if now - last > changetime:
                self.draw(screen, cellsize, surf)
                self.update()
                #tijd sinds laatste update wordt bijgewerkt
                last = pygame.time.get_ticks()
                
class Cellular2D(CellularAutomata):
    
    def __init__(self, width: int, height: int, rules):
        super().__init__((width, height), rules)
        self.width = width
        self.height = height
        
    def draw(self, screen):
        """tekent het huidige grid op het scherm"""

        cellsize = self.SCREEN_WIDTH//self.width
        screen.fill((0,0,0))
        surf = pygame.Surface((cellsize,cellsize))
        if self.rainbowmode:
            surf.fill((rnd.randint(0,255),rnd.randint(0,255),rnd.randint(0,255)))
        else:
            surf.fill((255,255,255))

        #ga alle cellen bij langs en teken ze als de staat > 0
        for idx, cell in np.ndenumerate(self.grid):
            if cell > 0:
                screen.blit(surf, (idx[0]*cellsize, idx[1]*cellsize))

        #update het hele scherm        
        pygame.display.flip()
    
    def run(self, width: int, height: int, changetime: int, rainbowmode: bool):
        """start pygame visualisatie met bepaalde width en height in pixels, changetime geeft tijd in ms tussen updates en rainbowmode zorgt voor random kleuren"""

        #variabelen initialiseren, en pygame configureren
        pygame.init()
        self.rainbowmode = rainbowmode
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        size = [self.SCREEN_WIDTH,self.SCREEN_HEIGHT]
        self.changetime = changetime #ms
        screen = pygame.display.set_mode(size)
        running = True
        last = pygame.time.get_ticks()

        #main loop, gebruik pygame.time ipv sleep voor betere event handling
        while running:

            #event handling, alleen gebruikt zodat je normaal kunt sluiten
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            
            #huidige tijd wordt vergeleken met de tijd sinds de laatste update
            now = pygame.time.get_ticks()
            if now - last > changetime:
                self.draw(screen)
                self.update()
                #tijd sinds laatste update wordt bijgewerkt
                last = pygame.time.get_ticks()
        
          
def rule22(cell, idx, grid):
    states = get_neighbours1D_wraparound(grid, idx[0], 1)
    left = states[0]
    center = states[1]
    right = states[2]
    #if idx[0] > 0:
     #   left = grid[idx[0]-1,idx[1]] > 0
    #else: left = False
    #if idx[0] < grid.shape[0] - 1:
    #    right = grid[idx[0]+1,idx[1]] > 0
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

def rule54(cell, idx, grid):
    if idx[0] > 0:
        left = grid[idx[0]-1,idx[1]] > 0
    else: left = False
    if idx[0] < grid.shape[0] - 1:
        right = grid[idx[0]+1,idx[1]] > 0
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
    

game = Cellular1D([640], rule22)
game.setcells([(300)], 1)

game.run(640,640, 500, 10, True)
