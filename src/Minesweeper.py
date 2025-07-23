from AI import My_AI
from Constants import Constants_, clear_console
import random

class Minesweeper: 
    def __init__(self): 
        self.x = 0
        self.y = 0
        self.mines = 0
        self.flagged_mines = 0
        self.tiles = {}
        self.real_board = []
        self.player_board = []
        self.game_over = False

    def create_board(self, x, y, mines): 
        self.x = x
        self.y = y
        self.mines = mines
        self.real_board = [['_' for _ in range(self.y)] for _ in range(self.x)] 
        self.player_board = [[' ' for _ in range(self.y)] for _ in range(self.x)] 
        self.tiles = {(i, j) for i in range(self.x) for j in range(self.y)}

    def set_board(self): 
        """ 
        Set board with mines, adjust nearby tiles based on number of mines
        """
        
        directions = [
            (0,1), (0,-1), (1,0), (-1,0), 
            (1,1), (1,-1), (-1,-1), (-1, 1)
            ] 

        # Place mines randomly
        count_mines = 0    
        while count_mines != self.mines:
            r_row = random.randrange(self.x) 
            r_col = random.randrange(self.y) 

            if self.real_board[r_row][r_col] != Constants_.MINE: 
                self.real_board[r_row][r_col] = Constants_.MINE
                count_mines += 1
            else: 
                continue
        
        # For each tile, check adjacent mines, set equal to # of mines
        for r in range(self.x): 
            for c in range(self.y): 
                if self.real_board[r][c] == Constants_.MINE: 
                    continue 

                mine_count = 0 
                for d in directions: 
                    row_dir = r + d[0]
                    col_dir = c + d[1] 
                    if row_dir >= 0 and row_dir < self.x and \
                        col_dir >= 0 and col_dir < self.y: 
                        if self.real_board[row_dir][col_dir] == Constants_.MINE: 
                            mine_count += 1
                
                self.real_board[r][c] = str(mine_count)
        
        x, y, res = self.first_move() 
        
        return x, y, res

    def print_board(self, player=True):  
        """
        Print player board if player, else print entire board
        """
        clear_console() 
        if player is False: 
            for r in self.real_board: 
                for items in r: 
                    print(f'[{items}]', end = "") 
                print()
        else: 
            for i in range(self.x): 
                print(f'{i} ', end = "") 
                for items in self.player_board[i]: 
                    print(f'[{items}]', end = "") 
                print() 

            print("   ", end = "") 
            for j in range(self.y): 
                print(f'{str(j)}  ', end = "") 
            print() 
              
    def first_move(self): 
        """
        Return the first row, column, and the value of the [r][c] that is 
        an empty tile
        """
        start_r = random.randrange(self.x) 
        start_c = random.randrange(self.y) 

        while self.real_board[start_r][start_c] != Constants_.ZERO_TILE: 
            start_r = random.randrange(self.x) 
            start_c = random.randrange(self.y) 

        self.tiles.remove((start_r, start_c)) 
        return (start_r, start_c, self.real_board[start_r][start_c]) 
    
    def is_valid_move(self, x, y): 
        return (self.player_board[x][y] == Constants_.SPACE and 
                self.real_board[x][y] != Constants_.MINE)


    def run(self, row, col, mines): 
        """ 
        """
        self.game_over = False
        self.create_board(row, col, mines) 
        x, y, res = self.set_board()     
        AI_ = My_AI(self.x, self.y, self.mines, self.player_board, x, y)

        while (len(self.tiles) != self.mines) and (self.flagged_mines != self.mines): 
            
            x, y = AI_.play_move(res) 
            x, y = int(x), int(y) 

            if self.is_valid_move(x, y): 
                res = self.real_board[x][y] 
                self.player_board[x][y] = res 
                self.tiles.remove((x,y)) 
            else:
                self.game_over = True
                break

        return not self.game_over # if game_over if False -> AI won else AI lost



