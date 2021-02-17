# Skrypt do sprawdzania czy się zgadza c(a,b) i c(b,a)
#
# Jeśli trzeba by policzyć cAB i cBA to wpisz cokolwiek
# w dwie ostatnie kolumny, np. 0 i 0
#
# [ 'z' albo 'k', p, q, gA, gB, cAB, cBA]

dane = [
    ['k',  5,  10,  3,  8,     1,  2/3],
    ['k',  1,   5,  6,  2,   1/4,    1],
    ['z',  5,  10,  3,  8,     1,    1],
    ['z',  1,   5,  6,  2,   1/4,    0],
    ['z',  3,   9,  1,  7,   1/2,    1],
    ['k',  3,   9,  1,  7,     1,  2/3],
]


# Tu już nic nie zmieniać
# --------------------------------------------------

def zysk(q, p, A, B):
    Aq = A + q
    Ap = A + p
    
    if B <= Aq:
        return  1
    elif B >= Ap:
        return 0
    else:
        return (B - Aq) / (Ap - Aq)


def koszt(q, p, A, B):
    Aq = max(0, A - q)
    Ap = max(0, A - p)
    
    if B >= Aq or Aq == 0:
        return  1
    elif B <= Ap:
        return 0
    else:
        return (B - Ap) / (Aq - Ap)


if __name__ == "__main__":

    for (typ, q, p, A, B, c1, c2) in dane:

        if p < q:
            print('p nie może być mniejsze od q')

        elif typ.lower() == 'z':
            z1 = zysk(q, p, A, B)
            z2 = zysk(q, p, B, A)
            ans = 'OK' if (z1 == c1 and z2 == c2) else '--'
            print(f'ZYSK:    c(a,b) = {z1:<7}  c(b,a) = {z2:<7}  {ans}')

        elif typ.lower() == 'k':
            k1 = koszt(q, p, A, B)
            k2 = koszt(q, p, B, A)
            ans = 'OK' if (k1 == c1 and k2 == c2) else '--' 
            print(f'KOSZT:   c(a,b) = {k1:<7}  c(b,a) = {k2:<7}  {ans}')

        else:
            print('Typ musi być Z albo K')
        