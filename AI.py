from collections import deque
from Constants import *
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
        self.tiles = {(i,j) for i in range(self.col) for j in range(self.row)} 
        self.cur_x = start_x
        self.cur_y = start_y


        self.directions = [
            (0,1), (0,-1), (1,0), (-1,0), 
            (1,1), (1,-1), (-1,-1), (-1, 1)
            ] 
    
    def print_board(self): 
        clear_console() 
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
                
    def check_unsafe_tiles(self, frontier): 
        for x, y in frontier: 
            flag, unflag = self.add_neighbors(x, y) 

            if len(flag) + len(unflag) == int(self.board[x][y]): 
                self.flag_unsafe_tiles(unflag) 
            elif len(flag) == int(self.board[x][y]): 
                self.add_safe_tiles(unflag) 
    
    def set_determination(self, frontier): 
        ...

            
    def play_move(self, res): 
        self.res = res
        self.board[self.cur_x][self.cur_y] = self.res

        if self.res == Constants_.ZERO_TILE: 
            _, unflag = self.add_neighbors(self.cur_x, self.cur_y)
            self.add_safe_tiles(unflag) 
        else: 
            self.unsure_frontier.append((self.cur_x, self.cur_y))

        while len(self.mines) != self.mines_count: 
            if self.safe_frontier: 
                tile = self.safe_frontier.popleft() 
                self.tiles.remove(tile) 
                self.cur_x, self.cur_y = tile[0], tile[1] 
                return tile 
            else: 
                unsure_ = self.unsure_frontier
                self.check_unsafe_tiles(unsure_) 
            self.print_board()

            
            # // ------------------------------------------------------------










        
                                
                    
                            
                                


                            

                            



                                    



            
        
        