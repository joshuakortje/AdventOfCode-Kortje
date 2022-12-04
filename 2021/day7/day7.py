import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
from functools import lru_cache
from collections import defaultdict
from collections import Counter


# Use memoization
@lru_cache(maxsize=5000)
def get_energy(dist):
    # The commented out code works just fine
    # but is noticably slower
    #energy = 0
    #for i in range(1, dist + 1):
    #    energy += i
    #
    #return energy

    # This is the fastest implementation I found
    if dist == 0:
        return 0
    if dist == 1:
        return 1
    else:
        return dist + get_energy(dist - 1)


# Start of script
file = open("input.txt", "r")

# Parse the file
text = [int(x) for x in file.readline().strip().split(',')]

last_energy = 10000000000
# Only need to go until we hit the min
# After that it just goes up
for pos in range(len(text)):
    total_energy = 0
    for crab in text:
        total_energy += abs(crab - pos)
    if total_energy <= last_energy:
        last_energy = total_energy
    else:
        break

print("Part 1")
print(last_energy)
print(max(text))

# Hacky, but this helps initialize the cache so we don't overflow the call stack
init = get_energy(400)
init = get_energy(800)

# Part 2
last_energy = 10000000000
# Only need to go until we hit the min
# After that it just goes up
for pos in range(len(text)):
    total_energy = 0
    for crab in text:
        added_energy = get_energy(abs(crab - pos))
        total_energy += added_energy
    if total_energy <= last_energy:
        last_energy = total_energy
    else:
        break

print("Part 2")
print(last_energy)

# print results
print("Day 7")
print()

file.close()
