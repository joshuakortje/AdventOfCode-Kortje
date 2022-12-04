import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
from collections import defaultdict
from collections import Counter


# Part 1 approach
def day_pass(fishes):
    new_fish = []
    for fish in range(len(fishes)):
        if fishes[fish] == 0:
            new_fish.append(8)
            fishes[fish] = 6
        else:
            fishes[fish] -= 1
    fishes[0:0] = new_fish


# Part 2 approach
def lifespan(fishes, time):
    for day in range(time):
        newfish = defaultdict(int)
        for i in range(9):
            if i == 0:
                newfish[8] = fishes[0]
                newfish[6] = fishes[0]
            else:
                newfish[i - 1] += fishes[i]
        fishes = newfish
    print(sum(fishes.values()))


# Start of script
file = open("input.txt", "r")
time_span = 256

# Parse the file
text = [int(x) for x in file.readline().strip().split(',')]

school = defaultdict(int, Counter(text))

lifespan(school, time_span)

# print results
print("Day 6")
print()

file.close()
