# Skrypt do sprawdzania czy się zgadza c(a,b) i c(b,a)
#
# Jeśli trzeba by samodzielnie policzyć c(a,b) i c(b,a)
# to wpisz cokolwiek w dwie ostatnie kolumny, np. 0 i 0
#
# [ 'z' albo 'k', q, p, g(A), g(B), c(ab), c(ba)]

dane = [
    ['k',  5,  10,  3,  8,    1,    0],
    ['k',  1,   5,  6,  2,  1/4,    1],
    ['z',  5,  10,  3,  8,    1,    1],
    ['z',  1,   5,  6,  2,  1/4,    0],
    ['z',  3,   9,  1,  7,  1/2,    1],
    ['k',  3,   9,  1,  7,    1,  2/3],
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

    for (typ, q, p, A, B, c1, c2) in dane:

        if p < q:
            print('p nie może być mniejsze od q')

        elif typ in 'zZ':
            w1 = zysk(q, p, A, B)
            w2 = zysk(q, p, B, A)

        elif typ in 'kK':
            w1 = koszt(q, p, A, B)
            w2 = koszt(q, p, B, A)

        ans = 'OK' if (abs(c1-w1)+abs(c2-w2)<0.0001) else '--'
        print(f'{typ}: c(a,b) = {w1:<20}  c(b,a) = {w2:<20}  {ans}')
