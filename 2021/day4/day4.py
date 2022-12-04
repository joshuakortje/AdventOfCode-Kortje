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

# Parse the input
nums_called = [int(x) for x in text[0].split(',')]
grids = list()
grids.append([])
j = 0
for i in range(2, len(text)):
    if text[i] is '':
        j += 1
        grids.append([])
        continue
    else:
        grids[j].append([int(x) for x in text[i].split()])

cards = np.array(grids)


# Remove any called numbers
def call_number(boards, num):
    # Return -1 since it isn't used (yes, I know it is kind of cheating)
    boards[boards == num] = -1


# Check for a win
def check_board(board):
    cols = np.sum(board, axis=0)
    rows = np.sum(board, axis=1)
    if -5 in rows or -5 in cols:
        return True
    return False


# Function to calculate score
def get_score(board, num):
    board[board == -1] = 0
    square = np.sum(board)
    score = num * square
    return score


for number in nums_called:
    # Cross off the numbers
    call_number(cards, number)
    
    # Check for wins
    fin = list()
    for i in range(len(cards)):
        if check_board(cards[i]):
            print("win")
            print(get_score(cards[i], number))
            fin.append(i)
    
    # Remove any finished boards
    if fin:
        cards = np.delete(cards, fin, axis=0)
    if np.size(cards) == 0:
        break

# print results
print("Day 4")
print()

file.close()
