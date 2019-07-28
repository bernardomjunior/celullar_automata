#article: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC29087/
class Sir_Model:
    def __init__(self):
        self.__c1()
        # self.c_test()
        self.S = self.H
        self.I = 1000
        self.R = 0
        self.B = 0
        self.t = 0
        self.population = self.S + self.I + self.R


    def next_t(self):
        self.S += round(self.dS_dt())
        self.I += round(self.dI_dt())
        self.B += round(self.dB_dt())
        new_r = self.population - self.S - self.I
        dR_dt = new_r - self.R #needed to return
        self.R = new_r
        self.t += 1
        print(round(self.dS_dt()), round(self.dI_dt()), dR_dt)
        return round(self.dS_dt()), round(self.dI_dt()), dR_dt


    def dS_dt(self):
        return self.n * (self.H - self.S) - self.a * self.λ() * self.S 
    
    def dI_dt(self):
        return self.a * self.λ() * self.S - (self.r * self.I)

    def dB_dt(self):
        return ( self.B * self.nb_mb) + (self.e * self.I)

    def λ(self):
        return self.B / (self.K + self.B)


    def __c1(self):
        self.H = 10_000
        self.n = 0.0001
        self.a = 0.5
        self.K = 1_000_000
        self.r = 0.2
        self.nb_mb = -0.33
        self.e = 10
        self.SC = 13_200
    
    def __c2(self):
        self.H = 10_000
        self.n = 0.0001
        self.a = 1
        self.K = 1_000_000
        self.r = 0.2
        self.nb_mb = -0.33
        self.e = 10
        self.SC = 6_600
    
    def __c2(self):
        self.H = 10_000
        self.n = 0.001
        self.a = 1
        self.K = 1_000_000
        self.r = 0.2
        self.nb_mb = -0.33
        self.e = 10
        self.SC = 6_600
    
    def c_test(self):
        self.H = 2400
        self.n = 0.001
        self.a = 1
        self.K = 1_000_000
        self.r = 0.2
        self.nb_mb = -0.33
        self.e = 10
        self.SC = 6_600