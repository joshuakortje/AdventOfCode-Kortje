import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
from scipy import ndimage
from functools import lru_cache
from collections import defaultdict
from collections import Counter
from collections import deque

# Looks like there is a solution where you can instead use the
# formula: x ored with 2*crease-x


# This function assumes the split will always be in the middle
# of the array. It deletes the middle row, splits into 2 sections
# flips the excess, and ORs together the results
def fold(array, dim):
    # Fold function
    shape = np.shape(array)
    middle = int((shape[dim]-1)/2)
    array = np.delete(array, middle, axis=dim)
    base, extra = np.split(array, 2, axis=dim)
    extra = np.flip(extra, dim)
    new_array = np.logical_or(base, extra)
    return new_array.astype(int)


# Start of script
file = open("input.txt", "r")

# Sizes are max + 1 (found empirically by mini max find program)
sizex = 1311
sizey = 895
grid = np.zeros((sizey, sizex), dtype=int)
dots_done = False

# Parse the file
text = list()
for line in file:
    if line.strip() == '':
        dots_done = True

    if dots_done:
        # folding
        text.append(line.strip().split())
    else:
        # Placing initial dots
        x, y = [int(x) for x in line.strip().split(',')]
        grid[y][x] = 1

# Folding
for fold_inst in text[1:]:
    # X or Y dimensions
    if fold_inst[2][0] == 'x':
        dimension = 1
    else:
        dimension = 0

    # Execute the fold
    new_grid = fold(grid, dimension)
    grid = new_grid.copy()

# print results
print("Day 13")
print(sum(sum(new_grid)))
print(new_grid)

# Pretty up the printing for convenience
print_grid = new_grid.astype(str)
print_grid = np.char.replace(print_grid, '1', '#')
print_grid = np.char.replace(print_grid, '0', '.')
print()
for i in range(0, 8*5 ,5):
    print(print_grid[:, i:i+5])
    print()

file.close()
