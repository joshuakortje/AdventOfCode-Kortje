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
from scipy import ndimage
from functools import lru_cache
from collections import defaultdict
from collections import Counter
from collections import deque

# For some reason part 2 takes a long time to run.
# I have narrowed it down to the deepcopy function,
# but there is no way to get around that.


# Cheaper copy function (marginally faster)
def self_copy(tree):
    nodes = tree.values
    new_tree = bt.build(nodes)
    return new_tree


# Parse into a binary tree recursively
def get_tree(tree_txt):
    if len(tree_txt) == 1:
        return bt.Node(int(tree_txt))
    new_root = bt.Node(-1)  # -1 will be invalid
    open_brackets = 0
    for char in range(len(tree_txt)):
        if open_brackets == 1 and tree_txt[char] == ',':
            magic_index = char
            break
        if tree_txt[char] == '[':
            open_brackets += 1
        elif tree_txt[char] == ']':
            open_brackets -= 1

    new_root.left = get_tree(tree_txt[1:magic_index])
    new_root.right = get_tree(tree_txt[magic_index+1:-1])
    return new_root


# Add two numbers (trees) together
def add_trees(left, right):
    new_root = bt.Node(-1)
    new_root.left = left
    new_root.right = right
    return new_root


# Reduce the tree
def reduce(tree):
    while tree.height > 4 or tree.max_node_value > 9:
        if tree.height > 4:
            # Explode
            all_nodes = tree.levels
            leaf = all_nodes[-1][0]
            parent = bt.get_parent(tree, leaf)
            past_par = parent
            new_par = past_par
            # Set the left
            while new_par is not tree:
                new_par = bt.get_parent(tree, past_par)
                if new_par.left is not past_par:
                    target = new_par.left.inorder[-1]
                    target.val += parent.left.val
                    break
                past_par = new_par
            # Set the right
            past_par = parent
            new_par = past_par
            while new_par is not tree:
                new_par = bt.get_parent(tree, past_par)
                if new_par.right is not past_par:
                    target = new_par.right.inorder[0]
                    target.val += parent.right.val
                    break
                past_par = new_par

            parent.val = 0
            parent.left = None
            parent.right = None
        else:
            # Split
            all_nodes = tree.inorder
            for node in all_nodes:
                if node.val > 9:
                    large = node
                    break

            left_val = bt.Node(int(math.floor(large.val / 2)))
            right_val = bt.Node(int(math.ceil(large.val / 2)))
            large.val = -1
            large.left = left_val
            large.right = right_val


# Get the magnitude
def get_mag(tree):
    if tree.val != -1:
        return tree.val

    left = get_mag(tree.left)
    right = get_mag(tree.right)

    return (left * 3) + (right * 2)

# Start of script
file = open("input.txt", "r")

# Parse the file
text = list()
for line in file:
    text.append(get_tree(line.strip()))

# Part 1
#result = text[0]
#for tree in text[1:]:
#    result = add_trees(result, tree)
#    result = reduce(result)


#mag = get_mag(result)
#print(mag)


# Find the largest sum
poss_mags = list()
pos_idx = list(itertools.product(list(range(len(text))), repeat=2))
for idx_1, idx_2 in pos_idx:
    if idx_1 != idx_2:
        res = add_trees(self_copy(text[idx_1]), self_copy(text[idx_2]))
        reduce(res)
        poss_mags.append(get_mag(res))



# print results
print("Day 18")
print(max(poss_mags))

file.close()
