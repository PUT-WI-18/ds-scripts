# a>b>c>d -> ['a', 'b', 'c', 'd']
# a~b>c>d -> [['a', 'b'], 'c', 'd']
# 
# [Ranking_A, Ranking_B, oczekiwany_wynik]
# Jeśli masz sam policzyć podaj cokolwiek, np. 0

dane = [
(   ['d', ['e', 'f']],      ['d', 'e', 'f'],            2/3     ),
(   ['e', 'f', 'g', 'h'],   [['e','f'],'g','h'],        5/6     ),
(   ['d', 'e', 'f'],        [['d', 'e'], 'f'],          1/2     ),
(   ['e', 'f', 'g', 'h'],   [['e', 'f', 'g'], 'h'],    -1/2     ),
(   ['h', ['g', 'f'], 'e'], ['e', 'f', 'g', 'h'],      -3/4     ),
(   ['e', 'f', 'g', 'h'],   ['h', 'g', ['f', 'e']],    -5/6     ),
]


# --------------------------------------------------

import numpy as np
from itertools import chain

class Ranking:
    def __init__(self, ranking):
        self.ranking = ranking
        self.size = sum(len(x) for x in ranking)
        self.matrix = np.zeros((self.size, self.size))

    def toMatrix(self):
        elements = list(chain(*self.ranking))
        elements.sort()
        min = ord(elements[0])

        for i, char in enumerate(self.ranking):
            if len(char) != 1:
                for obj in char:
                    for obj_2 in char:
                        if obj is not obj_2:
                            self.matrix[ord(obj_2) - min, ord(obj) - min] = 0.5

            for obj_2 in char:
                tmp_ranking = self.ranking[i + 1:]
                for obj in tmp_ranking:
                    for element in obj:
                        self.matrix[ord(obj_2) - min, ord(element) - min] = 1

class KendallCalculator:
    def __init__(self, ranking_1, ranking_2):
        self.matrix = ranking_1 - ranking_2
        self.distance = 0.5 * np.sum(np.absolute(self.matrix))
        self.kendallCoefficent = 1 - 4 * (self.distance / (np.size(self.matrix, 0) * (np.size(self.matrix, 0) - 1)))


if __name__ == '__main__':

    for (r1, r2, tk) in dane:
        
        A = Ranking(r1)
        A.toMatrix()

        B = Ranking(r2)
        B.toMatrix()

        kendallCalculator = KendallCalculator(A.matrix, B.matrix)

        dk = kendallCalculator.distance
        wsp = kendallCalculator.kendallCoefficent

        print(f"dk = {dk:<3}  tk = {wsp:<20}  {'OK' if abs(wsp-tk)<0.0001 else '--'}")
