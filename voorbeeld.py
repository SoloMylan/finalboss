import CA


def GameOfLifeSickness(cell, idx, grid):
    states = CA.Neighborhoods.get_neighbors2D_periodiek(grid, idx, 1)
    levende_buren = 0
    zieke_buren = 0
    for i in states: #telt de levende buren 
        if i == 1:
            levende_buren = levende_buren + 1
        if i >= 2:
            zieke_buren = zieke_buren + 1

    if cell == 0:
        if levende_buren == 3:
            return 1
        else:
            return 0

    if cell == 1:
        if zieke_buren >= 3:
            return 2
        elif levende_buren > 4 or levende_buren < 3: 
            return 0
        else:
            return 1

    if cell >= 2 and cell < 5:
        if levende_buren > 2:
            return 1
        else: 
            return cell+1
    
    if cell >= 5:
        return 0

colors = [(0,0,0), (0,255,0), (255,0,0)]
game = CA.Cellular2D(64,64, GameOfLifeSickness)
game.random(4)
game.runvisual(640,640, 100, 10, colors)