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
        ranked_infectious = sorted(infectious, key=lambda cell: cell.get_counter_state(), reverse=True)
        ranked_susceptible = sorted(susceptible, key=self.count_infectious_neighbors, reverse=True)
        ranked_recovered = sorted(recovered, key=lambda cell: cell.get_counter_state(), reverse=True)
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
           
    def get_deltas(self, cells):
        old_s, new_s = 0, 0
        old_i, new_i = 0, 0
        old_r, new_r = 0, 0
        for cell in cells:
            if cell.state == SUSCEPTIBLE:
                old_s += 1
            elif cell.state == INFECTIOUS:
                old_i += 1
            elif cell.state == RECOVERED:
                old_r += 1
            if cell.next_state == SUSCEPTIBLE:
                new_s += 1
            elif cell.next_state == INFECTIOUS:
                new_i += 1
            elif cell.next_state == RECOVERED:
                new_r += 1
        delta_s = old_s - new_s
        delta_i = old_i - new_i
        delta_r = old_r - new_r
        return delta_s, delta_i, delta_r

    def compute_commute(self, dif_s, dif_i, dif_r):
        r1,r2,r3 = 0,0,0
        while dif_s < 0 or dif_i < 0 or dif_r < 0:
            if dif_s < 0:
                r1 -= dif_s
                dif_i += dif_s
                dif_s = 0
            if dif_i < 0:
                r2 -= dif_i
                dif_r += dif_i
                dif_i = 0
            if dif_r < 0:
                r3 -= dif_r
                dif_s += dif_r
                dif_r = 0
        return r1,r2,r3
    
    def addapt_model_to_sir(self, dif_s, dif_i, dif_r, r_susceptible, r_infectious, r_recovered):
        commute_s, commute_i, commute_r = self.compute_commute(dif_s, dif_i, dif_r)
        for i in range(commute_s):
            r_susceptible[i].next_state = INFECTIOUS
        for i in range(commute_i):
            r_susceptible[i].next_state = RECOVERED
        for i in range(commute_r):
            r_susceptible[i].next_state = SUSCEPTIBLE
        # [r_susceptible[i].next_state = INFECTIOUS for i in range(commute_s)]
        # [r_susceptible[i].next_state = RECOVERED for i in range(commute_i)]
        # [r_susceptible[i].next_state = SUSCEPTIBLE for i in range(commute_r)]

    def next_t(self):
        [self.__get_next_status(cell) for cell in self.cells]
        dS_dt, dI_dt, dR_dt = self.sir.next_t()
        delta_s, delta_i, delta_r = self.get_deltas(self.cells)
        dif_s, dif_i, dif_r = dS_dt - delta_s, dI_dt - delta_i, dR_dt - delta_r
        r_susceptible, r_infectious, r_recovered = self.rank_cells(self.cells)
        self.addapt_model_to_sir(dif_s, dif_i, dif_r, r_susceptible, r_infectious, r_recovered)
        # [ranked_susceptible[i].next_state = INFECTIOUS for i in range()]
        [cell.update_state() for cell in self.cells]
