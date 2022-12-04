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


# Start of script
file = open("input.txt", "r")


# Parse the file
start = file.readline().strip()
file.readline()
polymers = defaultdict(str)  # The mapping to new insertions
polymer_counts = defaultdict(int)  # The counts of each pair
for line in file:
    instr = line.strip().split(' -> ')
    polymers[instr[0]] = instr[1]
    polymer_counts[instr[0]] = 0


# Part 1 (for legacy sake)
#curr_mol = start
#for i in range(40):
#    new_chars = list()
#    for j in range(1, len(curr_mol)):
#        new_chars.append(polymers[curr_mol[j-1:j+1]])
#    print(new_chars)
#    # Insert into the string
#    for k in range(len(new_chars), 0, -1):
#        curr_mol = curr_mol[:k] + new_chars[k-1] + curr_mol[k:]
#    print(curr_mol)
#    print(i)
#    print()

# Figure out the starting counts
for i in range(1, len(start)):
    polymer_counts[start[i-1:i+1]] += 1

for i in range(40):
    new_polymers = defaultdict(int)
    for key in polymer_counts.keys():
        # Get the new pairs
        new_A = ''.join([key[0], polymers[key]])
        new_B = ''.join([polymers[key], key[1]])

        # Tally up the pair counts
        new_polymers[new_A] += polymer_counts[key]
        new_polymers[new_B] += polymer_counts[key]
    polymer_counts = new_polymers

ans = defaultdict(int)
ans[start[0]] = 1  # Account for the unpaired letters at the start and end
ans[start[-1]] = 1
for key in polymer_counts.keys():
    # Count the number of each letter (ends up double the actual amount because everything is counted 2x)
    ans[key[0]] += polymer_counts[key]
    ans[key[1]] += polymer_counts[key]

letter_count = list(Counter(ans).most_common())

# print results
print("Day 14")
print((letter_count[0][1] - letter_count[-1][1])//2)


file.close()
