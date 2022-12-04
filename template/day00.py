import numpy
import copy
import itertools
import networkx as nx
import string
import re
import math
from collections import defaultdict


# Start of script
file = open("input.txt", "r")

# Split on every space
lines = list()
for line in file:
    lines.append(line.split())



# print results
print("Day 16")
print()

file.close()
