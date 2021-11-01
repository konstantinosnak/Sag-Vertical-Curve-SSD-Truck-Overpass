class ssd:
    def __init__(self, xvpc, L, s1, s2, Hw, vo):
        self.xvpc = xvpc
        self.L = L
        self.s1 = s1
        self.s2 = s2
        self.Hw = Hw
        self.vo = vo
        self.tpr = 2.5 # AASHTO

    def find_s(self, x):
        if x <= self.xvpc:
            return self.s1
        elif x > self.xvpc and x <= (self.xvpc + self.L):
            return self.s1 + 100.0 * (x - self.xvpc) / (self.Hw)
        else:
            return self.s2

    def get(self, x):
        BD  = 0 # will be aggregated (it's the sum of breaking distance)
        BD_last = 0
        Vi  = self.vo
        Vi1 = 1 # exact value doesn't matter, should be > 0, so that it gets in loop
        xx = x +(self.tpr * self.vo) # xx is x + offset , alternatively: xx=x

        t = 0.01
        #a = 3.4 m/s for decelaration
        while Vi1 > 0:
            s = self.find_s(xx)
            Vi1 = Vi - 9.81 * ((3.4/9.81)+(s*0.01)) * t
            BD_last = Vi*t - 0.5*9.81*((3.4/9.81)+(s*0.01)) * (t**2)
            BD += BD_last

            # For next loop
            Vi = Vi1
            t += 0.01
            xx += BD_last 

        SSD = self.vo*self.tpr + BD
        return SSD

        