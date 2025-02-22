from Minesweeper import Minesweeper
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time 

def run_minesweeper_game(row, col, mines):
    mine_sweep = Minesweeper()
    return mine_sweep.run_game(row, col, mines, False)

def test_ai(row, col, mines): 
    wins = 0
    lock = threading.Lock()  
    start = time.time()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_minesweeper_game, row, col, mines) for _ in range(1000)]

        for i, future in enumerate(as_completed(futures), 1):
            if future.result():
                with lock:  
                    wins += 1
                    print(f'Won: {wins} games Total: {i} games.')

    end = round(time.time() - start, 2)
    print(f'Ran for: {end} seconds')
    print(f'Won games: {wins}, win percentage: {wins / 1000 * 100:.2f}%')

    return wins, end
    
def main():
    res = dict() 
    print('Testing easy difficulty...')
    wins, time = test_ai(8, 8, 10)

    res['easy'] = (wins, time) 

    print('Testing medium difficulty...')
    wins, time = test_ai(16, 16, 40) 

    res['med'] = (wins, time)

    print('Testing hard difficulty...')
    wins, time = test_ai(16, 30, 99)

    res['hard'] = (wins, time) 

    print(res) 

if __name__ == "__main__":
    main()

# AI score - 1000 games, (win percentage, time to solve 1000)

# {
# 'easy': (86.2%, 1637.93), 
# 'med': (82.5%, 6657.39), 
# 'hard': (34.2%, 10758.77)
# }



