from cell import Cell
from desease import Desease
from map_r import Map

from itertools import product
from random import shuffle

import pandas as pd

SUSCEPTIBLE = "S"
INFECTIOUS = "I"
RECOVERED = "R"

grid_size = 50
population = 1500

s_ratio = 0.7

def print_matrix(map_m):
    matrix = {}
    for x in range(grid_size):
        colum_x = {}
        lista = list(filter(lambda key: key[0] == x, map_m.keys()))
        for i in lista:
            colum_x[i[1] + 1] = map_m[i].state
        matrix[x + 1] = colum_x
    df = pd.DataFrame(matrix)
    print( df.to_string(na_rep="-"))

possible_positions = list(product(range(grid_size), range(grid_size)))
shuffle(possible_positions)
cells_positions = possible_positions[:population]

susceptibles = [Cell(SUSCEPTIBLE, *i) for i in cells_positions[:(int(population*s_ratio))]]
infecteds = [Cell(INFECTIOUS, *i) for i in cells_positions[(int(population*s_ratio)):]]

spread_function = Desease.neighborhood_1

cells = susceptibles + infecteds
desease = Desease(8, 10, spread_function)

map_1 = Map(grid_size, grid_size, cells, desease)


while True:
    print_matrix(map_1.map)
    input("press enter to change t")
    map_1.next_t()

