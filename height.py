class height_calculator:
    def __init__(self, xvpc, H0, s1, s2, hVPC, Ad, L, hVPT):
        self.xvpc = xvpc
        self.curve_end = xvpc + L
        self.H0 = H0
        self.s1 = s1
        self.s2 = s2
        self.hVPC = hVPC
        self.a = 1.0 * (Ad/(2*L))
        self.hVPT = hVPT

    def get(self, x):
        if x < self.xvpc:
            return self.H0 + (self.s1) * (0.01) * x
        elif x >= self.xvpc and x <= self.curve_end:
            o = x - self.xvpc # offset
            return self.a * (o**2) + self.s1 * 0.01 * o + self.hVPC
        else:
            o = x - (self.curve_end) # offset
            return self.hVPT + self.s2 * 0.01 * o



