from itertools import product, combinations
from collections import deque
from math import comb
from Constants import Constants_, clear_console
import numpy as np 
import random

class My_AI(): 
    def __init__(self, row, col, mines, board, start_x, start_y): 
        self.row = row
        self.col = col
        self.board = board
        self.mines_count = mines # total mines count
        self.safe_frontier = deque() 
        self.unsure_frontier = deque()  
        self.found_mines = set()  # set of found mine tiles 
        self.tiles = {(i,j) for i in range(self.row) for j in range(self.col)} 
        #print(f'Start move: {start_x}, {start_y}')
        self.tiles.remove((start_x, start_y))
        self.cur_x = start_x
        self.cur_y = start_y
        self.solved = False 

        self.directions = [
            (0,1), (0,-1), (1,0), (-1,0), 
            (1,1), (1,-1), (-1,-1), (-1, 1)
            ] 
    
    def print_board(self): 
        clear_console() 
        for i in range(self.row): 
                for items in self.board[i]: 
                    print(f'[{items}]', end = "") 
                print() 
    
    def add_neighbors(self, x, y, board): 
        """"
        Returns the set of all neighbors of a given tile 
        categorized by flagged and unflagged neighbors
        """
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
        """ 
        Returns the first appened tile in safe_frontier and removes it from total tile set, expected to be played 
        Updates self.cur_x and self.cur_y, awaits results from Minesweeper class to return the result of the tile played
        """
        tile = self.safe_frontier.popleft()

        if tile not in self.tiles: 
            print("ERROR: Tile not in self.tiles.")

        self.tiles.remove(tile)
        self.cur_x, self.cur_y = tile[0], tile[1] 

        return tile 

    def add_safe_tiles(self, neighbors): 
        """ 
        Adds each tile in the parameter neighbors to the safe frontier
        if it doesn't already exist in the safe_frontier and is unopened (exists in total tile set)
        Returns False is no tiles were added to safe_frontier
        """
        progress = False 
        for tile in neighbors: 
            if (
                tile not in self.safe_frontier and
                tile in self.tiles
            ): 
                if tile in self.unsure_frontier: 
                    self.unsure_frontier.remove(tile) 
                    
                self.safe_frontier.append(tile) 
                progress = True

        return progress
    
    def flag_unsafe_tiles(self, mines): 
        """
        Flags each tile in parameter mines, means that the tile is suspected to be a mine
        """

        # TODO: remove from unsure frontier maybe 
        progress = False

        for mine in mines: 
            if (
                mine not in self.found_mines and
                mine in self.tiles and 
                len(self.found_mines) < self.mines_count
            ): 
                self.found_mines.add(mine) 
                self.tiles.remove(mine) 

                if mine in self.unsure_frontier: 
                    self.unsure_frontier.remove(mine) 

                self.board[mine[0]][mine[1]] = Constants_.FLAG
                progress = True

        return progress
                
    def check_unsafe_tiles(self): 
        """ 
        Checks each tile in unsafe_tiles if it can be solved with a deterministic approach
        Usually called after finding an unsafe tile, opening a safe tile, or flagging a tile.
        """

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
    
    def check_pair(self, a, b): 
        """ 
        Checks if tile a and tile b are next to each other depending on Up, Down, Left, or Right directions
        """
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
        """ 
        Uses set determination for pairs a and b
        TODO: update description...
        """

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
    
    def are_shared(self, groups): 
        # need to intersect everything at once, not step by step it doesn't work like that 
        shared_set = set() # 

        for i in range(len(groups)): 
            _, unflag = self.add_neighbors(groups[i][0], groups[i][1], self.board)

            if not shared_set and i == 0: # maybe start with the tile that has the most neighbors 
                shared_set = unflag
            else: 
                shared_set = shared_set.intersection(unflag) 
        
        return True if len(shared_set) >= 1 else False
            
    def get_subgroups(self, frontier, n): 
        subgroups = combinations(frontier, n) # makes every combination of n^len(frontier) 
        res = [] 

        for i in subgroups:
            if self.are_consecutive(i) or self.are_shared(i): 
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
        solve for x to A @ x = B, where @ means matrix multiplication
        """
        solution = [] 

        binary_combinations = product([0,1], repeat=n)

        for combo in binary_combinations: 
            x = np.array(combo) 
            if np.array_equal(A @ x, B): 
                solution.append(x) 
                
        return solution 

    def csp(self, group, size_combo): 
        """
        Constraint Satisfaction Problem: turn the current group (size 2 or 3) into 
        a system of equations, find whether there is a solution and if so: 
            if there are more than 1 sols -> check commonalities, e.g x1 will always be false or true
            if only 1 sol -> try to use subset of size 2: can solve 1-1 or 2-1 problems
        
        """
        # TODO: understand this function again 

        tile_neighbor, total_neighbors = self.get_neighbor_dict(group)

        n = len(total_neighbors)

        A, B = self.make_a_b(tile_neighbor, total_neighbors) 
        solution = self.solve_for_x(A, B, n) 

        if solution != []: 
            sol_arr = np.vstack(solution)
            check = False

            if sol_arr.shape[0] != 1: # means that there are a system of linear equations
                equal_ = np.all(sol_arr == sol_arr[0], axis=0) 

                for i in range(len(equal_)): 
                    if equal_[i] == True: 
                        x, y = total_neighbors[i] 
                        if sol_arr[0][i] == 1: # in every combination, this tile position was always a mine
                            self.flag_unsafe_tiles([(x, y)]) 
                            check = True
                        elif sol_arr[0][i] == 0: # in every combination, this tile position was never a mine
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
    
    def get_edge_cells(self, frontier): 
        """
        Finds the edge cells of given frontier, such that the edge cells are the 
        unmarked tiles of the current opened tile
        """
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
        """ 
        Find the discovered/numbered neighbors of given tile
        """
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
        """
        Checks if current mine position (x, y) is valid based on the numbered tiles around it
        """
        neighbors = self.num_neighbors(mine)

        for tile in neighbors: 
            x, y = tile 
            flag_count, _ = self.add_neighbors(x, y, grid)
            if len(flag_count) > int(grid[tile[0]][tile[1]]):
                return False 
        
        return True 
    
    def valid_arrangement(self, grid, count, frontier): 
        """
        Checks if given arrangement is valid such that the count
        of mines used in the current arrangement + current mines found < total mines
        and checks if numbers of mines in an area is valid based on the numbered tiles.

        @param list[list[str]] grid A 2D list representing the current minesweeper board for the AI
        @param int count The number of mines used in the current arrangement
        @param list[tuple[int, int]] frontier A list of (x, y) coordinates representing the current frontier
        """
        if count + len(self.found_mines) > self.mines_count: 
            return False
        
        for tile in frontier:
            x, y = tile
            flag, _ = self.add_neighbors(x, y, grid)
            if len(flag) != int(grid[x][y]): 
                return False 
        
        return True 
    
    def mine_arrangements(self, edge, frontier):
        """
        Create arrangement of edge cells based on given frontier
        Computes 2^n, where n = length of edge cells
        """
        arrangements = set()

        def make_arrangements(grid, mines, count, idx):
            if idx == len(edge):
                if self.valid_arrangement(grid, count, frontier):
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

    def mines_probability(self, frontier): 
        """
        Get all arrangements of given edge cells (max 25) and compute their probability
        """
        edge_cells = self.get_edge_cells(frontier)[:25] 
        arrangements = self.mine_arrangements(edge_cells, frontier)

        mines_prob = {k: 0 for k in edge_cells} 

    
        total_prob = 0 
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
        else:
            # print(f'Could not calculate probable move, finding random move from tile set...')
            # use random tile from tile set 
            for k, v in mines_prob.items(): 
                mines_prob[k] = round(1 / len(self.tiles, 3)) 

        return mines_prob
    
    def separate_frontiers(self): 
        """
        Separates self.unsure_frontier into linked groups
        """

        frontiers = [] 
        visited = set() 

        def dfs(edges, idx, frontier, visited_n): 
            if idx > len(edges) - 1: 
                if frontier not in frontiers: 
                    frontiers.append(frontier) 
                return
            
            tile = edges[idx] 

            _, nei = self.add_neighbors(tile[0], tile[1], self.board)
            if len(visited_n) == 0: 
                frontier.append(edges[idx]) 
                visited_n.update(nei)
            elif len(nei.intersection(visited_n)) >= 1: 
                frontier.append(edges[idx]) 
                visited_n.update(nei)
            else: 
                if frontier not in frontiers: 
                    frontiers.append(frontier)

                visited_n = set() 
                visited_n.update(nei)
                frontier = [edges[idx]] 
            
            dfs(edges, idx + 1, frontier, visited_n) 
            
        dfs(self.unsure_frontier, 0, [], visited) 

        return frontiers 

    def prob_analysis(self): 
        mines_prob = {} 
        frontiers = self.separate_frontiers() # separates frontiers by connectedness or shared neighbors 

        for i in frontiers: 
            x = self.mines_probability(i)
            mines_prob = mines_prob | x

        if (not frontiers or not mines_prob): 
            random_ = random.choice(list(self.tiles)) 
            self.add_safe_tiles([random_]) 
            return -1 # -1 = random choice, unable to properly calculate a safe move 
        
        # TODO: add check if a regular random corner/edge tile better than min of the min of the probabilities found
        # instead of just finding corners -> edges 
        regular_tile = round((self.mines_count - len(self.found_mines)) / len(self.tiles), 3) * 100
        
        if min(mines_prob.values()) > regular_tile: 
            corners = [] 
            for x, y in self.tiles: 
                if (
                    (x, y) in ((0, 0),            (0, self.col - 1),
                                (self.row - 1, 0), (self.row - 1, self.col - 1)) and 
                    not self.num_neighbors((x, y))
                ):
                    corners.append((x, y)) 
            
            edges = [] 
            if not corners: 
                for x, y in self.tiles: 
                    if ( 
                        (x in (0, self.row - 1) or 
                        y in (0, self.col - 1)) and
                        not self.num_neighbors((x, y))
                    ): 
                        edges.append((x, y))
            
            for i in edges + corners: 
                mines_prob[i] = round((self.mines_count - len(self.found_mines)) / len(self.tiles) * 100, 4) 
        
        progress = False 
        # check if prob is 100 -> means that tile is guaranteed mine
        if self.flag_unsafe_tiles([k for k, v in mines_prob.items() if v == 100]): 
            progress = True
        
        # also check if prob is 0 -> means tile is guaranteed safe 
        if self.add_safe_tiles([k for k, v in mines_prob.items() if v == 0]): 
            progress = True
        
        if progress: # means something happened to safe frontier or unsafe frontier
            return 1
        
        # get min of the subset of tiles' calculated probabilities
        min_ = min(mines_prob.values())
        x = [k for k, v in mines_prob.items() if v == min_]
        self.add_safe_tiles([random.choice(x)]) 

        return 0 # means regular probability operations 
    

    def play_move(self, res): 
        """
        Returns mine sweeper move in form of a tile: (x, y) 
        Uses 4 layers to solve minesweeper grid: 
        - Deterministic, 
        - Set Determinaton, 
        - Constraint Satisfaction Problem,
        - Probability 
        """

        # self.print_board()

        self.res = res
        self.board[self.cur_x][self.cur_y] = self.res
        

        if self.res == Constants_.ZERO_TILE: 
            _, unflag = self.add_neighbors(self.cur_x, self.cur_y, self.board)
            self.add_safe_tiles(unflag) 
        else: 
            self.unsure_frontier.append((self.cur_x, self.cur_y))

        while len(self.found_mines) != self.mines_count: 
            # // -------------------------------------
            # Deterministic
            #   finds safe tiles based on flagged or unflagged neighbors
            #   if unmarked tile == tile num -> those tiles are mines 
            #   if unmarked + flagged == tile num -> those tiles are mines 

            if self.safe_frontier: 
                return self.play_safe_frontier() 
            elif self.check_unsafe_tiles(): 
                    continue
            else: 
                # // ---------------------------------------------------------------------------
                # Set Determination 
                #   also subset elimination:
                #       if tile a (unflag + flag) set - tile b (unflag + flag) = len(a) - len(b) 
                #       the set of tiles in a - tiles of b -> (a \ b): flag all those tiles
                #       the set of tiles in b  - tiles of a-> (b \ a): unflag those tiles
                # print("Using set determination...")
                self.unsure_frontier = deque(sorted(self.unsure_frontier))

                if self.set_determination(): 
                    # TODO: sometimes accepts but doesn't find safe move,
                    # instead finds a mine tile or etc.., maybe fix 
                    #print("Found safe movie from set_determination...") 
                    continue
                else:
                    # // -----------------------------------------------------------------------
                    # Constraint Satisfaction Problem
                    #   get subgroups of 3, if more than 1 solution -> find commonalities
                    #   else, get subgroups of 2 from the original 3, helps for 1-1 mines or 1-2

                    subgroups = self.get_subgroups(self.unsure_frontier, 3)

                    found = False 
                    for group in subgroups: 
                        if self.csp(group, 3):
                            found = True
                            break
                    
                    if found or self.safe_frontier: 
                        #print("Found safe movie in CSP or safe frontier available") 
                        continue

                    # // ----------------------------------------------------------------------------------------------
                    # Probability Using Mine Arrangements
                    #   get edge cells of the frontier -> the unmarked tiles of the "opened" tiles
                    #   for each edge cell, create arrangement whether tile can be a mine or not 
                    #   total arrangements = 2^len(edge cells)
                    #
                    #  Then create probability from:
                    #  (total unbordered cells) Choose (total mines left - mines used in arrangement)
                    #  Get sum of these probabilities from all arrangements and put into tile dict to get percentage of mine

                    # TODO: add corner probabilities maybe 
                    # TODO: check if probability = 100, that means it is guaranteed mine 
                    
                    self.prob_analysis() # 0, 1, -1 = {probability move, progress made, random move} 

                    continue
        
        if not self.solved: # all mines found, we need to add every tile to safe list
            self.add_safe_tiles(self.tiles)
            self.solved = True  

        return self.play_safe_frontier()
