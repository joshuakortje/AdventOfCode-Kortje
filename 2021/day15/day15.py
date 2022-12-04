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

max = 0  # Defined later

class Cost:
    def __init__(self, num, x, y):
        self.cost = num
        self.x = x
        self.y = y

        n = list()
        if self.x > 0:
            n.append((self.x-1, self.y))
        if self.y > 0:
            n.append((self.x, self.y-1))
        if self.x < max:
            n.append((self.x+1, self.y))
        if self.y < max:
            n.append((self.x, self.y+1))
        self.neighbors = n

    def __lt__(self, nxt):
        return self.cost < nxt.cost

    def get_neighbors(self):
        return self.neighbors


def dijkstra(w, cost):
    # Start at (0, 0)
    cost[0][0].cost = 0
    cost[0][1].cost = w[0][1]
    cost[1][0].cost = w[1][0]

    explored = set()

    # Add all the nodes to the heap
    heap = list()
    heapq.heappush(heap, cost[0][0])
    heapq.heappush(heap, cost[0][1])
    heapq.heappush(heap, cost[1][0])
    explored.add((0, 0))
    explored.add((1, 0))
    explored.add((0, 1))
    #for node_list in cost:
    #    for node in node_list:
    #        heapq.heappush(heap, node)
        
    while heap:
        u = heapq.heappop(heap)
        for v in u.get_neighbors():
            if cost[v[0]][v[1]].cost > cost[u.x][u.y].cost + w[v[0]][v[1]]:
                cost[v[0]][v[1]].cost = cost[u.x][u.y].cost + w[v[0]][v[1]]
                if v not in explored:
                    explored.add(v)
                    heapq.heappush(heap, cost[v[0]][v[1]])
        heapq.heapify(heap)


# Start of script
file = open("input.txt", "r")


# Parse the file
text = [[] for i in range(10)]
for line in file:
    text[0].append([int(x) for x in line.strip()])
    text[1].append([(int(x)-1 + 1) % 9 + 1 for x in line.strip()])
    text[2].append([(int(x)-1 + 2) % 9 + 1 for x in line.strip()])
    text[3].append([(int(x)-1 + 3) % 9 + 1 for x in line.strip()])
    text[4].append([(int(x)-1 + 4) % 9 + 1 for x in line.strip()])


print(text)
start = np.concatenate((np.array(text[0]), np.array(text[1]), np.array(text[2]), np.array(text[3]), np.array(text[4])))
start1 = (start - 1 + 1) % 9 + 1
start2 = (start - 1 + 2) % 9 + 1
start3 = (start - 1 + 3) % 9 + 1
start4 = (start - 1 + 4) % 9 + 1
master = np.concatenate((start, start1, start2, start3, start4), axis=1)

text = master.tolist()
costs = copy.deepcopy(text)
max = len(text)-1
for i in range(len(text)):
    for j in range(len(text[0])):
        costs[i][j] = Cost(1000000, i, j)

print(costs)

# Implement Dijkstra
dijkstra(text, costs)
print(costs[max][max].cost)

# print results
print("Day 15")
print()


file.close()
