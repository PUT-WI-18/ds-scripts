#By Cezary Milewski

from itertools import permutations  

#### DANE 

matrixName=['A','B','C','D']
dane = [
    ['A','C','D','B'],
    ['B','A','C','D'],
    ['C','D','B','A'],
    ['D','A','B','C']   ]
glosy = [5,12,7,9]

'''
matrixName=['A','B','C','D','E']
dane = [
    ['A','E','C','D','B'],
    ['B','A','E','C','D'],
    ['C','D','B','A','E'],
    ['D','A','B','C','E']   ]
glosy = [31,30,29,10]
'''
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

def init():    
    buildMatrix()
    fillMatrix()
    showMatrix()

init()

#### FUNKCJE

MaxiMin()
Copeland()
Kermeny()

