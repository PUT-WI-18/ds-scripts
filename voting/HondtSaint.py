import numpy
def wylicz_macierzglosow(method='dHondt',glosy=[900,240,1200,600],n=7):
    return_matrix=[];
    if(method is 'dHondt'):
        for i in range(1,n+1):
            for j in range(len(glosy)):
                return_matrix.append(glosy[j]/i)

    elif(method is 'Saint'):
        for j in range(len(glosy)):
            return_matrix.append(glosy[j] / 1)
        for i in range(1,n):
            for j in range(len(glosy)):
                return_matrix.append(glosy[j] / (i*2+1))
    return return_matrix


def hondtAndSaint(metoda,glosy1,ilosc_mandatow):
    macierz_glosow=wylicz_macierzglosow(method=metoda,n=7,glosy=glosy1)
    partie=[0]*len(glosy1);
    sorted_order=numpy.argsort(macierz_glosow)
    max=sorted(macierz_glosow,reverse=True)
    max=max[:ilosc_mandatow]
    for i in range(ilosc_mandatow):
        macierz_glosow.index(max[i])
        partie[macierz_glosow.index(max[i]) % len(partie)]+=1
        macierz_glosow[macierz_glosow.index(max[i])]=0
    print(partie)

hondtAndSaint('dHondt',[900,240,1200,600],9) #metoda, glosy dla partii, ilosc mandatow metody to ('Saint,dHondt)