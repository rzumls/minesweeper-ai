from itertools import product, combinations
from math import comb
import numpy as np 

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
""" 
grid = [[ 1, ' ', ' '],
        [ 1, ' ', ' '],
        [ 1, ' ', ' ']
    ]
 """
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

# // --------------------------------------------------------------
# PROBABILITY WORKS - IMPLEMEN WITH MINESWEEPER CAN JUST USE THIS 
grid = [[ 0,   0,   1, ' '],
        [ 1,   1,   2, ' '],
        [' ', ' ', ' ', ' '],
]

n, m = len(grid), len(grid[0]) 
unsure = [(0,2), (1,0), (1,1), (1,2)]

def get_edge_cells(frontier): 
    edge_cells = [] 

    for tile in frontier: 
        x, y = tile 

        for dir in directions: 
            xd, yd = x + dir[0], y + dir[1] 

            if (
                xd >= 0 and xd < n and 
                yd >= 0 and yd < m and 
                grid[xd][yd] == ' '
            ): 
                if (xd, yd) not in edge_cells: 
                    edge_cells.append((xd, yd)) 
            else: 
                continue
    
    return edge_cells

def add_numn(mine): 
    x, y = mine
    neighbors = [] 

    for d in directions: 
        xd, yd = x + d[0], y + d[1] 

        if ( 
            xd >= 0 and xd < n and
            yd >= 0 and yd < m and 
            type(grid[xd][yd]) == int
        ): 
            if grid[xd][yd] not in neighbors: 
                neighbors.append((xd, yd)) 
    
    return neighbors 

def valid_mine(grid, mine): 
    neighbors = add_numn(mine)

    for tile in neighbors: 
        flag_count, _ = add_(tile) 
        if flag_count > grid[tile[0]][tile[1]]:
            return False 
    
    return True 

def valid_arrangement(grid, frontier): 
    for tile in frontier: 
        i, j = tile 
        flag_c, _ = add_((i, j))
        if flag_c != grid[i][j]: 
            return False

    return True

edge_cells = get_edge_cells(unsure)
edge_cells.sort()  

def mine_arrangements(unsure_): 
    # get all edge cells, ones that border a number
    # for each edge, iterate through function to recursively
    # check if that edge can be mine or not

    # WIP -- modify for number of mines left 
    arrangements = set() 

    def make_arrangements(grid, mines, idx):
        grid_ = grid.copy() 

        if idx == len(mines):  
            if valid_arrangement(grid_, unsure): 
                arrangements.add(tuple(mines)) 
        else: 
            x, y = edge_cells[idx] 
            
            grid_[x][y] = 'F' 
            mines[idx] = True

            # try to place mine here, check if valid 
            # technically, does get valid mine placements 
            # however, some tiles with values may not have mines 
            if valid_mine(grid_, (x, y)): 
                make_arrangements(grid_, mines, idx + 1) 
            
            grid[x][y] = ' ' 
            mines[idx] = False
            # try to not place mine here 
            make_arrangements(grid_, mines, idx + 1) 
    
    make_arrangements(grid, [False] * len(edge_cells), 0) 

    return arrangements

x = mine_arrangements(unsure)

from collections import Counter

mines_prob = dict() 
for i in edge_cells: 
    mines_prob[i] = 0

total = len(x) 
total_arrangements = 0 
for arr in x: 
    mines_count = 0

    for i in range(len(arr)): 
        if arr[i] == True: 
            mines_count += 1

    prob = comb(465, (99 - mines_count))
    total_arrangements += prob 

    for j in range(len(arr)):
        if arr[j] == True: 
            mines_prob[edge_cells[j]] += prob


for k, v in mines_prob.items(): 
    print(f'{k}: {v / total_arrangements * 100:2f}')

print(f'total arrangements: {total}')
