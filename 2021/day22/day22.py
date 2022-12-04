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


def get_direct(box):
    return (box[1] - box[0] + 1) * (box[3] - box[2] + 1) * (box[5] - box[4] + 1)


# Get the overlapping coordinates
def get_overlap(a, b):
    min_x = max(a[0], b[0])
    max_x = min(a[1], b[1])
    min_y = max(a[2], b[2])
    max_y = min(a[3], b[3])
    min_z = max(a[4], b[4])
    max_z = min(a[5], b[5])
    # Make sure the cube is valid
    if min_x <= max_x and min_y <= max_y and min_z <= max_z:
        return min_x, max_x, min_y, max_y, min_z, max_z
    return None


def get_volume(instructions):
    total = 0
    already_counted = list()
    # Iterate over the instructions
    for instr in reversed(instructions):
        cmd = instr[0]
        cube = instr[1:]
        if cmd == 'on':
            overlap = list()
            # Get the overlap with each already covered cube
            for overlapping in [get_overlap(cube, c) for c in already_counted]:
                if overlapping:
                    overlap.append(['on', *overlapping])
            # Get total volume of the overlapping cube
            overcount = get_volume(overlap)
            # Subtract the overlap and add the cube
            total += get_direct(cube)
            total -= overcount
        # Always add to the covered area
        already_counted.append(cube)
    return total


# Start of script
file = open("input.txt", "r")
size = 102

# initialize variables
input_file = [line.strip() for line in file.readlines()]

# Initialize the grid
grid = np.zeros((size, size, size), dtype=int)
grid2 = 0
current_on_lights = list()
text = list()
for line in input_file:
    cmd, ranges = line.split()
    indices = re.split(r"[|,=..]", ranges)
    x_start = int(indices[1])
    x_end = int(indices[3])
    y_start = int(indices[5])
    y_end = int(indices[7])
    z_start = int(indices[9])
    z_end = int(indices[11])
    text.append([cmd, x_start, x_end, y_start, y_end, z_start, z_end])

print(text)


res = get_volume(text)
print(res)

# print results
print("Day 22")
print()

file.close()
