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


all_letters = set('abcdefg')


def sort_string(str_in):
    return ''.join(sorted(str_in))


def list_to_num(digits):
    strs = [str(integer) for integer in digits]
    return int(''.join(strs))

# Start of script
file = open("input.txt", "r")

# Parse the file
text = list()
for line in file:
    combinations, code = line.split('|')
    combinations = [sort_string(x) for x in combinations.strip().split()]
    code = [sort_string(x) for x in code.strip().split()]
    text.append((combinations, code))


decodings = list()
for screen in text:
    mapping = defaultdict(int)
    rev_map = defaultdict(str)
    # Find the 4 digits that are we know based off length
    for num in screen[0]:
        if len(num) == 2:
            mapping[num] = 1
            rev_map[1] = num
        elif len(num) == 3:
            mapping[num] = 7
            rev_map[7] = num
        elif len(num) == 4:
            mapping[num] = 4
            rev_map[4] = num
        elif len(num) == 7:
            mapping[num] = 8
            rev_map[8] = num

    for num in screen[0]:
        if num not in mapping:
            if len(num) == 6:
                off_letters = all_letters - set(num)
                letter = off_letters.pop()
                if letter in rev_map[1]:
                    rev_map[6] = num
                    mapping[num] = 6
                elif letter in rev_map[4]:
                    rev_map[0] = num
                    mapping[num] = 0
                else:
                    rev_map[9] = num
                    mapping[num] = 9

    for num in screen[0]:
        if num not in mapping:
            off_letters = list(all_letters - set(num))
            if off_letters[0] not in rev_map[1] and off_letters[1] not in rev_map[1]:
                rev_map[3] = num
                mapping[num] = 3
            elif off_letters[0] in rev_map[9] and off_letters[1] in rev_map[9]:
                rev_map[2] = num
                mapping[num] = 2
            else:
                rev_map[5] = num
                mapping[num] = 5

    decodings.append([mapping, screen])


# Part 1
easy_instances = 0
for num_map, screen in decodings:
    for num in screen[1]:
        if num in num_map:
            easy_instances += 1

#print(easy_instances)

# Part 2
code_sum = 0
for num_map, screen in decodings:
    code = list()
    for num in screen[1]:
        code.append(num_map[num])
    code_sum += list_to_num(code)

print(code_sum)

# print results
print("Day 8")
print()

file.close()
