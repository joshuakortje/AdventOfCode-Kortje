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
lines = list()
for line in file:
    lines.append(int(line.strip()))

bigger = 0
for i in range(3, len(lines)):
    A = sum(lines[(i-3):i])
    B = sum(lines[(i-2):(i+1)])
    # Part 1
    #if lines[i] > lines[i-1]:
    #    bigger += 1

    # Part 2
    if B > A:
        bigger += 1

# print results
print("Day 1")
print(bigger)

file.close()
