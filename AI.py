from itertools import product, combinations
from collections import deque
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
                print(f'{i} ', end = "") 
                for items in self.board[i]: 
                    print(f'[{items}]', end = "") 
                print() 

        print("   ", end = "") 
    
        for j in range(self.col): 
            print(f'{str(j)}  ', end = "") 
        print() 

    def add_neighbors(self, x, y): 
        flagged = set()
        unflagged = set()

        for dir in self.directions: 
            row_dir = x + dir[0]
            col_dir = y + dir[1]

            if (
                row_dir >= 0 and row_dir < self.row and 
                col_dir >= 0 and col_dir < self.col
            ): 
                if self.board[row_dir][col_dir] == Constants_.SPACE: 
                    unflagged.add((row_dir, col_dir))
                elif self.board[row_dir][col_dir] == Constants_.FLAG: 
                    flagged.add((row_dir, col_dir)) 
        
        return flagged, unflagged

    def play_safe_frontier(self): 
        tile = self.safe_frontier.popleft() 
        self.tiles.remove(tile) 
        self.cur_x, self.cur_y = tile[0], tile[1] 
        #print(f'Playing tile: {tile}') 
        return tile 

    def add_safe_tiles(self, neighbors): 
        for tile in neighbors: 
            if (
                tile not in self.safe_frontier and
                tile in self.tiles
            ): 
                self.safe_frontier.append(tile) 
    
    def flag_unsafe_tiles(self, mines): 
        for mine in mines: 
            if (
                mine not in self.mines and
                mine in self.tiles
            ): 
                self.mines.add(mine) 
                self.tiles.remove(mine) 
                self.board[mine[0]][mine[1]] = Constants_.FLAG
                
    def check_unsafe_tiles(self): 
        progress = False 
        for x, y in self.unsure_frontier.copy() : 
            flag, unflag = self.add_neighbors(x, y) 

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
        
    def set_determination(self): 
        l = len(self.unsure_frontier.copy())

        for i in range(l):
            tile_a = self.unsure_frontier[i] 
            for j in range(i + 1, l): 
                tile_b = self.unsure_frontier[j]
                if self.check_pair(tile_a, tile_b): 
                    ax, ay = tile_a 
                    bx, by = tile_b

                    flag_a, unflag_a = self.add_neighbors(ax, ay) 
                    flag_b, unflag_b = self.add_neighbors(bx, by)

                    a_val = int(self.board[ax][ay]) - len(flag_a) 
                    b_val = int(self.board[bx][by]) - len(flag_b) 

                    # print(f'Checking: {a_val} - {b_val} = {unflag_a - unflag_b}') 
                    if (
                        a_val - b_val == len(unflag_a - unflag_b)
                        and a_val - b_val != 0 
                    ):  
                        #self.print_board()
                        #print(f'Pair: {tile_a}, {tile_b} found set:')
                        #print(f'Unsafe tiles: {unflag_a - unflag_b}') 
                        #print(f'Safe tiles: {unflag_b - unflag_a}')
                        self.flag_unsafe_tiles(unflag_a - unflag_b) 
                        self.add_safe_tiles(unflag_b - unflag_a) 
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
            flag, unflag = self.add_neighbors(tile[0], tile[1]) 
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
                    if self.csp(group_, 2): 
                        return True

            if check: 
                return True 
            
        return False
        
    def play_move(self, res): 
        self.res = res
        self.board[self.cur_x][self.cur_y] = self.res

        if self.res == Constants_.ZERO_TILE: 
            _, unflag = self.add_neighbors(self.cur_x, self.cur_y)
            self.add_safe_tiles(unflag) 
        else: 
            self.unsure_frontier.append((self.cur_x, self.cur_y))

        while len(self.mines) != self.mines_count: 
            # self.print_board() 
            # // -------------------------------------
            # Deterministic -> find safe tiles based on flagged + unflagged neighbors
            if self.safe_frontier: 
                return self.play_safe_frontier() 
            elif self.check_unsafe_tiles(): 
                    continue
            else: 
                # // -------------------------------------------------------
                # Set Determination 
                self.unsure_frontier = deque(sorted(self.unsure_frontier))
                if self.set_determination(): 
                    continue
                else:
                    # // ---------------------------------------------------
                    # Constraint Satisfaction Problem
                    # get subgroups of 3, if more than 1 solution -> find commonalities
                    # else, get subgroups of 2 from the 3, helps for 1-1 mines or 1-2
                    subgroups = self.get_subgroups(self.unsure_frontier, 3)
                    for group in subgroups: 
                        if self.csp(group, 3):
                            break
                    else: 
                        # // ---------------- WIP -------------------------
                        # Smart Random 
                        # corners best guess -> edges -> use probability 

                        # GOAL: create different mine arrangements and find probability 

                        tiles_ = list(self.tiles) 

                        corners = [i for i in tiles_ if (
                            (i[0] == self.row - 1 and
                            i[1] == self.col - 1) or 
                            (i[0] == 0 and
                             i[1] == 0) or 
                            (i[0] == 0 and
                             i[1] == self.col - 1) or
                            (i[0] == self.row - 1 and
                             i[1] == 0)
                        )]

                        edges = [i for i in tiles_ if (
                            i[0] == self.row - 1 or
                            i[1] == self.col - 1 and 
                            i not in corners 
                        )] 

                        if corners: 
                            random_ = random.choice(corners) 
                        elif edges: 
                            random_ = random.choice(edges) 
                        else: 
                            random_ = random.choice(list(self.tiles)) 

                        self.safe_frontier.append(random_) 
                        continue 
        

        self.add_safe_tiles(self.tiles) 

        if self.safe_frontier:
            return self.play_safe_frontier()
