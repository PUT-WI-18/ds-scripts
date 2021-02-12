import numpy as np


class Ranking:
    def __init__(self, ranking):
        self.ranking = ranking
        self.size = sum(len(x) for x in ranking)
        self.matrix = np.zeros((self.size, self.size))

    def toMatrix(self):
        for i, char in enumerate(self.ranking):
            if len(char) != 1:
                for obj in char:
                    for obj_2 in char:
                        if obj is not obj_2:
                            self.matrix[ord(obj_2) - 97, ord(obj) - 97] = 0.5

            for obj_2 in char:
                tmp_ranking = self.ranking[i + 1:]
                for obj in tmp_ranking:
                    for element in obj:
                        self.matrix[ord(obj_2) - 97, ord(element) - 97] = 1

class KendallCalculator:
    def __init__(self, ranking_1, ranking_2):
        self.matrix = ranking_1 - ranking_2
        self.distance = 0.5 * np.sum(np.absolute(self.matrix))
        self.kendallCoefficent = 1 - 4 * (self.distance / (np.size(self.matrix, 0) * (np.size(self.matrix, 0) - 1)))



if __name__ == '__main__':

    # tutaj dodajemy rankingi
    # np. a~b>c>d
    ranking_1 = Ranking([['a', 'b'], 'c', 'd'])
    ranking_1.toMatrix()

    # a>b>c>d
    ranking_2 = Ranking(['a','b','c','d'])
    ranking_2.toMatrix()

    # d>c>b>a
    ranking_3 = Ranking(['d','c','b','a'])
    ranking_3.toMatrix()

    # a>b>c~d
    ranking_4 = Ranking(['a', 'b', ['c', 'd']])
    ranking_4.toMatrix()

    # jako argumenty podajemy rankingi między którymi chcemy obliczyć współczynnik Kendalla
    kendallCalculator = KendallCalculator(ranking_2.matrix, ranking_4.matrix)

    print("dk = " + str(kendallCalculator.distance))
    print("wspolczynnik = " + str(kendallCalculator.kendallCoefficent))