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
import cProfile
import pandas as pd


# NOTE: Super inefficient. Looks like a lot of people sped it up by
# only keeping the hallway and rooms and just having separate lists for them.
def day23():
    # Costs associated with moving
    costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    # Entryways to rooms (Amphipods can't stay here and must move)
    entryways = {3, 5, 7, 9}
    # Valid room dictionary
    valid_room = {'A': 3, 'B': 5, 'C': 7, 'D': 9, '.': -1}
    valid_pod = {3: 'A', 5: 'B', 7: 'C', 9: 'D'}
    doors = {(2, 3), (2, 5), (2, 7), (2, 9)}
    hallway = [1, 2, 4, 6, 8, 10, 11]
    depth = 4


    class Node:

        def __init__(self, grid, cost):
            self.grid = grid
            self.cost = cost
            if grid:
                self.key = tuple(map(tuple, grid))
            else:
                self.key = None

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


    # Returns clear, top
    # where clear indicates if the room is ready to be filled
    # and top indicates the location of the first amphipod to move
    # where clear is false
    def check_room(b, y):
        goal = valid_pod[y]
        col = [row[y] for row in b]
        room = col[2:depth + 2]
        clear = True
        for r in room:
            if not(r == goal or r == '.'):
                clear = False

        top = depth + 2
        for i in range(len(room)):
            if room[i] != '.':
                top = i + 2
                break

        return clear, top

    # Check if a given amphipod can go to the correct room
    # Return can_fin, spaces, loc
    def check_finish(b, y):
        amph = b[1][y]
        home = valid_room[amph]
        can_fin, top = check_room(b, home)
        if not can_fin:
            # Can't finish (room needs to clear)
            return False, -1, (-1, -1)

        # Check if the path is clear
        direction = 1 if home > y else -1
        for path in range(y + direction, home + direction, direction):
            if b[1][path] != '.':
                # Someone blocking the way
                return False, -1, (-1, -1)

        # We can finish if we made it this far
        spaces = abs(home - y) - 1 + top - 1
        loc = (top - 1, home)
        return True, spaces, loc


    # Get the next states of the game that are possible
    def get_next(state):
        next_state = list()

        # Check if we can move anyone to their home
        for y in hallway:
            if state.grid[1][y] != '.':
                can_fin, spaces, final_loc = check_finish(state.grid, y)
                if can_fin:
                    #pretty_print(state.grid)
                    new_cost = state.cost + (spaces * costs[state.grid[1][y]])
                    new_grid = copy.deepcopy(state.grid)
                    new_grid[final_loc[0]][final_loc[1]] = state.grid[1][y]
                    new_grid[1][y] = '.'
                    #pretty_print(new_grid)
                    new_node = Node(new_grid, new_cost)
                    next_state.append(new_node)

        # Check if we can move any more amphipods out
        for y in entryways:
            should_stay, top = check_room(state.grid, y)
            if not should_stay:
                # We should try to move one out
                # Get the avaliable hallway spaces
                hall_spots = list()
                idx = y//2
                # Going left
                for i in range(idx, -1, -1):
                    if state.grid[1][hallway[i]] == '.':
                        hall_spots.append((1, hallway[i]))
                    else:
                        break
                # Going right
                idx += 1
                for i in range(idx, len(hallway), 1):
                    if state.grid[1][hallway[i]] == '.':
                        hall_spots.append((1, hallway[i]))
                    else:
                        break
                # Add all the new states
                for loc in hall_spots:
                    #pretty_print(state.grid)
                    new_cost = state.cost + (top - 1 + abs(loc[1] - y)) * costs[state.grid[top][y]]
                    new_grid = copy.deepcopy(state.grid)
                    new_grid[loc[0]][loc[1]] = state.grid[top][y]
                    new_grid[top][y] = '.'
                    #pretty_print(new_grid)
                    new_node = Node(new_grid, new_cost)
                    next_state.append(new_node)

        return next_state


    # Use Dijkstra (q has already been seeded with the end solution
    def dijkstra(q, start, game_space):
        answer = heapq.heappop(q)
        answer_key = set()
        answer_key.add(tuple(map(tuple, answer.grid)))
        heapq.heappush(q, start)
        i = 0

        while q:
            if i % 5000 == 0:
                print(i)
            i += 1
            # Get next node from the heapq
            u = heapq.heappop(q)
            # Check if we made it
            if u.key in answer_key:
                # Found the end
                pretty_print(u.grid)
                return u.cost
            next_boards = get_next(u)
            for board in next_boards:
                if game_space[board.key].cost:
                    if game_space[board.key].cost > board.cost:
                        # Old board, update the cost if we found a cheaper way
                        game_space[board.key].cost = board.cost
                        heapq.heapify(q)
                else:
                    # New board, add to q and game space
                    heapq.heappush(q, board)
                    game_space[board.key] = board
        # We should never get here
        return -1


    # Start of script
    file = open("input.txt", "r")
    ans_file = open("answer2.txt", "r")


    # initialize variables
    board = [list(a) for a in [line.strip() for line in file.readlines()]]
    end_result = [list(a) for a in [line.strip() for line in ans_file.readlines()]]

    # Put in a set to speed up checking equality
    game_space = defaultdict(lambda: Node(None, None))
    start = Node(board, 0)
    sol = Node(end_result, 1000000000)
    heap = []
    heapq.heappush(heap, sol)


    ans = dijkstra(heap, start, game_space)
    print(ans)

    # print results
    print("Day 23")
    print()

    file.close()


cProfile.run("day23()")
