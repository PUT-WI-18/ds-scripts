import copy

#By Mateusz Kluba

#### DANE

toName = []
#names = ['M', 'W', 'B']
#dane = [['M', 'W', 'B'], ['W', 'B', 'M'], ['B', 'M', 'W']]
#glosy = [7, 9, 4]

#names = ['A','B','C','D']
#dane = [['A','B','C','D'], ['C','D','B','A'], ['D','B','A','C']]
#glosy = [10,8,17]

#names = ['A','B','C']
#dane = [['A','B','C'], ['B','C','A'], ['C','B','A']]
#glosy = [4,3,2]

#names = ['A','B','C', 'D']
#dane = [['A','B','C','D'], ['B','D','C','A'], ['C','B','A','D'], ['D','C','B','A']]
#glosy = [5,7,7,4]


names=['A','B','C','D','E']
dane = [
    ['A','E','C','D','B'],
    ['B','A','E','C','D'],
    ['C','D','B','A','E'],
    ['D','A','B','C','E']   ]
glosy = [31,30,29,10]

#### KONIEC

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


init()

#### FUNKCJE

Borda()
Plurality()
AntiPlurality()
PluralityRunOff()
STV()
Coombs()
Baldwin()