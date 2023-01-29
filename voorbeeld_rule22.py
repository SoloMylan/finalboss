import CA


def rule22(cell, idx, grid):
    states = CA.Neighborhoods.get_neighbors1D_periodiek(grid, idx, 1)
    left = states[0]
    center = states[1]
    right = states[2]
    

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


game = CA.Cellular1D(640, rule22)
game.start_middle()
game.runvisual(640,640,100,10,[(0,0,0), (255,255,255)])