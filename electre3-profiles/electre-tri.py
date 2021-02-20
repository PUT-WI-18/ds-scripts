class Criterium:
    def __init__(self, types, weight, q, p, v, values_a, values_b):
        self.type = type
        self.weight = weight
        self.q = q
        self.p = p
        self.v = v
        self.a = a
        self.b = b

    def calculate_c(self):
        c = []
        d = []
        for type,a,b in self.types, self.values_a, self.values_b:
            if self.type is 'z':
                if self.a >= self.b - self.q:
                    c.append(1)
                elif self.a > self.b - self.p:
                    c.append(self.a - (self.b - self.p) / (self.p - self.q))
                else:
                    c.append(0)

                if self.a <= self.b - self.v:
                    d.append(1)
                elif self.a < self.b - self.p:
                    d.append(self.b - self.p) - self.a / (self.p - self.v)
                else:
                    d.append(0)

            elif self.type is 'k':
                if self.a > self.b + self.p:
                    c.append(0)
                elif self.a > self.b + self.q:
                    c.append((self.b + self.p) - self.a / (self.p - self.q))
                else:
                    c.append(1)

                if self.a > self.b + self.v:
                    d.append(1)
                elif self.a > self.b + self.p:
                    d.append(self.a - (self.b + self.p) / (self.v - self.p))
                else:
                    d.append(0)

            else:
                return "type must be 'z' or 'k'"


