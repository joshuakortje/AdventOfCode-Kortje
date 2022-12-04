import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
import binascii
from scipy import ndimage
from functools import lru_cache
from collections import defaultdict
from collections import Counter
from collections import deque

# Not great code... but it works

# Get the literal
def parse_literal(num, idx):
    bits_read = 0
    val = ''
    while True:
        val += num[idx+bits_read+1:idx+bits_read+5]
        if num[idx + bits_read] != '1':
            break
        bits_read += 5
    bits_read += 5
    num_val = int(val, 2)

    return idx + bits_read, num_val


def parse_operation_len(num, idx, bit_len):
    num_list = list()
    sub_tot = 0
    curr_idx = idx
    while curr_idx - idx != bit_len:
        version = int(num[curr_idx:curr_idx + 3], 2)
        type_id = int(num[curr_idx + 3:curr_idx + 6], 2)
        sub_tot += version
        if type_id == 4:
            curr_idx, number = parse_literal(num, curr_idx + 6)
        else:
            sub_sum, curr_idx, number = parse_operator(num, curr_idx, type_id)
            sub_tot += sub_sum
        num_list.append(number)
    return sub_tot, curr_idx, num_list


def parse_operation_pack(num, idx, num_pks):
    num_list = list()
    passed_pks = 0
    sub_tot = 0
    while passed_pks < num_pks:
        passed_pks += 1
        version = int(num[idx:idx + 3], 2)
        type_id = int(num[idx + 3:idx + 6], 2)
        sub_tot += version
        if type_id == 4:
            idx, number = parse_literal(num, idx + 6)
        else:
            sub_sum, idx, number = parse_operator(num, idx, type_id)
            sub_tot += sub_sum
        num_list.append(number)
    return sub_tot, idx, num_list


def parse_operator(num, idx, op):
    i_bit = num[idx + 6]
    if i_bit != '1':
        l = int(num[idx + 7:idx + 7 + 15], 2)
        sub_sum, idx, operands = parse_operation_len(num, idx + 7 + 15, l)
    else:
        packs = int(num[idx + 7:idx + 7 + 11], 2)
        sub_sum, idx, operands = parse_operation_pack(num, idx + 7 + 11, packs)

    # Now that we have the operands, perform the operation
    res = 0
    if op == 0:
        res = sum(operands)
    elif op == 1:
        #res = np.prod(operands) # This doesn't work. I think numpy overflows
        res = 1
        for n in operands:
            res *= n
    elif op == 2:
        res = min(operands)
    elif op == 3:
        res = max(operands)
    elif op == 5:
        res = 1 if operands[0] > operands[1] else 0
    elif op == 6:
        res = 1 if operands[0] < operands[1] else 0
    elif op == 7:
        res = 1 if operands[0] == operands[1] else 0
    else:
        print("ERROR!!!")
        print(op)
    return sub_sum, idx, res

# Start of script
file = open("input.txt", "r")

# Parse the file
text = file.readline().strip()
bin_string = (bin(int(text, 16))[2:]).zfill(len(text)*4)
print(text)
print(bin_string)

index = 0
end = len(bin_string)
running_total = 0
while index + 3 < end:
    # Parse the header
    version = int(bin_string[index:index+3], 2)
    type_id = int(bin_string[index+3:index+6], 2)
    running_total += version
    if type_id == 4:
        # This should never happen here (I hope...)
        index, number = parse_literal(bin_string, index+6)
    else:
        sub_sum, index, answer = parse_operator(bin_string, index, type_id)
        running_total += sub_sum

    if end - index < 20 and index != end:
        if int(bin_string[index:], 2) == 0:
            break


# print results
print("Day 16")
print(running_total)
print(answer)


file.close()
