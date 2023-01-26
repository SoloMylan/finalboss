import random as rnd

import numpy as np
import pygame

#Globale functies
class Neighborhoods:
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

    def get_neighbours2D(grid: np.ndarray, idx: list, reach: int) -> list:
        states = []
        #thanks steven
        for i in range(idx[0]-reach, idx[0]+reach+1):
            for j in range(idx[1]-reach, idx[1]+reach+1):
                if i > 0 and j > 0 and i < grid.shape[0] and j < grid.shape[1]:
                    #print(grid[(i,j)])
                    states.append(grid[(i,j)])
                else:
                    states.append(0)
        return states

    def get_neighbours(grid: np.ndarray, idx: list, reach: int) -> list:
        """"Geeft een lijst met alle staten van buurtcellen binnen een bereik van reach aantal cellen in elke dimensie. Geeft 0 als indexen buiten het grid vallen"""
        states = []
        #maakt gebruik van recursie, elke keer 1 dimensie eraf totdat we bij dimensie 1 uitkomen

        #basecase voor dimensie 1
        if len(idx) == 1:
            for i in range(idx[0]-reach, idx[0]+reach+1):
                #checken of indexen binnen grid vallen
                if i >= 0 and i < grid.shape[0]:
                    states.append(grid[i])
                else: 
                    states.append(0)
        else: #dimensie > 1
            for i in range(idx[0]-reach, idx[0]+reach+1): #we snijden het grid in stukjes met dimensie 1 lager, pakken daar degene bij die in onze neighborhood zitten
                if i >= 0 and i < grid.shape[0]:
                    states.extend(get_neighbours(grid[i], idx[1:], reach))
                else: 
                    states.extend(get_neighbours(np.zeros(idx[1:]), idx[1:], reach))
        return states

    def get_neighbours_wraparound(grid: np.ndarray, idx: list, reach: int) -> list:
        """"Geeft een lijst met alle staten van buurtcellen binnen een bereik van reach aantal cellen in elke dimensie. Gaat verder vanaf de andere kant als indexen buiten het grid vallen"""
        states = []
        #maakt gebruik van recursie, elke keer 1 dimensie eraf totdat we bij dimensie 1 uitkomen

        #basecase voor dimensie 1
        if len(idx) == 1:
            for i in range(idx[0]-reach, idx[0]+reach+1):
                    states.append(grid[i%grid.shape[0]])          
        else: #dimensie > 1
            for i in range(idx[0]-reach, idx[0]+reach+1):#we snijden het grid in stukjes met dimensie 1 lager, pakken daar degene bij die in onze neighborhood zitten            
                states.extend(get_neighbours_wraparound(grid[i%grid.shape[0]], idx[1:], reach))
        return states            

    def get_neighbours2D_wraparound(grid: np.ndarray, idx: list, reach: int) -> list:
        states = []
        #thanks steven
        for i in range(idx[0]-reach, idx[0]+reach+1):
            for j in range(idx[1]-reach, idx[1]+reach+1):
                states.append(grid[(i%grid.shape[0], j%grid.shape[1])])
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
        

    def runvisual(self, width: int, height: int, changetime: int, cellsize: int, rainbowmode: bool):
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
        
    def draw(self, screen, cellsize):
        """tekent het huidige grid op het scherm"""

        
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
    
    def runvisual(self, width: int, height: int, changetime: int, cellsize: int, rainbowmode: bool):
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
                self.draw(screen, cellsize)
                self.update()
                #tijd sinds laatste update wordt bijgewerkt
                last = pygame.time.get_ticks()
        
class GameOfLife(Cellular2D):

    def Game_of_life_rules(cell, idx, grid):
        states = Neighborhoods.get_neighbours2D_wraparound(grid, idx, 1)
        print(states)
        levende_buren = 0
        for i in states: #telt de levende buren 
                if i == 1:
                    levende_buren = levende_buren + 1
        
                    
        if cell == 0: #laat er een geboren worden als er precies 3 levende buren zijn
            if levende_buren == 3: 
                return 1
            else:
                return 0
        
            
        if cell == 1: #laat een levende cel sterven door over- of onderbevolking
            if levende_buren > 4 or levende_buren < 3: #er is hier rekening gehouden met dat cell ook leeft
                return 0
            else:
                return 1

    def __init__(self, width: int, height: int):
        super().__init__(width, height, GameOfLife.Game_of_life_rules)

    def glider(self, offset_width, offset_height, direction):
        """Zet een glider in het grid, met de linkerbovenkant op positie offset_width, offset_height, en direction 0 voor naar linksboven, 1 voor rechtsboven, 2 voor linksonder en 3 voor rechtsonder"""
        if direction == 0:
            self.setcells([(offset_width,offset_height), (offset_width+1, offset_height), (offset_width+2, offset_height), (offset_width, offset_height+1), (offset_width+1, offset_height+2)], 1)
        if direction == 1:
            self.setcells([(offset_width,offset_height), (offset_width+1, offset_height), (offset_width+2, offset_height), (offset_width+2, offset_height+1), (offset_width+1, offset_height+2)], 1)
        if direction == 2:
            self.setcells([(offset_width,offset_height+2), (offset_width+1, offset_height+2), (offset_width+2, offset_height+2), (offset_width, offset_height+1), (offset_width+1, offset_height)], 1)
        if direction == 3:
            self.setcells([(offset_width+1,offset_height),(offset_width+2,offset_height+1),(offset_width+1,offset_height+2),(offset_width,offset_height+2),(offset_width+2,offset_height+2)], 1)



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

def Game_of_life(cell, idx, grid):
    states = get_neighbours_wraparound(grid, idx, 1)
    print(states)
    levende_buren = 0
    for i in states: #telt de levende buren 
            if i == 1:
                levende_buren = levende_buren + 1
    
                
    if cell == 0: #laat er een geboren worden als er precies 3 levende buren zijn
        if levende_buren == 3: 
            return 1
        else:
            return 0
    
        
    if cell == 1: #laat een levende cel sterven door over- of onderbevolking
        if levende_buren > 4 or levende_buren < 3: #er is hier rekening gehouden met dat cell ook leeft
            return 0
        else:
            return 1

def Sickness(cell, idx, grid):
    states = get_neighbours_wraparound(grid, idx, 1)
    print(states)
    levende_buren = 0
    zieke_buren = 0
    for i in states: #telt de levende buren 
        if i == 1:
            levende_buren = levende_buren + 1
        if i == 2:
            zieke_buren = zieke_buren + 1

    if cell == 0:
        if levende_buren == 3:
            return 1
        else:
            return 0

    if cell == 1:
        if zieke_buren >= 2:
            return 2
        elif levende_buren > 4 or levende_buren < 3: 
            return 0
        else:
            return 1

    if cell >= 2:
        if levende_buren == 8:
            return 1
        else: 
            return cell+1
    
    if cell == 5:
        return 0
                    
    
    
    
#game = Cellular2D(20, 20, Game_of_life)
game = GameOfLife(20, 20)
#game = Cellular1D([640], rule22)
#game.setcells([(300)], )
#game.setcells([(10,10),(11,11),(10,12),(9,12),(11,12)], 1) #glider
game.glider(10,10, 1)
#game.setcells([(10,10), (11,10), (11,9), (11,11), (12,10)], 1) #pretty
#game.setcells([(10,11), (11,11), (11,10), (11,12), (12,10)], 1) #R-Pentomino
#game.setcells([(1,1), (1,2), (1,3)], 1)
print(game.grid)

game.runvisual(640,640, 100, 10, False)
