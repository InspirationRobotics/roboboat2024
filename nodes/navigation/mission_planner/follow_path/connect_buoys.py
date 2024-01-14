from cmath import inf
from turtle import pos
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import six

import sys
from starAlgorithm.starUtils import *

from sys import maxsize
from itertools import permutations
import itertools

# traveling salesperson function provided by geeksforgeeks
# implementation of traveling Salesman Problem
def travelling_salesman(graph, s):
    V = np.shape(graph)[0]-1

    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)
 
    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    best_path = tuple(np.zeros((1,V)))

    next_permutation=permutations(vertex)
    for i in next_permutation:
        # store current Path weight(cost)
        current_pathweight = 0
 
        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]
        # update minimum
        if(current_pathweight < min_path):
            min_path = min(min_path, current_pathweight)
            best_path = i

    return best_path

def set_for_salesman(buoys):
    """
    Implement the costs for the traveling salesman algorithm by calculating eucledian distance
    of the buoys

    Keyword arguments:
    buoys: location in the map of the buoys
    green_red: what color they are(probably remove)
    """
    #extract only the wanted permutations
    possible_pairings = permutations(range(len(buoys)),2)
    buoy_matrix = np.zeros((len(buoys)+1,len(buoys)+1))
    unique_permutations = []
    k = 0
    for i in possible_pairings:
        if i[0] < i[1]:
            unique_permutations.append(i)
            k = k+1
    k = 0

    #
    for i in unique_permutations:
        euc_dist = np.linalg.norm(buoys[i[0]].location - buoys[i[1]].location)
        buoy_matrix[i[0]][i[1]] = euc_dist
        buoy_matrix[i[1]][i[0]] = euc_dist
        k = k+1
        pass

    for i in range(1,len(buoy_matrix[:,-1])-2):
        buoy_matrix[-1][i] = 1000
        buoy_matrix[i][-1] = 1000

    return buoy_matrix


def connect_the_buoys(grid_map, bouyes_loc):
    """
    Runs traveling salesman algorithm and then adds  path onto gridmap

    Keyword arguments:
    grid_map: binary ocuppancy map
    buoys_loc: floating_objects in the map of the buoys
    """
    #runs traveling salesman algorithm with start and end points
    correct_set = set_for_salesman(bouyes_loc)
    organic_path = travelling_salesman(correct_set,0)
    organic_path = list(organic_path)
    organic_path = list(itertools.chain.from_iterable([[0], organic_path]))

    # creates direct path from one point to another and adds it to themap
    for i in range(len(organic_path)-1):
        x = bresenham2D(bouyes_loc[organic_path[i]].location[0], bouyes_loc[organic_path[i]].location[1],\
            bouyes_loc[organic_path[i+1]].location[0], bouyes_loc[organic_path[i+1]].location[1])
            
        if(np.shape(x)[1]>1):
            for j in range(np.shape(x)[1]):
                grid_map[int(x[0,j])][int(x[1,j])] = 1
        else:
            grid_map[int(x[0])][int(x[1])] = 1

    return grid_map