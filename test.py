import numpy as np
from itertools import product, combinations

# Constraint Satisfaction Problem
# // ---------------------------------------------------------

directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1), 
        (1, -1), (1, 0), (1, 1)
    ]

def add_(tile):
    flag_count = 0
    neighbors = []

    x, y = tile 

    for dir in directions: 
        xd, yd = x + dir[0], y + dir[1] 
        if (
            xd >= 0 and xd < len(grid) and 
            yd >= 0 and yd < len(grid[0])
        ):
            if grid[xd][yd] == ' ':
                neighbors.append((xd, yd)) 
            elif grid[xd][yd] == 'F': 
                flag_count += 1
    
    return flag_count, neighbors

# set determination -> reveal 1-1 patterns, reveal other things
# CSP -> 1-2-1, 1-2-2-1, 1-2

grid = [[ 1, ' ', ' '],
        [ 1, ' ', ' '],
        [ 1, ' ', ' ']
    ]

unsure_frontier = [(0,0), (1,0), (2,0)]

def csp(grid, frontier): 
    neighbor_tiles = []
    tile_dict = dict() 

    for tile in frontier: 
        flag, nei = add_(tile) 
        nei = sorted(nei) 

        if tile not in tile_dict: 
            tile_dict[tile] = (nei, flag)
        else:
            tile_dict[tile] = (nei, flag)  

        for n in nei: 
            if n not in neighbor_tiles: 
                neighbor_tiles.append(n) 

    print(neighbor_tiles) 
    n = len(neighbor_tiles) 

    A = []
    B = [] 
    for k,v in tile_dict.items(): 
        # check if tile val - flag > 0 
        B.append(grid[k[0]][k[1]] - tile_dict[k][1])
        cur = [0] * n

        for ni in v[0]: 
            get_ = neighbor_tiles.index(ni) 
            cur[get_] = 1
        
        if len(A) == 0: 
            A = cur
        else: 
            A = np.vstack([A, cur]) 
    
    print(f'A = {A}\nB = {B}')

    # provides better solutions than linalg.lstsq, linalg.lstsq estimates but not guarantee
    binary_combinations = product([0, 1], repeat=n) 
    sol = [] 
    for combination in binary_combinations:
        x = np.array(combination)
        if np.array_equal(A @ x, B):
            sol.append(x)
    
    if not sol:
        print("False") 
    else: 
        print(sol) 
    
    test = np.vstack(sol)
    # equal_ = np.apply_along_axis(lambda col: np.all(col == col[0]), axis=0, arr=test)
    equal_ = np.all(test == test[0], axis=0) 
    print(equal_)
    for i in range(len(equal_)): 
        if equal_[i] == True: 
            print(grid) 
            x, y = neighbor_tiles[i] 
            if test[0][i] == 1: 
                grid[x][y] = 'F'
            elif test[0][i] == 0: 
                grid[x][y] == 'SAFE'

    # print(test.all(axis=1)) # axis = 0 checks all cols if all are equal 
                            # axis = 1 checks rows if all equal 


    # check what indexes are in common with solution
    # if 0 is common -> tile is safe
    # if 1 is common -> tile is a mine
    

csp(grid, unsure_frontier)
