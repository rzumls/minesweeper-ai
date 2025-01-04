from Minesweeper import Minesweeper
# create option to choose r, c, or difficulty, replayability, use AI 
import time 
c = 0 

start = time.time() 
for i in range(1, 101): 
    mine_sweep = Minesweeper()
    if mine_sweep.run_game(False): 
        c += 1
        print(f'Won: {c} games Total: {i} games.')


end = time.time() 
print(f'Ran for: {end - start:.2f} seconds')
print(f'Won games: {c}, win percentage: {c / 100 * 100}%')
# 8x8 10 - (80.4, 79.2, 78.4)
# 16x16 40 - (75.9, 74.3, )
# 16x30 99 - 






