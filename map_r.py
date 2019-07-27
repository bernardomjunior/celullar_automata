SUSCEPTIBLE = "S"
INFECTIOUS = "I"
RECOVERED = "R"

class Map:
    
    def __init__(self, widht, height, cells, desease, sir):
        self.sir = sir
        self.map = {}
        self.map_b = (widht-1, height-1)
        self.__t = 0
        self.cells = cells
        self.desease = desease
        self.__load_cells(cells)

    def __load_cells(self, cells):
        """
        Update map
        """
        [self.map.update({cell.position: cell}) for cell in self.cells]
    
    def __get_neighbors(self, cell):
        """
        Get nearby neighbors cells
        """
        possible_neighbors = self.desease.spread_function(*(cell.position))
        neighbors = [self.map[pos] for pos in possible_neighbors if pos in self.map]
        return neighbors

    def __count_d_nei(self, neighbors):
        """
        Counts the amount of infectious neighbors
        """
        t_list = [1 for nei in neighbors if nei.state == INFECTIOUS]
        return sum(t_list)

    
    def count_infectious_neighbors(self, cell):
        neighbors = self.__get_neighbors(cell)
        t_list = [1 for nei in neighbors if nei.state == INFECTIOUS]
        return sum(t_list)


    def rank_cells(self, cells):
        """
        Rank all cells by class
        """
        infectious = list(filter(lambda cell: cell.next_state == INFECTIOUS, cells))
        susceptible = list(filter(lambda cell: cell.next_state == SUSCEPTIBLE, cells))
        recovered = list(filter(lambda cell: cell.next_state == RECOVERED, cells))
        ranked_infectious = infectious.sort(key=lambda cell: cell.get_counter_state, reverse=True)
        ranked_susceptible = susceptible.sort(key=self.count_infectious_neighbors, reverse=True)
        ranked_recovered = recovered.sort(key=lambda cell: cell.get_counter_state, reverse=True)
        return ranked_susceptible, ranked_infectious, ranked_recovered
    
    def __get_next_status(self, cell):
        """
        Get cell next state consedering: 
            Cell state,
            Desease contamination number, 
            The amount of infectious neighbors,
            Desease recouvery length.
        """
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
        dS_dt, dI_dt, dR_dt = self.sir.next_t()
        ranked_susceptible, ranked_infectious, ranked_recovered = self.rank_cells(self.cells)
        # [ranked_susceptible[i].next_state = INFECTIOUS for i in range()]
        [cell.update_state() for cell in self.cells]
