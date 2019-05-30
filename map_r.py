SUSCEPTIBLE = "S"
INFECTIOUS = "I"
RECOVERED = "R"

class Map:
    
    def __init__(self, widht, height, cells, desease):
        self.map = {}
        self.map_b = (widht-1, height-1)
        self.__t = 0
        self.cells = cells
        self.desease = desease
        self.__load_cells(cells)

    def __load_cells(self, cells):
        [self.map.update({cell.position: cell}) for cell in self.cells]
    
    def __get_neighbors(self, cell):

        possible_neighbors = self.desease.spread_function(*(cell.position))
        neighbors = [self.map[pos] for pos in possible_neighbors if pos in self.map]
        return neighbors

    def __count_d_nei(self, neighbors):
        t_list = [1 for nei in neighbors if nei.state == INFECTIOUS]
        return sum(t_list)

    def __get_next_status(self, cell):
        neighbors = self.__get_neighbors(cell)
        c_number = self.desease.contamination_number
        infect_duration = self.desease.infection_duration
        recovered_length = self.desease.recovered_length
        if cell.state == INFECTIOUS and cell.get_counter_state() >= infect_duration:
            cell.next_state = RECOVERED
        elif cell.state == SUSCEPTIBLE and self.__count_d_nei(neighbors) >= c_number:
            cell.next_state = INFECTIOUS
        elif cell.state == RECOVERED and cell.get_counter_state() >= recovered_length:
            cell.next_state = SUSCEPTIBLE
           
    def next_t(self):
        [self.__get_next_status(cell) for cell in self.cells]
        [cell.update_state() for cell in self.cells]
