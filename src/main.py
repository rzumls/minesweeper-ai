from Minesweeper import Minesweeper
import time 

c = 0 
start = time.time() 
for i in range(1, 501):
    mine_sweep = Minesweeper()
    if mine_sweep.run_game(False): 
        c += 1
        print(f'Won: {c} games Total: {i} games.\n')

end = time.time() 
print(f'Ran for: {end - start:.2f} seconds')
print(f'Won games: {c}, win percentage: {c / 500 * 100:.2f}%')

# 1000 games 
# 8x8 10 - 88.8%
# 16x16 40 - 80.9% ran for 2021 secs


# // ----------------------------------------------
#                   WIP
#     Separated frontiers for mine arrangements 
#     Make some functions better time complexity
# // ----------------------------------------------

# 500 games
# 16x30 99 - 29.20% 




