from Minesweeper import Minesweeper
import time 

def test_ai(row, col, mines): 
    wins = 0
    start = time.time()
    ms = Minesweeper() 

    for _ in range(5000): 
        if ms.run(row, col, mines): 
            wins += 1
            print(f'Wins: {wins}, total: {_ + 1}') 

    end = round(time.time() - start, 2)
    print(f'Ran for: {end} seconds')
    print(f'Won games: {wins}, win percentage: {wins / 5000 * 100:.2f}%')

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
    wins, time = test_ai(30, 16, 99)
    res['hard'] = (wins, time) 

    print(res) 

if __name__ == "__main__":
    main()

# AI score - 1000/5000 games, (win percentage, time to solve 1000/5000)

# trial 1: pre csp fix 
# difficulty: (win_percentage, time seconds)
# {'easy': (86.2%, 1637.93), 'med': (82.5%, 6657.39), 'hard': (34.2%, 10758.77)}

# trial 2 1000 runs: post csp fix TODO: need to add probability better choices
# {'easy': (860, 26.68), 'med': (850, 87.18), 'hard': (369, 1039.4)}
# easy: 86.0%, med: 85.0%, hard: 36.9%

# trial 3 5000 runs each: didnt fix probability yet: 
# {'easy': (4344, 131.12), 'med': (4266, 385.6), 'hard': (1869, 5134.93)}
# easy: 86.88%, med: 85.32%, hard: 37.38%

# trial 4: 1000 runs each: fixed probability
# {'easy': (900, 115.93), 'med': (859, 301.81), 'hard': (389, 3336.37)}
# easy: 90.0%, med: 85.9%, hard: 38.9%

# trial 5: testing 5000 runs: final test 
# easy: 87.7%, med: 85.02%, hard: 37.44%
