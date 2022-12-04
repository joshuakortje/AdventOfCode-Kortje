import numpy as np
import copy
import itertools
import networkx as nx
import string
import re
import math
import heapq
import binascii
import binarytree as bt
from scipy import spatial
from scipy import ndimage
from functools import lru_cache
from collections import defaultdict
from collections import Counter
from collections import deque

# NOTE: Not necessary to keep track of the players turn
# Better to use recursion and memoization. Use a function like
# @functools.lru_cache(maxsize=None)
# wins, losses = play(curr_player, otherplayer, curr_score, other_score)
# with a base case:
# if curr_score >= 21:
#   return 1, 0
# elif other_score >= 21
#   return 0, 1
# And the other cases use a for loop to iterate over the new game possibilities

# Starting values for the player places and the die
start1 = 7
start2 = 6
die = 1
die_rolls = 0
spaces = [start1-1, start2-1]
scores = [0, 0]
player = 0

# Part 1
#while max(scores) < 1000:
#    dist = (die % 100) + ((die + 1) % 100) + ((die + 2) % 100)
#    die = (die + 3) % 100
#    die_rolls += 3
#    spaces[player] = (spaces[player] + dist) % 10
#    scores[player] += spaces[player] + 1
#    player = 1 if player == 0 else 0
#
#ans = min(scores) * die_rolls
#print(ans)

# Part 2
# Possible combos for the player's scores
combos = list(itertools.product(range(0, 21), repeat=2))
all_combos = list()
for c in combos:
    # False-> Player 1's turn, True -> Player 2's turn
    # Account for the different spaces and for the
    # spaces the players might be on
    for a, b in itertools.product(range(10), repeat=2):
        all_combos.append(c + (True, a, b))
        all_combos.append(c + (False, a, b))
# We need to sort so we go through the game states in the right order
all_combos = sorted(all_combos)

# Initialize with the first game
games = defaultdict(int)
games[(0, 0, False) + tuple(spaces)] = 1

# Use dynamic programming to build up the game possibilities
for space_pair in all_combos:
    curr_games = games[space_pair]
    # If there are games do the algorithm
    if curr_games != 0:
        new_games = list()
        # Get all the possible offsets (distances moved)
        offset = [sum(x) for x in list(itertools.product((1, 2, 3), repeat=3))]
        if not space_pair[2]:
            # Player 1
            for off in offset:
                # Get the number of points to be added to the score
                new_points = space_pair[0] + ((space_pair[3] + off) % 10) + 1
                new_games.append((new_points, space_pair[1], not space_pair[2], (space_pair[3] + off) % 10, space_pair[4] % 10))
        else:
            # Player 2
            for off in offset:
                # Get the number of points to be added to the score
                new_points = space_pair[1] + ((space_pair[4] + off) % 10) + 1
                new_games.append((space_pair[0], new_points, not space_pair[2], space_pair[3] % 10, (space_pair[4] + off) % 10))
        # Perpetuate the game possibilities into the pool
        for inst in new_games:
            games[inst] += curr_games

player1_win = 0
player2_win = 0
for end in games.keys():
    if end[0] >= 21:
        player1_win += games[end]
    elif end[1] >= 21:
        player2_win += games[end]

print(player1_win)
print(player2_win)

# print results
print("Day 21")
print()

