from cell import Cell
from desease import Desease
from map_r import Map

from itertools import product
from random import shuffle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import pandas as pd

SUSCEPTIBLE = "S"
INFECTIOUS = "I"
RECOVERED = "R"

def printable_matrix(map_m, grid_size):
    universe = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            state = map_m.map[(i, j)].state
            if state == "S": 
                int_state = 0
            elif state == "I": 
                int_state = 1
            else:
                int_state = 2
            universe[i,j] = int_state
    return universe


def fullfill_map(x_len, y_len, s_ratio):
    possible_positions = list(product(range(x_len), range(y_len)))
    shuffle(possible_positions)
    population = len(possible_positions)
    susceptibles = [Cell(SUSCEPTIBLE, *i) for i in possible_positions[:(int(population*s_ratio))]]
    infecteds = [Cell(INFECTIOUS, *i) for i in possible_positions[(int(population*s_ratio)):]]
    return susceptibles, infecteds


grid_size = 50
s_ratio = 0.85

susceptibles, infecteds = fullfill_map(grid_size, grid_size, s_ratio)

neighborhood_function = Desease.r_1

cells = susceptibles + infecteds
desease = Desease(4, 10, neighborhood_function, 2)

map_1 = Map(grid_size, grid_size, cells, desease)

fig = plt.figure()


def update_matrix(i):
    global map_1, grid_size
    map_1.next_t()
    matrix = printable_matrix(map_1, grid_size)
    plt.cla()
    im = plt.imshow(matrix)
    return [im]

ani = animation.FuncAnimation(fig, update_matrix, interval=50, blit=True)
plt.show()


