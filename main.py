from cell import Cell
from desease import Desease
from map_r import Map

from itertools import product
from random import shuffle

import pandas as pd

SUSCEPTIBLE = "S"
INFECTIOUS = "I"
RECOVERED = "R"



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


def fullfill_map(x_len, y_len, s_ratio):
    possible_positions = list(product(range(x_len), range(y_len)))
    shuffle(possible_positions)
    population = len(possible_positions)
    susceptibles = [Cell(SUSCEPTIBLE, *i) for i in possible_positions[:(int(population*s_ratio))]]
    infecteds = [Cell(INFECTIOUS, *i) for i in possible_positions[(int(population*s_ratio)):]]
    return susceptibles, infecteds


if __name__ == "__main__":
    grid_size = 50
    s_ratio = 0.85

    susceptibles, infecteds = fullfill_map(grid_size, grid_size, s_ratio)

    neighborhood_function = Desease.r_1

    cells = susceptibles + infecteds
    desease = Desease(4, 10, neighborhood_function, 2)

    map_1 = Map(grid_size, grid_size, cells, desease)


    while True:
        print_matrix(map_1.map)
        input("press enter to change t")
        map_1.next_t()

