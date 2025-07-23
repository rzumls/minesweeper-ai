# Minesweeper AI Solver 

This is a **console-based Minesweeper AI solver** that works directly on the game board represented as arrays. The solver focuses on the logic and algorithms needed to solve Minesweeper puzzles without a graphical user interface.

---

## Features

- Solves Minesweeper puzzles using layered strategies:
  - **Deterministic rules** (safe moves and mine identification)
  - **Set Determination** (subset elimination)
  - **Constraint Satisfaction Problem (CSP)** approach for complex scenarios
  - **Probabilistic analysis** to handle uncertainty and guess safely
- Focus was on the solver rather than the actual game.

---

## How It Works

The solver updates a 2D array representing the Minesweeper board. Each move updates the board state, and the AI applies increasingly advanced techniques to find safe tiles or identify mines. The main logic layers are:

1. **Deterministic:** Mark safe or mine tiles based on neighbor counts.
2. **Set Determination:** Uses subset relationships among uncertain tiles.
3. **CSP:** Finds consistent mine placements in small groups of tiles.
4. **Probability:** Estimates mine likelihood on ambiguous tiles for informed guesses.

---
