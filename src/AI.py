from itertools import product, combinations
from collections import deque
from math import comb
from Constants import *
import numpy as np 
import random

class My_AI(): 
    def __init__(self, row, col, mines, board, start_x, start_y): 
        self.row = row
        self.col = col
        self.board = board
        self.mines_count = mines
        self.safe_frontier = deque() 
        self.unsure_frontier = deque()  
        self.mines = set()  
        self.tiles = {(i,j) for i in range(self.row) for j in range(self.col)} 
        self.tiles.remove((start_x, start_y)) 
        self.cur_x = start_x
        self.cur_y = start_y


        self.directions = [
            (0,1), (0,-1), (1,0), (-1,0), 
            (1,1), (1,-1), (-1,-1), (-1, 1)
            ] 
    
    def print_board(self): 
        # clear_console() 
        for i in range(self.row): 
                for items in self.board[i]: 
                    print(f'[{items}]', end = "") 
                print() 
    
    def add_neighbors(self, x, y, board): 
        flagged = set()
        unflagged = set()

        for dir in self.directions: 
            row_dir = x + dir[0]
            col_dir = y + dir[1]

            if (
                row_dir >= 0 and row_dir < self.row and 
                col_dir >= 0 and col_dir < self.col
            ): 
                if board[row_dir][col_dir] == Constants_.SPACE: 
                    unflagged.add((row_dir, col_dir))
                elif board[row_dir][col_dir] == Constants_.FLAG: 
                    flagged.add((row_dir, col_dir)) 
        
        return flagged, unflagged

    def play_safe_frontier(self): 
        tile = self.safe_frontier.popleft() 
        #print(f'Playing tile: {tile}')
        #print(f'Safe frontier: {self.safe_frontier}') 
        self.tiles.remove(tile) 
        #print(f'Removing tile: {tile}\n from: {self.tiles}')
    
        self.cur_x, self.cur_y = tile[0], tile[1] 
        return tile 

    def add_safe_tiles(self, neighbors): 
        for tile in neighbors: 
            if (
                tile not in self.safe_frontier and
                tile in self.tiles
            ): 
                self.safe_frontier.append(tile) 
    
    def flag_unsafe_tiles(self, mines): 
        progress = False

        for mine in mines: 
            if (
                mine not in self.mines and
                mine in self.tiles
            ): 
                self.mines.add(mine) 
                self.tiles.remove(mine) 
                self.board[mine[0]][mine[1]] = Constants_.FLAG
                progress = True

        return progress
                
    def check_unsafe_tiles(self): 
        progress = False 
        for x, y in self.unsure_frontier.copy() : 
            flag, unflag = self.add_neighbors(x, y, self.board) 

            if (
                len(flag) + len(unflag) == int(self.board[x][y]) and
                len(unflag) > 0
            ): 
                self.unsure_frontier.remove((x,y)) 
                self.flag_unsafe_tiles(unflag) 
                progress = True
            elif len(flag) == int(self.board[x][y]): 
                self.unsure_frontier.remove((x,y)) 
                self.add_safe_tiles(unflag) 
                progress = True

        return progress
    
    # are_consecutive maybe can replace this 
    def check_pair(self, a, b): 
        ax, ay = a
        if (
            (ax + 1, ay) == b or 
            (ax - 1, ay) == b or 
            (ax, ay + 1) == b or
            (ax, ay - 1) == b
        ): 
            return True 
        return False 
    
    def set_pairs(self, a, b): 
        ax, ay = a
        bx, by = b

        flag_a, unflag_a = self.add_neighbors(ax, ay, self.board) 
        flag_b, unflag_b = self.add_neighbors(bx, by, self.board)

        a_val = int(self.board[ax][ay]) - len(flag_a) 
        b_val = int(self.board[bx][by]) - len(flag_b)

        progress = False

        if a_val - b_val == len(unflag_a - unflag_b): 
            if self.flag_unsafe_tiles(unflag_a - unflag_b): 
                progress = True
            
            if self.add_safe_tiles(unflag_b - unflag_a): 
                progress = True
        elif (
            progress is False and
            b_val - a_val == len(unflag_b - unflag_a)
        ): 

            if self.flag_unsafe_tiles(unflag_b - unflag_a): 
                progress = True
            
            if self.add_safe_tiles(unflag_a - unflag_b): 
                progress = True

        return progress
            

    def set_determination(self): 
        l = len(self.unsure_frontier.copy())

        for i in range(l):
            tile_a = self.unsure_frontier[i] 
            for j in range(i + 1, l): 
                tile_b = self.unsure_frontier[j]
                if self.check_pair(tile_a, tile_b):     
                    #print(f'Checking pairs: {tile_a}, {tile_b}')
                    if self.set_pairs(tile_a, tile_b): 
                        #print(f'{tile_a}, {tile_b} successful')
                        return True 

        return False
    
    def are_consecutive(self, groups):
        groups = sorted(groups) 
    
        if all(
            groups[i][0] == groups[0][0] and 
            groups[i][1] == groups[0][1] + i 
            for i in range(len(groups))
        ):
            return True

        if all(groups[i][1] == groups[0][1] and 
               groups[i][0] == groups[0][0] + i 
               for i in range(len(groups))
        ):
            return True

        return False
    
    def get_subgroups(self, frontier, n): 
        subgroups = combinations(frontier, n) 
        res = [] 

        for i in subgroups:
            if self.are_consecutive(i):
                res.append(i) 
        
        return res 
    
    def get_neighbor_dict(self, group): 
        tile_neighbor= dict() 
        total_neighbors = []

        for tile in group: 
            flag, unflag = self.add_neighbors(tile[0], tile[1], self.board) 
            flag_count = len(flag) 
            unflag = sorted(unflag)

            tile_neighbor[tile] = (unflag, flag_count) 

            for nei in unflag: 
                if nei not in total_neighbors: 
                    total_neighbors.append(nei)
        
        return tile_neighbor, total_neighbors

    def make_a_b(self, tile_neighbor, total_neighbors):
        """ 
        Make the A, B matrices for CSP
        """
        A, B = [], [] 
        n = len(total_neighbors) 

        for k,v in tile_neighbor.items(): 
            B.append(int(self.board[k[0]][k[1]]) - tile_neighbor[k][1]) 
            cur = [0] * n

            for nei in v[0]:
                get_ = total_neighbors.index(nei) 
                cur[get_] = 1
            
            if len(A) == 0: 
                A = cur
            else: 
                A = np.vstack([A, cur])  

        return A, B

    def solve_for_x(self, A, B, n): 
        """ 
        Produce combination of [0,1] for size n of A, B matrices
        to find answer to A @ x = B.
        Takes long since it finds every combinations and tries it
        """
        solution = [] 

        binary_combinations = product([0,1], repeat=n)

        for combo in binary_combinations: 
            x = np.array(combo) 
            if np.array_equal(A @ x, B): 
                solution.append(x) 

        x = np.vstack(solution) 
        return solution 

    def csp(self, group, size_combo): 
        # self.print_board() 

        tile_neighbor, total_neighbors = self.get_neighbor_dict(group)

        n = len(total_neighbors)

        A, B = self.make_a_b(tile_neighbor, total_neighbors) 
        solution = self.solve_for_x(A, B, n) 

        if solution: 
            # self.print_board() 
            sol_arr = np.vstack(solution) 
            # print(f'Sol_arr shape: {sol_arr.shape}')

            if sol_arr.shape[0] != 1: 
                equal_ = np.all(sol_arr == sol_arr[0], axis=0) 
                check = False
                # self.print_board()

                # print(f'Solutions: {sol_arr}\n{equal_}') 

                for i in range(len(equal_)): 
                    if equal_[i] == True: 
                        x, y = total_neighbors[i] 
                        if sol_arr[0][i] == 1: # means that this is a mine
                            self.flag_unsafe_tiles([(x, y)]) 
                            check = True
                        elif sol_arr[0][i] == 0: # safe tiles 
                            self.add_safe_tiles([(x, y)]) 
                            check = True

            elif size_combo != 2: 
                subgroups_ = self.get_subgroups(group, 2)
                for group_ in subgroups_: 
                    #print(f'Checking subgroup_2: {group_}')
                    if self.csp(group_, 2): 
                        return True

            if check: 
                return True 
            
        return False
    
    def get_edge_cells(self, frontier): 
        edge_cells = [] 

        for tile in frontier: 
            x, y = tile 

            for dir in self.directions: 
                xd, yd = x + dir[0], y + dir[1] 

                if (
                    xd >= 0 and xd < self.row and 
                    yd >= 0 and yd < self.col and 
                    self.board[xd][yd] == ' '
                ): 
                    if (xd, yd) not in edge_cells: 
                        edge_cells.append((xd, yd)) 

        return edge_cells

    def num_neighbors(self, tile): 
        x, y = tile
        neighbors = [] 

        for d in self.directions: 
            xd, yd = x + d[0], y + d[1] 

            if ( 
                xd >= 0 and xd < self.row and
                yd >= 0 and yd < self.col and 
                self.board[xd][yd].isdigit()
            ): 
                if self.board[xd][yd] not in neighbors: 
                    neighbors.append((xd, yd)) 
        
        return neighbors 

    def valid_mine(self, grid, mine): 
        neighbors = self.num_neighbors(mine)

        for tile in neighbors: 
            x, y = tile 
            flag_count, _ = self.add_neighbors(x, y, grid)
            if len(flag_count) > int(grid[tile[0]][tile[1]]):
                return False 
        
        return True 
    
    def valid_arrangement(self, grid, count): 
        if count + len(self.mines) > self.mines_count: 
            return False
        
        for tile in self.unsure_frontier: 
            x, y = tile
            flag, _ = self.add_neighbors(x, y, grid)
            if len(flag) != int(grid[x][y]): 
                return False 
        
        return True 

    def mine_arrangements(self, edge):
        arrangements = set()

        def make_arrangements(grid, mines, count, idx):
            if idx == len(edge):
                if self.valid_arrangement(grid, count):
                    arrangements.add(tuple(mines))
                return
            
            x, y = edge[idx]

            grid[x][y] = 'F'
            mines[idx] = True

            if self.valid_mine(grid, (x, y)):
                make_arrangements(grid, mines, count + 1, idx + 1)

            grid[x][y] = ' '
            mines[idx] = False
            make_arrangements(grid, mines, count, idx + 1)

        grid = [row[:] for row in self.board] 
        make_arrangements(grid, [False] * len(edge), 0, 0)

        return arrangements

    
    # memoization
    # WIP - if multiple 0% moves, add all to safe frontier
    def mines_probability(self): 
        self.unsure_frontier = sorted(self.unsure_frontier)
        edge_cells = self.get_edge_cells(self.unsure_frontier)[:25]

        # print("Starting mine arrangement...\n")
        arrangements = self.mine_arrangements(edge_cells) 
        mines_prob = {k: 0 for k in edge_cells} 
        # print("Finished mine arrangement...")
 
        total_prob = 0 
        # print(f'Starting probability calculation with edge cell size: {len(edge_cells)}...') 
        for arr in arrangements: 
            count = 0 
            for i in range(len(arr)): 
                if arr[i] == True: 
                    count += 1
            
            probability = comb(
                len(self.tiles) - len(edge_cells), 
                (self.mines_count - count)
            )  

            if probability != 0:  
                total_prob += probability
            else: 
                probability = 1
            
            for j in range(len(arr)): 
                if arr[j] == True: 
                    mines_prob[edge_cells[j]] += probability
        
        if total_prob == 0: 
            total_prob = len(edge_cells) 

        if len(mines_prob) != 0 and edge_cells: 
            # print(f'Calculated mine probability with valid total probability...')
            for k, v in mines_prob.items(): 
                mines_prob[k] = round((v / total_prob) * 100, 3)

            min_ = min(mines_prob.values()) 
            choices = [i for i in mines_prob.keys() if mines_prob[i] == min_]

            # if prob of multiple tiles are 0, open all those tiles
            if min_ == 0 and len(choices) > 2: 
                # print("Multiple safe mines... adding to safe frontier...\n")
                self.add_safe_tiles(choices) 
                return 'C', 0, 0 # C = continue 

            random_ = random.choice(choices)
            return 'P', random_, mines_prob[random_]
        else:
            # print(f'Could not calculate probable move, finding random move from tile set...')
            # use random tile from tile set 
            choices = list(self.tiles) 
            random_ = random.choice(choices)

            return 'P', random_, round(1 / len(self.tiles), 3) # P = play
        

    def play_move(self, res): 
        self.res = res
        self.board[self.cur_x][self.cur_y] = self.res

        if self.res == Constants_.ZERO_TILE: 
            _, unflag = self.add_neighbors(self.cur_x, self.cur_y, self.board)
            self.add_safe_tiles(unflag) 
        else: 
            self.unsure_frontier.append((self.cur_x, self.cur_y))

        while len(self.mines) != self.mines_count: 
            #self.print_board() 
            # // -------------------------------------
            # Deterministic -> find safe tiles based on flagged + unflagged neighbors
            # print(f'Tiles in safe frontier: {len(self.safe_frontier)}\nTotal tiles left: {len(self.tiles)}')
            if self.safe_frontier: 
                return self.play_safe_frontier() 
            elif self.check_unsafe_tiles(): 
                    continue
            else: 
                # // -------------------------------------------------------
                # Set Determination 
                print("Using set determination...")
                self.unsure_frontier = deque(sorted(self.unsure_frontier))
                if self.set_determination(): 
                    continue
                else:
                    # // ---------------------------------------------------
                    # Constraint Satisfaction Problem
                    # get subgroups of 3, if more than 1 solution -> find commonalities
                    # else, get subgroups of 2 from the 3, helps for 1-1 mines or 1-2
                    print("Using CSP...")
                    subgroups = self.get_subgroups(self.unsure_frontier, 3)
                    for group in subgroups: 
                        if self.csp(group, 3):
                            break
                    # // -------------------------------------------------------

                    print("Using probability...")
                    move, safe_random, percent = self.mines_probability() 
                    if move == 'C': 
                        continue 
                    else:
                        # print(f'Playing safe random move: {safe_random} with {percent:.2f}% chance of being a mine\n') 
                        self.add_safe_tiles([safe_random])
                        continue
                        
        self.add_safe_tiles(self.tiles) 

        if self.safe_frontier:
            return self.play_safe_frontier()
