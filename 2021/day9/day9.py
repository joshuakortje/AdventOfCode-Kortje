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


# NOTE TO SELF: could have used scipy.ndimage.measurements.label which would have found all of the basins

# makes it easier to find adjacent indicies
adj_set = {(0,1), (1,0), (-1,0), (0,-1)}


# Get the values at the adjacent spaces
def get_adj(m, x, y):
    return [m[x-1][y], m[x+1][y], m[x][y-1], m[x][y+1]]


# Find the full basin, filling with 9 as we go.
# Based on DFS.
def find_all(m, x_in, y_in):
    q = list()
    size = 0
    q.append((x_in, y_in))
    while q:
        x, y = q.pop(0)
        m[x][y] = 9
        size += 1
        for new_x, new_y in adj_set:
            if m[x + new_x][y + new_y] != 9 and (x + new_x, y + new_y) not in q:
                q.append((x + new_x, y + new_y))
    return size


# Start of script
file = open("input.txt", "r")

# Parse the file
text = list()
for line in file:
    text.append([int(x) for x in line.strip()])

floor = np.array(text)


# Part 1
points = 0
# Pad with 9s to make indexing easy
floor = np.pad(floor, (1, 1), mode='constant', constant_values=(9, 9))
x_max, y_max = floor.shape
for x in range(1, x_max-1):
    for y in range(1, y_max-1):
        nums = get_adj(floor, x, y)
        if floor[x][y] < min(nums):  # check if we have the min
            points += 1 + floor[x][y]

# Part 2
basin_sizes = list()
for x in range(1, x_max-1):
    for y in range(1, y_max-1):
        if floor[x][y] != 9:
            # Found a basin, now fill it and get the size
            basin_sizes.append(find_all(floor, x, y))

# Sort the sizes and report solution
basin_sizes = sorted(basin_sizes, reverse=True)
solution = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

# print results
print("Day 9")
print(points)
print(solution)

file.close()
