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
import cProfile
import pandas as pd


# Helper function to print the boards
def pretty_print(b):
    for l in b:
        s = ''
        for i in range(len(l)):
            if l[i] == 0:
                s = s + '.'
            elif l[i] == 1:
                s = s + '>'
            else:
                s = s + 'v'
        print(s)
    print()


def step(grid, x_len, y_len):
    changed = False
    new_grid = np.zeros(grid.shape, dtype=int)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 2:
                new_grid[i][j] = 2
            elif grid[i][j] == 1 and grid[i][(j + 1) % y_len] == 0:
                new_grid[i][(j + 1) % y_len] = 1
                changed = True
            elif grid[i][j] == 1:
                new_grid[i][j] = 1
    grid = copy.deepcopy(new_grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 2 and grid[(i + 1) % x_len][j] == 0:
                new_grid[i][j] = 0
                new_grid[(i + 1) % x_len][j] = 2
                changed = True
            elif grid[i][j] == 2:
                new_grid[i][j] = 2
    return new_grid, changed



def day25():

    # Start of script
    file = open("input.txt", "r")


    # Read in the input
    board = [list(a) for a in [line.strip() for line in file.readlines()]]
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '.':
                board[x][y] = 0
            elif board[x][y] == '>':
                board[x][y] = 1
            else:
                board[x][y] = 2

    floor = np.array(board, dtype=int)
    x_len, y_len = floor.shape
    change = True
    sol = 0
    while change:
        sol += 1
        floor, change = step(floor, x_len, y_len)

    # print results
    print("Day 25")
    print(sol)

    file.close()


cProfile.run("day25()")
