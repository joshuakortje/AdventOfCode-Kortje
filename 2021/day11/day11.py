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


def get_flashes(board):
    count = 0
    # Get all adjacent positions
    pos = list(itertools.product((0, 1, -1), repeat=2))
    while np.amax(board) > 9:
        # Loop over every spot on the board
        for i in range(1, len(board[1])-1):
            for j in range(1, len(board[1])-1):
                # If > 9 flash
                if board[i][j] > 9:
                    count += 1
                    board[i][j] = 0
                    # Add extra to adjacent positions
                    for x_add, y_add in pos:
                        new_i = i + x_add
                        new_j = j + y_add
                        # Increment anything other than -1 (edges) or 0 (flashed)
                        if board[new_i][new_j] != 0 and board[new_i][new_j] != -1:
                            board[new_i][new_j] += 1
    return count


# Start of script
file = open("input.txt", "r")

# Parse the file
text = list()
for line in file:
    text.append([int(x) for x in line.strip()])

octo = np.array(text)
octo = np.pad(octo, (1, 1), mode='constant', constant_values=(-1, -1))

flashes = 0
for i in range(10000): # arbitrary
    # Add 1 to everything
    octo[1:-1, 1:-1] += 1

    # Get the new flashes
    new_flashes = get_flashes(octo)

    # Part 2
    if new_flashes == 100:
        print('Part 2')
        print(i+1)
        break
    # Add the new flashes
    flashes += new_flashes


print(flashes)

# print results
print("Day 11")
print()

file.close()
