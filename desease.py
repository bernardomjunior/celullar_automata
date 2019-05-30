from itertools import product

class Desease:
    def __init__(self, c_number, infect_d, spread_f, r_length):
        self.contamination_number = c_number
        self.infection_duration = infect_d
        self.spread_function = spread_f
        self.recovered_length = r_length

    @staticmethod
    def r_1(i, j):
        position_tuple = [(i-1, i, i+1), (j-1, j, j+1)]
        combined_positions = list(product(position_tuple[0], position_tuple[1]))
        return combined_positions

    @staticmethod
    def r_2(i, j):
        position_tuple = [(i-2, i-1, i, i+1, i+2), (j-2, j-1, j, j+1, j+2)]
        combined_positions = list(product(position_tuple[0], position_tuple[1]))
        return combined_positions