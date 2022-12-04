import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
from collections import defaultdict


# Start of script
file = open("input.txt", "r")

# Split on every space
depth = 0
dist = 0
aim = 0
lines = list()
for line in file:
    instr, num = line.strip().split()
    lines.append((instr, (int(num))))

for text in lines:
    word, change = text[0], text[1]
    if word == 'forward':
        dist += change
        depth += aim*change
    elif word == 'up':
        aim -= change
    elif word == 'down':
        aim += change

print(depth)
print(dist)

# print results
print("Day 2")
print(depth * dist)

file.close()
