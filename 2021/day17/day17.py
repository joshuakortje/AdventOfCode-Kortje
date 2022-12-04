import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
import binascii
from scipy import ndimage
from functools import lru_cache
from collections import defaultdict
from collections import Counter
from collections import deque


# Get the minimum x velocity to make it a particular distance
def get_min_vel(dist):
    vel = 0
    pos_dist = 0
    while pos_dist < dist:
        vel += 1
        pos_dist += vel
    return vel


# Get the max height you can get with a starting y velocity
def get_max_dist(speed):
    dist = 0
    for i in range(speed + 1):
        dist += i
    return dist


# Start of script
file = open("input.txt", "r")

# Parse the file
text = file.readline().strip().split()
# Get the target locations
x_parts = text[2].split('=')[1].split('..')
x_target = list(range(int(x_parts[0]), int(x_parts[1][:-1])+1))
y_parts = text[3].split('=')[1].split('..')
y_target = list(range(int(y_parts[0]), int(y_parts[1])+1))

# Part 1
y_max = abs(y_target[0] + 1)
print('Part 1')
print(y_max)
height = get_max_dist(y_max)
print(height)
print()

# Part 2
# We need the range of x velocities
min_x_vel = get_min_vel(x_target[0])
max_x_vel = x_target[-1]
pos_x_vel = list(range(min_x_vel, max_x_vel + 1))

# Get the range of possible y velocities
min_y_vel = y_target[0]
max_y_vel = y_max
pos_y_vel = list(range(min_y_vel, max_y_vel + 1))

# Check which solutions work
solutions = 0
for testx, testy in itertools.product(pos_x_vel, pos_y_vel):
    posx = 0
    posy = 0
    while posx < x_target[-1] and posy > y_target[0]:
        # Execute a step
        posx += testx
        posy += testy
        if testx > 0:
            testx -= 1
        testy -= 1
        # Check if we hit the target
        if posx in x_target and posy in y_target:
            solutions += 1
            break


# print results
print("Day 17")
print(solutions)

file.close()
