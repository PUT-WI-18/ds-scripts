class Criterium:
    c = []
    d = []

    def __init__(self, types, weight, values_q, values_p, values_v, values_a, values_b):
        self.types = types
        self.weight = weight
        self.values_q = values_q
        self.values_p = values_p
        self.values_v = values_v
        self.values_a = values_a
        self.values_b = values_b

    def calculate_c(self):
        for (type, a, b, q, p, v) in zip(self.types, self.values_a, self.values_b, self.values_q, self.values_p, self.values_v):
            if type is 'z':
                if a >= b - q:
                    self.c.append(1)
                elif a > b - p:
                    self.c.append((a - (b - p)) / (p - q))
                else:
                    self.c.append(0)

                if a <= b - v:
                    self.d.append(1)
                elif a < b - p:
                    self.d.append(((b - p) - a) / (p - v))
                else:
                    self.d.append(0)

            elif type is 'k':
                if a > b + p:
                    self.c.append(0)
                elif a > b + q:
                    self.c.append(((b + p) - a) / (p - q))
                else:
                    self.c.append(1)

                if a > b + v:
                    self.d.append(1)
                elif a > b + p:
                    self.d.append((a - (b + p)) / (v - p))
                else:
                    self.d.append(0)

            else:
                return "type must be 'z' or 'k'"


if __name__ == '__main__':
    # types, weight, values_q, values_p, values_v, values_a, values_b
    criterium = Criterium(['z', 'k'], [5, 2], [0.3, 0.4], [0.9, 0.8], [1.8, 2.1], [1.7, 7.6], [1.0, 7.0])
    criterium.calculate_c()
    print(criterium.c)
    print(criterium.d)
