import random

import numpy
import pygame


class Neighborhoods:  
    def get_neighbors1D(grid: numpy.ndarray, idx: list, reach: int, default: int) -> list:
        """Geeft een lijst met de staten van horizontale buren met reach voor verschillende 'groottes' van buurten. Bedoeld voor 1D, maar kan ook voor meerdere dimensies gebruikt worden. Dan kijkt het alleen naar buren in 1 dimensie (de 1e)"""
        states = []
        for i in range(idx[0]-reach, idx[0]+reach+1):
            #check dat de index bestaat, anders 0 toevoegen
            if i > 0 and i < grid.size:
                states.append(grid[i])
            else:
                states.append(default)
        return states

    def get_neighbors1D_periodiek(grid: numpy.ndarray, idx: list, reach: int) -> list:
        """geeft een list met de toestanden van buurtcellen in een 1D Moore-Neighborhood met reach voor de grootte van de buurt. Gaat verder vanaf de andere kant als cellen niet bestaan."""
        states = []
        for i in range(idx[0]-reach, idx[0]+reach+1):
            #voeg waarde van de cell toe, mod grid.size voor de wrap-around (aangepast voor mogelijk negatieve getallen als uitkomst)
            states.append(grid[(i - int(i/grid.size)*grid.size)])
        return states

    def get_neighbors2D(grid: numpy.ndarray, idx: list, reach: int, default: int) -> list:
        """geeft een list met de toestanden van buurtcellen in een 2D Moore-Neighborhood met reach voor de grootte van de buurt. Gebruikt default als cellen niet bestaan."""
        states = []
        #thanks steven
        for i in range(idx[0]-reach, idx[0]+reach+1):
            for j in range(idx[1]-reach, idx[1]+reach+1):
                if i > 0 and j > 0 and i < grid.shape[0] and j < grid.shape[1]:
                    #print(grid[(i,j)])
                    states.append(grid[(i,j)])
                else:
                    states.append(default)
        return states

    def get_neighbors(grid: numpy.ndarray, idx: list, reach: int, default: int) -> list:
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
                    states.append(default)
        else: #dimensie > 1
            for i in range(idx[0]-reach, idx[0]+reach+1): #we snijden het grid in stukjes met dimensie 1 lager, pakken daar degene bij die in onze neighborhood zitten
                if i >= 0 and i < grid.shape[0]:
                    states.extend(Neighborhoods.get_neighbors(grid[i], idx[1:], reach))
                else: 
                    states.extend(Neighborhoods.get_neighbors(numpy.zeros(idx[1:]), idx[1:], reach))
        return states

    def get_neighbors_periodiek(grid: numpy.ndarray, idx: list, reach: int) -> list:
        """"Geeft een lijst met alle staten van buurtcellen binnen een bereik van reach aantal cellen in elke dimensie. Gaat verder vanaf de andere kant als indexen buiten het grid vallen"""
        states = []
        #maakt gebruik van recursie, elke keer 1 dimensie eraf totdat we bij dimensie 1 uitkomen

        #basecase voor dimensie 1
        if len(idx) == 1:
            for i in range(idx[0]-reach, idx[0]+reach+1):
                    states.append(grid[i%grid.shape[0]])          
        else: #dimensie > 1
            for i in range(idx[0]-reach, idx[0]+reach+1):#we snijden het grid in stukjes met dimensie 1 lager, pakken daar degene bij die in onze neighborhood zitten            
                states.extend(Neighborhoods.get_neighbors_wraparound(grid[i%grid.shape[0]], idx[1:], reach))
        return states            

    def get_neighbors2D_periodiek(grid: numpy.ndarray, idx: list, reach: int) -> list:
        """geeft een list met de toestanden van buurtcellen in een 2D Moore-Neighborhood met reach voor de grootte van de buurt. Gaat verder vanaf de andere kant als cellen niet bestaan."""
        states = []
        #thanks steven
        for i in range(idx[0]-reach, idx[0]+reach+1):
            for j in range(idx[1]-reach, idx[1]+reach+1):
                states.append(grid[(i%grid.shape[0], j%grid.shape[1])])
        return states




class CellularAutomata():
    
    def __init__(self, shape, rules):
        """Maakt een cellulaire automata aan met de shape voor de vorm van het grid, en een functie rules met als inumpyut een cell, een index en het grid en als output de geupdate staat van de cell"""
        self.grid = numpy.zeros(shape) #grid begint met allemaal nullen
        self.shape = shape
        self.rules = rules

    def update(self):
        """update het hele grid door voor elke cel de rules functie op te roepen om te bepalen wat zijn nieuwe staat moet zijn"""
        nieuw_grid = numpy.copy(self.grid)
        for idx, cell in numpy.ndenumerate(self.grid):
            nieuw_grid[idx] = self.rules(cell, idx, self.grid)
        self.grid = nieuw_grid
    
    def run(self, updates: int):
        """Update het grid een gegeven aantal keer."""
        for i in range(updates):
            self.update()

    def __str__(self):
        return str(self.grid)

    def setcells(self, coordinates: list, value: int):
        """verandert de waarden van cellen met de gegeven coordinaten naar de gegeven waarde"""
        for idx in coordinates:
            self.grid[idx] = value

    def setzeros(self):
        """verandert alle waarden naar 0"""
        for idx, cell in numpy.ndenumerate(self.grid):
            self.grid[idx] = 0

    def random(self, max: int):
        """vult grid met random getallen tussen 0 en max"""
        for idx, cell in numpy.ndenumerate(self.grid):
            self.grid[idx] = random.randint(0,max)

class Cellular1D(CellularAutomata):

    def __init__(self, size: int, rules):
        super().__init__((size), rules)
        self.size = size
        #stored states word gebruikt voor rijen die worden getekend
        self.stored_states = []

    def start_middle(self):
        """"maakt het middelste element van het grid gelijk aan 1"""
        self.grid[(self.shape)//2] = 1
    
    
                


    def draw(self, screen: pygame.Surface, cellsize: int, surflist: list):
        """"tekent het grid op een screen, scrollt automatisch mee als onderkant van scherm wordt bereikt. Gebruikt de surflist met surfaces om de cellen in te tekenen op basis van de toestand."""
        
        #update de lijst van te tekenen rijen met de huidige staat
        self.stored_states.append(self.grid)
        
        screen.fill((0,0,0))
        

        #ga alle cellen bij langs en kleur ze in als de staat > 0  
        for line_idx in range(len(self.stored_states)):
            for idx, cell in numpy.ndenumerate(self.stored_states[line_idx]):
                if idx[0]*cellsize - (self.size*cellsize/2 - self.SCREEN_WIDTH/2) >= 0 and idx[0]*cellsize - (self.size*cellsize/2 - self.SCREEN_WIDTH/2) <= self.SCREEN_WIDTH:
                    #tekent vierkant op de correcte lijn door de line_idx die de correcte line aangeeft. Deze kan niet groter worden dan self.SCREEN_HEIGHT/cellsize doordat ongebruikte rijen verwijdert worden
                    screen.blit(surflist[int(cell)], ((idx[0]*cellsize - (self.size*cellsize/2 - self.SCREEN_WIDTH/2)), line_idx*cellsize))

        #update het hele scherm
        pygame.display.flip()

        #zorgt ervoor dat niet getekende (te hoge) rijen uit de lijst verwijdert worden
        if len(self.stored_states) > self.SCREEN_HEIGHT/cellsize:
                    self.stored_states.pop(0)
        

    def runvisual(self, width: int, height: int, changetime: int, cellsize: int, colorlist: list):
        """start pygame visualisatie met bepaalde width en height in pixels, changetime geeft tijd in ms tussen updates en colorlist zorgt voor de kleuren per toestand (als lijst met RGB-waardes)"""
        
        #variabelen initialiseren, en pygame configureren
        pygame.init()
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        size = [self.SCREEN_WIDTH,self.SCREEN_HEIGHT]
        self.changetime = changetime #ms
        screen = pygame.display.set_mode(size)
        surflist = []
        for color in colorlist:
            surf = pygame.Surface((cellsize, cellsize))
            surf.fill(color)
            surflist.append(surf)
        
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
                self.draw(screen, cellsize, surflist)
                self.update()
                #tijd sinds laatste update wordt bijgewerkt
                last = pygame.time.get_ticks()
                
class Cellular2D(CellularAutomata):
    
    def __init__(self, width: int, height: int, rules):
        super().__init__((width, height), rules)
        self.width = width
        self.height = height
        
    def draw(self, screen: pygame.Surface, cellsize: int, surflist: list):
        """tekent het huidige grid op het scherm"""

        
        screen.fill((0,0,0))
        

        #ga alle cellen bij langs en teken ze als de staat > 0
        for idx, cell in numpy.ndenumerate(self.grid):
            if cell >= len(surflist):
                screen.blit(surflist[-1], (idx[0]*cellsize, idx[1]*cellsize))
            else:
                screen.blit(surflist[int(cell)], (idx[0]*cellsize, idx[1]*cellsize))

        #update het hele scherm        
        pygame.display.flip()
    
    def runvisual(self, width: int, height: int, changetime: int, cellsize: int, colorlist: list):
        """start pygame visualisatie met bepaalde width en height in pixels, changetime geeft tijd in ms tussen updates en rainbowmode zorgt voor random kleuren"""

        #variabelen initialiseren, en pygame configureren
        pygame.init()
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        size = [self.SCREEN_WIDTH,self.SCREEN_HEIGHT]
        self.changetime = changetime #ms
        screen = pygame.display.set_mode(size)
        running = True
        updating = True
        surflist = []
        for color in colorlist:
            surf = pygame.Surface((cellsize, cellsize))
            surf.fill(color)
            surflist.append(surf)
        last = pygame.time.get_ticks()

        #main loop, gebruik pygame.time ipv sleep voor betere event handling
        while running:

            #event handling, alleen gebruikt zodat je normaal kunt sluiten
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        updating = not updating
            
            #huidige tijd wordt vergeleken met de tijd sinds de laatste update
            now = pygame.time.get_ticks()
            if now - last > changetime and updating:
                self.draw(screen, cellsize, surflist)
                self.update()
                #tijd sinds laatste update wordt bijgewerkt
                last = pygame.time.get_ticks()
        
class GameOfLife(Cellular2D):

    def Game_of_life_rules(cell, idx, grid):
        states = Neighborhoods.get_neighbors2D_periodiek(grid, idx, 1)
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

    def glider(self, offset_width: int, offset_height: int, direction: int):
        """Zet een glider in het grid, met de linkerbovenkant op positie offset_width, offset_height, en direction 0 voor naar linksboven, 1 voor rechtsboven, 2 voor linksonder en 3 voor rechtsonder"""
        if direction == 0:
            self.setcells([(offset_width,offset_height), (offset_width+1, offset_height), (offset_width+2, offset_height), (offset_width, offset_height+1), (offset_width+1, offset_height+2)], 1)
        if direction == 1:
            self.setcells([(offset_width,offset_height), (offset_width+1, offset_height), (offset_width+2, offset_height), (offset_width+2, offset_height+1), (offset_width+1, offset_height+2)], 1)
        if direction == 2:
            self.setcells([(offset_width,offset_height+2), (offset_width+1, offset_height+2), (offset_width+2, offset_height+2), (offset_width, offset_height+1), (offset_width+1, offset_height)], 1)
        if direction == 3:
            self.setcells([(offset_width+1,offset_height),(offset_width+2,offset_height+1),(offset_width+1,offset_height+2),(offset_width,offset_height+2),(offset_width+2,offset_height+2)], 1)










                    
    
    
    
