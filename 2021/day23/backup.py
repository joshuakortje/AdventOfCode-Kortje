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


# Costs associated with moving
costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
# Entryways to rooms (Anthropods can't stay here and must move)
entryways = {(1, 3), (1, 5), (1, 7), (1, 9)}
# Valid room dictionary
valid_room = {'A': 3, 'B': 5, 'C': 7, 'D': 9, '.': -1}
doors = {(2, 3), (2, 5), (2, 7), (2, 9)}
hallway = [1, 2, 4, 6, 8, 10, 11]


class Node:
    
    def __init__(self, grid, cost):
        self.grid = grid
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost


# Pretty print function for ease of viewing
def pretty_print(b):
    pretty = [''.join(l) for l in b]
    for line in pretty:
        print(line)
    print()


# Get adjacent open spaces
def get_open_spaces(b, x, y):
    valid = list()
    anth = b[x][y]
    for n_x, n_y in itertools.product((0, 0), (-1, 1)):
        new_x, new_y = x + n_x, y + n_y
        # Rule 2: No moving into rooms that are not your own and
        # only move into your room if no other type is in that room
        # x == 1 means we only check when standing in the entryway
        if x == 1 and new_x == 2:
            if y != valid_room[anth]:
                # Not the right room (Rule 2a)
                continue
            if b[3][y] != '.' and b[3][y] != anth:
                # Occupied by a different kind already
                continue
        if b[new_x][new_y] == '.':
            valid.append((new_x, new_y))
    return valid


# Check if a given amphipod can go to the correct room
def check_finish(b, y):
    amph = b[1][y]
    home = valid_room[amph]
    if b[2][home] == '.' and (b[3][home] == '.' or b[3][home] == amph):
        # The room is empty or has valid occupants
        direction = 1 if home > y else -1
        for path in range(y + direction, home + direction, direction):
            if b[1][path] != '.':
                # Someone blocking the way
                return False, -1, (-1, -1)
        # If we made it this far we can make it. Return True and the total energy it would take
        # as well as the landing space
        spaces = abs(home - y) + 1
        if b[3][home] == '.':
            spaces += 1
            loc = (3, home)
        else:
            loc = (2, home)
        return True, spaces, loc
    return False, -1, (-1, -1)


# Get all the next possible states, trimming the states we have already visited
def get_next_boards(energy, state, last, visited, visit_cost):
    new_boards = list()
    # Rule 1: Never stand outside the rooms
    for ent_x, ent_y in entryways:
        if state[ent_x][ent_y] != '.':
            #pretty_print(state)
            new_energy = energy + costs[state[ent_x][ent_y]]
            for open_x, open_y in get_open_spaces(state, ent_x, ent_y):
                # Move
                new_state = list(map(list, state))
                new_state[open_x][open_y] = state[ent_x][ent_y]
                new_state[ent_x][ent_y] = '.'
                if tuple(map(tuple, new_state)) not in visited:
                    visited.add(tuple(map(tuple, new_state)))
                    visit_cost[tuple(map(tuple, new_state))] = new_energy
                    #pretty_print(new_state)
                    new_boards.append((new_energy, tuple(map(tuple, new_state)), (open_x, open_y)))
                #else:
                #    if new_energy < visit_cost[tuple(map(tuple, new_state))]:
                #        visit_cost[tuple(map(tuple, new_state))] = new_energy
                #        # pretty_print(new_state)
                #        new_boards.append((new_energy, tuple(map(tuple, new_state)), (open_x, open_y)))

            # We can return now because those were the only valid moves
            return new_boards

    # Check if anyone can finish up (Rule 3) and do it all in one turn
    for y in range(1, len(state[0]) - 1):
        if state[1][y] != '.':
            #pretty_print(state)
            # Check if they can finish
            can_fin, spaces, final_loc = check_finish(state, y)
            if can_fin:
                new_energy = energy + (spaces * costs[state[1][y]])
                new_state = list(map(list, state))
                new_state[final_loc[0]][final_loc[1]] = state[1][y]
                new_state[1][y] = '.'
                if tuple(map(tuple, new_state)) not in visited:
                    visited.add(tuple(map(tuple, new_state)))
                    visit_cost[tuple(map(tuple, new_state))] = new_energy
                    new_boards.append((new_energy, tuple(map(tuple, new_state)), None))
                #else:
                #    if new_energy < visit_cost[tuple(map(tuple, new_state))]:
                #        visit_cost[tuple(map(tuple, new_state))] = new_energy
                #        # pretty_print(new_state)
                #        new_boards.append((new_energy, tuple(map(tuple, new_state)), None))

    # Check if we can move the last person
    # If last is None, we just put a piece in the right room
    if last:
        for open_x, open_y in get_open_spaces(state, last[0], last[1]):
            #pretty_print(state)
            new_state = list(map(list, state))
            new_state[open_x][open_y] = state[last[0]][last[1]]
            new_state[last[0]][last[1]] = '.'
            if tuple(map(tuple, new_state)) not in visited:
                #pretty_print(new_state)
                visited.add(tuple(map(tuple, new_state)))
                visit_cost[tuple(map(tuple, new_state))] = energy + costs[state[last[0]][last[1]]]
                new_boards.append((energy + costs[state[last[0]][last[1]]], tuple(map(tuple, new_state)), (open_x, open_y)))
            #else:
            #    if (energy + costs[state[last[0]][last[1]]]) < visit_cost[tuple(map(tuple, new_state))]:
            #        # pretty_print(new_state)
            #        visited.add(tuple(map(tuple, new_state)))
            #        visit_cost[tuple(map(tuple, new_state))] = energy + costs[state[last[0]][last[1]]]
            #        new_boards.append((energy + costs[state[last[0]][last[1]]], tuple(map(tuple, new_state)),
            #                           (open_x, open_y)))

    # Check if we can move a new one out
    for door_x, door_y in doors:
        if state[door_x][door_y] == '.':
            # Check the one below
            if state[door_x + 1][door_y] != '.' and valid_room[state[door_x + 1][door_y]] != door_y:
                # This one can move up only
                #pretty_print(state)
                new_state = list(map(list, state))
                new_state[door_x][door_y] = state[door_x + 1][door_y]
                new_state[door_x + 1][door_y] = '.'
                if tuple(map(tuple, new_state)) not in visited:
                    #pretty_print(new_state)
                    visited.add(tuple(map(tuple, new_state)))
                    visit_cost[tuple(map(tuple, new_state))] = energy + costs[state[door_x + 1][door_y]]
                    new_boards.append((energy + costs[state[door_x + 1][door_y]], tuple(map(tuple, new_state)), (door_x, door_y)))
                #else:
                #    if energy + costs[state[door_x + 1][door_y]] < visit_cost[tuple(map(tuple, new_state))]:
                #        #pretty_print(new_state)
                #        visited.add(tuple(map(tuple, new_state)))
                #        visit_cost[tuple(map(tuple, new_state))] = energy + costs[state[door_x + 1][door_y]]
                #        new_boards.append((energy + costs[state[door_x + 1][door_y]], tuple(map(tuple, new_state)),
                #                           (door_x, door_y)))
        else:
            # If the threshold of the room is occupied
            if valid_room[state[door_x][door_y]] != door_y or valid_room[state[door_x + 1][door_y]] != door_y:
                # Again, he can only move up
                #pretty_print(state)
                new_state = list(map(list, state))
                new_state[door_x - 1][door_y] = state[door_x][door_y]
                new_state[door_x][door_y] = '.'
                if tuple(map(tuple, new_state)) not in visited:
                    #pretty_print(new_state)
                    visited.add(tuple(map(tuple, new_state)))
                    visit_cost[tuple(map(tuple, new_state))] = energy + costs[state[door_x][door_y]]
                    new_boards.append((energy + costs[state[door_x][door_y]], tuple(map(tuple, new_state)), (door_x - 1, door_y)))
                #else:
                #    if energy + costs[state[door_x][door_y]] < visit_cost[tuple(map(tuple, new_state))]:
                #        # pretty_print(new_state)
                #        visited.add(tuple(map(tuple, new_state)))
                #        visit_cost[tuple(map(tuple, new_state))] = energy + costs[state[door_x][door_y]]
                #        new_boards.append((energy + costs[state[door_x][door_y]], tuple(map(tuple, new_state)),
                #                           (door_x - 1, door_y)))
    return new_boards


# Use Dijkstra
def dijkstra(start):



# Uses BFS with a PriorityQ to find the minimum energy in the final state
def get_min_energy(q, visited, visited_cost):
    i = 0
    while q:
        if i % 20000 == 0:
            print(i)
        i += 1
        curr_score, curr_board, last_spot = heapq.heappop(q)
        # Check if finished
        if curr_board in end_res_set:
            # Solved (Found the end result)
            return curr_score
        # Get the next possible states and add them to our heapq
        next_boards = get_next_boards(curr_score, curr_board, last_spot, visited, visited_cost)
        if next_boards:
            q.extend(next_boards)
            heapq.heapify(q)

    # We only reach this upon error
    return -1


# Start of script
file = open("input.txt", "r")
ans_file = open("answer.txt", "r")


# initialize variables
board = [list(a) for a in [line.strip() for line in file.readlines()]]
end_result = [list(a) for a in [line.strip() for line in ans_file.readlines()]]

# Put in a set to speed up checking equality
end_res_set = set()
end_res_set.add(tuple(map(tuple, end_result)))

visited_states = set()
visited_states.add(tuple(map(tuple, board)))
visited_cost = defaultdict(int)
visited_cost[tuple(map(tuple, board))] = 0
heap = []
heapq.heappush(heap, (0, tuple(map(tuple, board)), None))

ans = get_min_energy(heap, visited_states, visited_cost)
print(ans)

# print results
print("Day 23")
print()

file.close()
