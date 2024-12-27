from Minesweeper import Minesweeper
# create option to choose r, c, or difficulty, replayability, use AI 
import time 
c = 0 

start = time.time() 
for i in range(1000): 
    mine_sweep = Minesweeper()
    if mine_sweep.run_game(False): 
        c += 1

end = time.time() 
print(f'Ran for: {end - start:.2f} seconds')
print(f'Won games: {c}, win percentage: {c / 1000 * 100}%')






