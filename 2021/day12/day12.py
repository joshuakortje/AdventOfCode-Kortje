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


# The gross function for part 2
# Returns if we will double visit this time, and
# if we have already double visited
# I know, it didn't have to be this bad...
def will_cheat(have_cheated, next_node, prev):
    if have_cheated:
        return False, have_cheated
    if next_node.isupper():
        return False, have_cheated

    if next_node in prev and next_node != 'start':
        # This is the branch where we double visit
        return True, True
    else:
        return False, have_cheated

# Start of script
file = open("input.txt", "r")

# Parse the file
text = list()
for line in file:
    text.append(line.strip().split('-'))

# Make a graph
G = nx.Graph()
for to, fro in text:
    G.add_edge(*(to, fro))

paths = 0
q = list()
q.append(('start', ['start'], False))
# Modified BFS (sort of)
while q:
    node, pred, cheat_yet = q.pop(0)
    for new_node in G[node]:
        # True if we are going to double visit a cave
        cheat_now, cheat = will_cheat(cheat_yet, new_node, pred)
        if new_node == 'end':
            # Found the path
            paths += 1
            #print(pred)
        elif new_node.isupper() or new_node not in pred or cheat_now:
            q.append((new_node, pred + [new_node], cheat))

# print results
print("Day 12")
print(paths)

file.close()
