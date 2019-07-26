#TODO: funções sir para o problema
class sir_model:
    def __init__(self):
        pass
        # State Variables	
        #     S	number of susceptibles
        #     I	number of infected
        #     B	concentration of toxigenic V. cholerae in water (cells/ml)
        # Parameters	
        #     H	total human population
        #     n	Human birth and death rates (day-1)
        #     a	rate of exposure to contaminated water (day-1)
        #     K	concentration of V. cholerae in water that yields 50% chance of
        #         catching cholera (cells/ml)
        #     r	rate at which people recover from cholera (day-1)
        #     nb	growth rate of V. cholerae in the aquatic environment (day-1)
        #     mb	loss rate of V. cholerae in the aquatic environment (day-1)
        #     e	contribution of each infected person to the population of V. cholerae
        #         in the aquatic environment (cell/ml day-1 person-1)
    
    def dS_dt(self, n, H, S, a, B, K, s):
        return n * (H - S) - a * self.λ(B, K) * S
    
    def dI_dt(self, a, B, K, S, r, I):
        return a * self.λ(B, K) * S - (r * I)

    def dB_dt(self, B, nb, mb, e, I):
        return ( B * (nb - mb)) + (e * I)

    def λ(self, B, K):
        return B / (K + B)

