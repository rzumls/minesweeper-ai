# Minesweeper AI Solver 

This is a **console-based Minesweeper AI solver** that works directly on the game board represented as arrays. The solver focuses on the logic and algorithms needed to solve Minesweeper puzzles without a graphical user interface.

---

## Features

- Solves Minesweeper puzzles using layered strategies:
  - **Deterministic rules** (safe moves and mine identification)
  - **Set Determination** (subset elimination)
  - **Constraint Satisfaction Problem (CSP)** approach for complex scenarios
  - **Probabilistic analysis** to handle uncertainty and guess safely

---

## How It Works

The solver updates a 2D array representing the Minesweeper board. Each move updates the board state, and the AI applies increasingly advanced techniques to find safe tiles or identify mines. The main logic layers are:

1. **Deterministic:** Mark safe or mine tiles based on neighbor counts.
2. **Set Determination:** Uses subset relationships among uncertain tiles.
3. **CSP:** Finds consistent mine placements in small groups of tiles.
4. **Probability:** Estimates mine likelihood on ambiguous tiles for informed guesses.

---

## Trial Results and Developer Notes

The Minesweeper AI solver was tested on three classic difficulty levels:

- Easy: 8x8 board with 10 mines  
- Medium: 16x16 board with 40 mines  
- Hard: 30x16 board with 99 mines  

The AI was run on thousands of generated boards to evaluate its win percentage and total solving time.

| Trial | Runs per Difficulty | Description                  | Easy Win % | Easy Time (s) | Medium Win % | Medium Time (s) | Hard Win % | Hard Time (s) |
|-------|---------------------|------------------------------|------------|---------------|--------------|-----------------|------------|---------------|
| 1     | 5000                | Pre CSP fix                  | 86.2%      | 1637.93       | 82.5%        | 6657.39         | 34.2%      | 10758.77      |
| 2     | 1000                | Post CSP fix                 | 86.0%      | 26.68         | 85.0%        | 87.18           | 36.9%      | 1039.4        |
| 3     | 5000                | Before probability fix       | 86.88%     | 131.12        | 85.32%       | 385.6           | 37.38%     | 5134.93       |
| 4     | 1000                | After probability fix        | 90.0%      | 115.93        | 85.9%        | 301.81          | 38.9%      | 3336.37       |
| 5     | 5000                | Final test                   | 87.7%      | *N/A*         | 85.02%       | *N/A*           | 37.44%     | *N/A*         |

---

### Notes:

- **Win percentage:** Number of games won divided by total games played.
- **Time:** Total time to solve the number of boards at each difficulty.
- Improvements in CSP and probability logic led to better performance.
- Probability handling is ongoing and remains a key area for enhancement.
- The solver focuses on the logic and algorithm, no GUI is included.

---

# How to Run

Simply run the main.py file to begin testing the solver on the 3 difficulties. 
