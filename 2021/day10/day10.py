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
text = list()
for line in file:
    text.append([x for x in line.strip()])

# Key for point values
key = defaultdict(int)
key[')'] = 3
key[']'] = 57
key['}'] = 1197
key['>'] = 25137
opposite = defaultdict(str)
opposite['('] = ')'
opposite['['] = ']'
opposite['{'] = '}'
opposite['<'] = '>'
close_key = defaultdict(int)
close_key['('] = 1
close_key['['] = 2
close_key['{'] = 3
close_key['<'] = 4

stack = deque()
error_score = 0
mismatch = False
incomplete_scores = list()
for line in text:
    stack.clear()
    for char in line:
        if char in opposite:
            stack.append(char)
        else:
            opener = stack.pop()
            if char != opposite[opener]:
                mismatch = True
                error_score += key[char]
                break
    if mismatch:
        mismatch = False
    else:
        # Incomplete lines (Part 2)
        score = 0
        while len(stack) > 0:
            opener = stack.pop()
            score = score * 5 + close_key[opener]
        incomplete_scores.append(score)

incomplete_scores = sorted(incomplete_scores)
win_index = (len(incomplete_scores)-1)//2

# print results
print("Day 10")
print(error_score)
print(incomplete_scores[win_index])

file.close()
