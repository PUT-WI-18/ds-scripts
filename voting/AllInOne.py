from itertools import permutations  
import copy

# By Mateusz Kluba
# By Cezary Milewski
# By Piotr 'Kradne z gita' Tylczynski

names=['A','B','C','D']
matrixName = copy.deepcopy(names)
dane = [
    ['A','B', 'C', 'D'],
    ['C', 'D', 'B', 'A'],
    ['D', 'B', 'A', 'C']   ]
glosy = [10, 8, 17]


toName = []

#### KONIEC

matrix= [];
toIndex = {};
toName = {}
def buildMatrix():
    for i in range(len(dane[0])):
        matrix.append([])
        toIndex[matrixName[i]] = i;
        toName[i] = matrixName[i];
        for j in range(len(dane[0])):
            if(i==j):
                matrix[i].append(-1)
            else:
                matrix[i].append(0)

def showMatrix():
    print("MACIERZ:")
    for i in matrix:
        for j in i:
            print(str(j) + ", ", end='')
        print(" ");
    print(" ");
    
def fillMatrix():
    for i in range(len(dane)):
        for j in range(len(dane[0])):
            for k in range(1+j,len(dane[0])):
                indexJ = toIndex[dane[i][j]]
                indexK = toIndex[dane[i][k]]
                matrix[indexJ][indexK] += glosy[i]

def MaxiMin():
    print("\n===MaxiMin===")
    minimum =[]
    rank = list(toName.values());
    for a in matrix:
        min_val = min(i for i in a if i > 0) 
        minimum.append( min_val )
    for i in range(len(dane[0])):
        print( toName[i] +": "+ str(minimum[i]), end= "\t")
    print("")
    Z = [x for _,x in sorted(zip(minimum,rank), reverse=True)]
    print("Ranking: " + str(Z))

def Copeland():
    print("\n===Copeland===")
    rank = list(toName.values());
    value = [0] * len(dane[0])
    for i in range(len(dane)):
        for j in range(i+1, len(dane[0])):
           
            if( matrix[i][j] > matrix[j][i] ):
                value[ toIndex[toName[j]]]-=1
                value[ toIndex[toName[i]]]+=1
            else:
                value[ toIndex[toName[j]]]+=1
                value[ toIndex[toName[i]]]-=1
    for i in range(len(dane[0])):
        print( toName[i] +": "+ str(value[i]), end= "\t")
    print("")
    Z = [x for _,x in sorted(zip(value,rank), reverse=True)]
    print("Ranking: " + str(Z))

def Kermeny():
    print("\n===Kermeny===")
    
    perm = list(permutations(matrixName))
    
    bestSum =0;
    for i in perm:
        suma=0
        print(str(i)+": ", end="")
        for j in range(len(i)):
            for k in range(j+1, len(i)):
                suma+= matrix[toIndex[i[j]]][toIndex[i[k]]]
        print(suma)
        if(suma>bestSum):
            bestSum=suma
            bestPerm = i
    print("Decyzja: ", bestPerm)

def Borda():
    print("\n====Borda====")
    results = []
    for i in range(len(names)):
        results.append(0)
    maxPoints = len(names) - 1
    for i in range(len(dane)):
        for j in range(len(dane[i])):
            results[toName.index(dane[i][j])] += (maxPoints - j) * glosy[i]
    for i in range(len(dane[0])):
        print(toName[i] + ": " + str(results[i]), end="\t")
    print("")
    Z = [x for _, x in sorted(zip(results, toName), reverse=True)]
    print("Ranking: " + str(Z))

def Plurality():
    print("\n====Plurality rule====")
    results = []
    for i in range(len(names)):
        results.append(0)
    for i in range(len(dane)):
        results[toName.index(dane[i][0])] += glosy[i]
    for i in range(len(dane[0])):
        print(toName[i] + ": " + str(results[i]), end="\t")
    print("")
    Z = [x for _, x in sorted(zip(results, toName), reverse=True)]
    print("Ranking: " + str(Z))

def AntiPlurality():
    print("\n====Antiplurality rule====")
    results = []
    for i in range(len(names)):
        results.append(0)
    for i in range(len(dane)):
        for j in range(len(dane[i])-1):
            results[toName.index(dane[i][j])] += glosy[i]
    for i in range(len(dane[0])):
        print(toName[i] + ": " + str(results[i]), end="\t")
    print("")
    Z = [x for _, x in sorted(zip(results, toName), reverse=True)]
    print("Ranking: " + str(Z))

def PluralityRunOff():
    print("\n====Plurality Run-Off====")
    results = []
    for i in range(len(names)):
        results.append(0)
    threshold = 0.5 * sum(glosy)
    toNameTMP = copy.deepcopy(toName)
    noweDane = copy.deepcopy(dane)
    for i in range(len(noweDane)):
        results[toNameTMP.index(noweDane[i][0])] += glosy[i]
    for i in range(len(noweDane[0])):
        print(toNameTMP[i] + ": " + str(results[i]), end="\t")
    print("")
    Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
    if(max(results) > threshold):
        print("\nRanking: " + str(Z))
    else:
        for i in range(len(Z)-2):
            for j in range(len(noweDane)):
                noweDane[j].remove(Z[i+2])
            results.remove(results[-1])
            toNameTMP.remove(Z[i+2])
        for i in range(len(results)):
            results[i] = 0
        for i in range(len(noweDane)):
            results[toNameTMP.index(noweDane[i][0])] += glosy[i]
        for i in range(len(noweDane[0])):
            print(toNameTMP[i] + ": " + str(results[i]), end="\t")
        print("")
        Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
        print("\nRanking: " + str(Z))

def STV():
    print("\n====Single Transferable Vote====")
    results = []
    rank = []
    for i in range(len(names)):
        results.append(0)
    threshold = 0.5 * sum(glosy)
    toNameTMP = copy.deepcopy(toName)
    noweDane = copy.deepcopy(dane)
    for i in range(len(noweDane)):
        results[toNameTMP.index(noweDane[i][0])] += glosy[i]
    for i in range(len(noweDane[0])):
        print(toNameTMP[i] + ": " + str(results[i]), end="\t")
    print("")
    Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
    if(max(results) > threshold):
        print("\nRanking: " + str(Z))
    else:
        while(len(results) > 2):
            rank.append(Z[-1])
            toNameTMP.remove(Z[-1])
            results.remove(min(results))
            for i in range(len(results)):
                results[i] = 0
            for i in range(len(noweDane)):
                noweDane[i].remove(Z[-1])
            for i in range(len(noweDane)):
                results[toNameTMP.index(noweDane[i][0])] += glosy[i]
            for i in range(len(noweDane[0])):
                print(toNameTMP[i] + ": " + str(results[i]), end="\t")
            print("")
            Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
            if(max(results) > threshold):
                break
    end = Z + rank[::-1]
    print("\nRanking: " + str(end))

def Coombs():
    print("\n====Coombs====")
    results = []
    rank = []
    for i in range(len(names)):
        results.append(0)
    toNameTMP = copy.deepcopy(toName)
    noweDane = copy.deepcopy(dane)
    for i in range(len(noweDane)):
        results[toNameTMP.index(noweDane[i][-1])] += glosy[i]
    for i in range(len(noweDane[0])):
        print(toNameTMP[i] + ": " + str(results[i]), end="\t")
    print("")
    Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
    if(len(results) < 3):
        print("\nRanking: " + str(Z[::-1]))
    else:
        while(len(results) > 1):
            rank.append(Z[0])
            toNameTMP.remove(Z[0])
            results.remove(max(results))
            for i in range(len(results)):
                results[i] = 0
            for i in range(len(noweDane)):
                noweDane[i].remove(Z[0])
            for i in range(len(noweDane)):
                results[toNameTMP.index(noweDane[i][-1])] += glosy[i]
            for i in range(len(noweDane[0])):
                print(toNameTMP[i] + ": " + str(results[i]), end="\t")
            print("")
            Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
        end = Z + rank[::-1]
        print("\nRanking: " + str(end))

def Baldwin():
    print("\n====Baldwin====")
    results = []
    rank = []
    for i in range(len(names)):
        results.append(0)
    toNameTMP = copy.deepcopy(toName)
    noweDane = copy.deepcopy(dane)
    maxPoints = len(names) - 1
    for i in range(len(noweDane)):
        for j in range(len(noweDane[i])):
            results[toNameTMP.index(noweDane[i][j])] += (maxPoints - j) * glosy[i]
    for i in range(len(noweDane[0])):
        print(toNameTMP[i] + ": " + str(results[i]), end="\t")
    print("")
    Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
    if(len(results) < 3):
        print("Ranking: " + str(Z))
    else:
        while(len(results) > 2):
            rank.append(Z[-1])
            toNameTMP.remove(Z[-1])
            results.remove(min(results))
            for i in range(len(results)):
                results[i] = 0
            for i in range(len(noweDane)):
                noweDane[i].remove(Z[-1])
            maxPoints = maxPoints - 1
            for i in range(len(noweDane)):
                for j in range(len(noweDane[i])):
                    results[toNameTMP.index(noweDane[i][j])] += (maxPoints - j) * glosy[i]
            for i in range(len(noweDane[0])):
                print(toNameTMP[i] + ": " + str(results[i]), end="\t")
            print("")
            Z = [x for _, x in sorted(zip(results, toNameTMP), reverse=True)]
        end = Z + rank[::-1]
        print("\nRanking: " + str(end))

def init():
    for i in range(len(names)):
        toName.append(names[i])
    buildMatrix()
    fillMatrix()
    showMatrix()


init()

#### FUNKCJE

Borda()
Plurality()
AntiPlurality()
PluralityRunOff()
STV()
Coombs()
Baldwin()