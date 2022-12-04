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
text = list()
for line in file:
    text.append(line.strip())


def find_ones(array):
    total_nums = len(array)
    num_ones = [0] * len(array[0])
    for num in array:
        for i in range(len(num)):
            if num[i] == '1':
                num_ones[i] += 1

    gamma = ''
    epsilon = ''
    for res in num_ones:
        if res >= total_nums/2:
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'
    return gamma, epsilon


gamma, epsilon = find_ones(text)

int_gamma = int(gamma, 2)
int_epsilon = int(epsilon, 2)

# Part 2
oxy_nums = text.copy()
i = 0
while len(oxy_nums) > 1:
    new_gamma, new_epsilon = find_ones(oxy_nums)
    oxy_nums = list(filter(lambda x: x[i] == new_gamma[i], oxy_nums))
    i += 1

co2_nums = text.copy()
i = 0
while len(co2_nums) > 1:
    new_gamma, new_epsilon = find_ones(co2_nums)
    co2_nums = list(filter(lambda x: x[i] == new_epsilon[i], co2_nums))
    i += 1

int_oxy = int(oxy_nums[0], 2)
int_co2 = int(co2_nums[0], 2)

# print results
print("Day 3")
print(int_gamma * int_epsilon)
print(int_oxy * int_co2)

file.close()
