from itertools import product

class Desease:
    def __init__(self, contamination_number, infection_duration, spread_function):
        self.contamination_number = contamination_number
        self.infection_duration = infection_duration
        self.spread_function = spread_function

    
    def neighborhood_1(self, i, j):
        position_tuple = [(i-1, i, i+1), (j-1, j, j+1)]
        combined_positions = list(product(position_tuple[0], position_tuple[1]))
        return combined_positions

    def cholera_neighborhood(self, i, j):
        position_tuple = [(i-2, i-1, i, i+1, i+2), (j-2, j-1, j, j+1, j+2)]
        combined_positions = list(product(position_tuple[0], position_tuple[1]))
        return combined_positions