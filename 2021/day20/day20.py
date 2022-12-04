import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
import binascii
import binarytree as bt
from scipy import spatial
from scipy import ndimage
from functools import lru_cache
from collections import defaultdict
from collections import Counter
from collections import deque


def get_index(grid, j, k):
    shift = sorted(itertools.product((0, -1, 1), repeat=2))
    bin_str = ''
    for x, y in shift:
        bin_str += str(grid[x + j, y + k])
    return int(bin_str, 2)


# Start of script
file = open("input.txt", "r")

# Parse the file
text = file.readlines()
key = list()
key = np.array([v == '#' for v in text[0].strip()], dtype=int)
grid = np.array([[v == '#' for v in line.strip()] for line in text[2:]], dtype=int)
# Pad by 50 on each side to account for the infinite direction
grid = np.pad(grid, (50, 50), mode='constant', constant_values=(0, 0))

# 50 turns
for i in range(50):
    new_grid = copy.deepcopy(grid)
    for j in range(1, len(grid)-1):
        for k in range(1, len(grid[0])-1):
            idx = get_index(grid, j, k)
            new_grid[j, k] = key[idx]
    # Fix the edges
    new_grid[0, :] = new_grid[1, 1]
    new_grid[:, 0] = new_grid[1, 1]
    new_grid[len(grid)-1, :] = new_grid[1, 1]
    new_grid[:, len(grid)-1] = new_grid[1, 1]
    grid = new_grid

# print results
print("Day 20")
print(sum(sum(grid)))

file.close()
