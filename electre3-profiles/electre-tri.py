class Pair:
    def __init__(self, types, weights, values_q, values_p, values_v, values_a, values_b):
        self.types = types
        self.weights = weights
        self.values_q = values_q
        self.values_p = values_p
        self.values_v = values_v
        self.values_a = values_a
        self.values_b = values_b
        self.c = []
        self.d = []
        self.coefficent = 0
        self.sigma = 0


    def calculate(self):
        for (type, a, b, q, p, v) in zip(self.types, self.values_a, self.values_b, self.values_q, self.values_p, self.values_v):
            if type == 'z':
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

            elif type == 'k':
                if a > b + p:
                    self.c.append(0)
                elif a > b + q:
                    self.c.append(((b + p) - a) / (p - q))
                else:
                    self.c.append(1)

                if a >= b + v:
                    self.d.append(1)
                elif a > b + p:
                    self.d.append((a - (b + p)) / (v - p))
                else:
                    self.d.append(0)

            else:
                return "type must be 'z' or 'k'"

    def calculate_coefficent(self):
        sum = 0
        weights_sum = 0
        for value, weight in zip(self.c, self.weights):
            sum += value * weight
            weights_sum += weight
        self.coefficent =  sum / weights_sum

    def calculate_sigma(self):
        temp_d = [self.d for i,j in zip(self.d, self.c) if i > j]
        self.sigma = self.coefficent



if __name__ == '__main__':
    pairs = []
    # types, weight, values_q, values_p, values_v, values_a, values_b
    pairs.append(Pair(['z', 'k'], [5, 2], [0.3, 0.4], [0.9, 0.8], [1.8, 2.1], [1.7, 7.6], [1.0, 7.0]))
    pairs.append(Pair(['z', 'k'], [5, 2], [0.3, 0.4], [0.9, 0.8], [1.8, 2.1], [1.7, 7.6], [6.0, 2.0]))
    pairs.append(Pair(['z', 'k'], [5, 2], [0.3, 0.4], [0.9, 0.8], [1.8, 2.1], [5.1, 4.1], [1.0, 7.0]))
    pairs.append(Pair(['z', 'k'], [5, 2], [0.7, 0.9], [1.2, 1.7], [2.9, 2.5], [5.1, 4.1], [6.0, 2.0])) # e, b2

    for pair in pairs:
        pair.calculate()
        pair.calculate_coefficent()
        pair.calculate_sigma()
        print(pair.c, pair.d, pair.coefficent, pair.sigma)

