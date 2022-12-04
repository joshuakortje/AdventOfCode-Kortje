import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
from collections import defaultdict


# Class to manage info storage
class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


# Draw the line on the floor grid
def draw_line(grid, line):
    if line.x1 == line.x2:
        for i in range(min(line.y1, line.y2), max(line.y1, line.y2) + 1):
            grid[line.x1][i] += 1
    elif line.y1 == line.y2:
        for i in range(min(line.x1, line.x2), max(line.x1, line.x2) + 1):
            grid[i][line.y1] += 1
    else:
        # Part 2
        # Not the best, but it works
        dir_x = (line.x2 - line.x1)/(abs(line.x1 - line.x2))
        dir_y = (line.y2 - line.y1)/(abs(line.y1 - line.y2))
        count_x = itertools.count(line.x1, dir_x)
        count_y = itertools.count(line.y1, dir_y)
        for i in range(abs(line.x1 - line.x2) + 1):
            grid[int(next(count_x))][int(next(count_y))] += 1


# Start of script
file = open("input.txt", "r")

# Parse the file
text = list()
for line in file:
    start, end = line.strip().split(' -> ')
    start_x, start_y = start.split(',')
    end_x, end_y = end.split(',')
    text.append(Line(int(start_x), int(start_y), int(end_x), int(end_y)))

# Init array of zeros
floor = np.zeros((1000, 1000), dtype=int)

# Draw each line
for vent in text:
    draw_line(floor, vent)
    print(floor)

# Get all spots >= 2
danger = floor >= 2
print(sum(sum(danger)))

# print results
print("Day 5")
print()

file.close()
