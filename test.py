import numpy as np
from itertools import product

# Constraint Satisfaction Problem
# // ---------------------------------------------------------

""" from itertools import combinations

tiles = [(3, 1), (3, 2), (3, 3), (1, 0), (1, 1), (1, 2), (2, 2), (2, 3)]
tiles = sorted(tiles)


# Trying to group by triples to set up CSP 

# Function to check if a list of tiles is "next to each other"
def find_next_to(tiles):

    triples = []
    # Group tiles by x coordinate
    tiles_by_x = {}
    for tile in tiles:
        if tile[0] not in tiles_by_x:
            tiles_by_x[tile[0]] = []
        tiles_by_x[tile[0]].append(tile)

    # Check for triples with the same x and decreasing y values
    for x in tiles_by_x:
        y_sorted = sorted(tiles_by_x[x], key=lambda t: t[1], reverse=True)
        for i in range(len(y_sorted) - 2):
            if y_sorted[i][1] > y_sorted[i + 1][1] > y_sorted[i + 2][1]:
                triples.append((y_sorted[i], y_sorted[i + 1], y_sorted[i + 2]))

    return triples
print(find_next_to(tiles)) """

A = np.array([
    [1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1 ,0, 0],
    [0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1]

])
B = np.array([1, 2, 2, 1])

# One way to find solution using linalg.lstsq
x = np.linalg.lstsq(A, B, rcond=None)[0] 
print(x) 

""" binary_combinations = product([0, 1], repeat=9)


# Another way but checks all combinations to find A @ x = B
for combination in binary_combinations:
    print(combination)
    x = np.array(combination)
    if np.array_equal(A @ x, B):
        print("Solution:", x)  """

# Takes O(n^3) 

# Learn ILP for small 


