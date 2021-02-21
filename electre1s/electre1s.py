# Skrypt do sprawdzania czy się zgadza c(a,b) i c(b,a)
#
#
# Jeśli trzeba by samodzielnie policzyć c(a,b) i c(b,a)
# to wpisz cokolwiek w dwie ostatnie kolumny, np. 0 i 0
#
# Może takze liczyc globalny wspolczynnik zgodnosci o ile przyjmiemy ze istnieja tylko dwa warianty (a, b) i dowolna ilosc kryteriow
# kazde kryterium w osobnej podtablicy
#
# np.       g1  g2  g3
#       A   10  12  7
#       B   8   3   1
#
#       g1: q = 1, p = 3, gain, weight = 2
#       g2: q = 0, p = 7, gain, weight = 1
#       g3: q = 2, p = 5, cost, weight = 4
#            
#   dane = [   
#        ['z', 1, 3, 10, 8, 0, 0, 2],
#        ['z', 0, 7, 12, 3, 0, 0, 1],
#        ['k', 2, 5, 7, 1, 0, 0, 4]
#    ]
# [ 'z' albo 'k', q, p, g(A), g(B), c(ab), c(ba), weight]

dane = [
    ['z', 20, 50, 100, 150, 0,0, 2],
    ['k', 500, 900, 1000, 50000, 0, 0, 3]
]




# Niżej już nic nie zmieniać
# --------------------------------------------------

def zysk(q, p, A, B):
    Aq = A + q
    Ap = A + p
    
    if B <= Aq:
        return  1
    elif B >= Ap:
        return 0
    else:
        return 1 - ((B - Aq) / (Ap - Aq))


def koszt(q, p, A, B):
    Aq = A - q
    Ap = A - p
    
    if B >= Aq:
        return  1
    elif B <= Ap:
        return 0
    else:
        return (B - Ap) / (Aq - Ap)


if __name__ == "__main__":
    
    w1_sum = 0
    w2_sum = 0
    weight_sum = 0
    
    for (typ, q, p, A, B, c1, c2, weight) in dane:
        
        if p < q:
            print('p nie może być mniejsze od q')

        elif typ in 'zZ':
            w1 = zysk(q, p, A, B)
            w2 = zysk(q, p, B, A)

        elif typ in 'kK':
            w1 = koszt(q, p, A, B)
            w2 = koszt(q, p, B, A)
        
        w1_sum += w1
        w2_sum += w2
        weight_sum += weight
        
        ans = 'OK' if (abs(c1-w1)+abs(c2-w2)<0.0001) else '--'
        print(f'{typ}: c(a,b) = {w1:<20}  c(b,a) = {w2:<20}  {ans}')

    print("C(a,b) = {}, C(b,a) = {}".format(w1_sum / weight_sum, w2_sum / weight_sum))