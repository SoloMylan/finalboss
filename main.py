import numpy as np
import random as rnd
import pygame
import time

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

class Cellullar1D(CellularAutomata):

    def __init__(self, size, rules):
        super().__init__((size,1), rules)
        self.line_idx = 0
        self.size = size

    def start_middle(self):
        self.rooster[(self.shape[0])//2] = 1


    def draw(self, screen):
        cellsize = 10
        surf = pygame.Surface((cellsize,cellsize))
        surf.fill((255,255,255))
        for idx, cell in np.ndenumerate(self.rooster):
            if cell > 0:
                print(idx[0],self.line_idx)
                screen.blit(surf, (idx[0]*cellsize, self.line_idx*cellsize))
        pygame.display.flip()
        self.line_idx += 1

    def run(self):
        pygame.init()
        SCREEN_WIDTH = 640
        SCREEN_HEIGHT = 640
        size = [SCREEN_WIDTH,SCREEN_HEIGHT]
        changetime = 1 #s
        screen = pygame.display.set_mode(size)
        while True:
            self.draw(screen)
            self.update()
            time.sleep(changetime)
          
def rule22(cell, idx, rooster):
    if idx[0] > 0:
        left = rooster[idx[0]-1,idx[1]] > 0
    else: left = False
    if idx[0] < rooster.shape[0] - 1:
        right = rooster[idx[0]+1,idx[1]] > 0
    else: right = False
    center = cell > 0

    if left and center:
        return 0
    elif left and right:
        return 0
    elif right and not center and not right:
        return 1
    elif center and right:
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
    

game = Cellullar1D(64, rule54)
game.start_middle()
game.run()
