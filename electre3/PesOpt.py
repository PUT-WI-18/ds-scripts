#By Cezary Milewski

dane=[]

def Pes( a ):
    for i in range( len(a)-1, -1, -1 ):
        if(a[i]=='>' or a[i]=='~'):
            return i+1+1
    return 1

def Opt( a ):
    for i in range( 0, len(a)):
        if(a[i]=='<'):
            return i+1
    return len(a)+1

def Solve( d ):
    for a in d:
        korekta = (a[0]-1)
        print("Zbior:",a,"Pes:", Pes(a[1])+korekta, "Opt:",Opt(a[1])+korekta)

def addNew(index,prog,sigma):
    a = []
    b=[index]
    for i in sigma:
        if( i[0] >= prog ):
            if(i[1] >= prog):
                a.append('~')
            else:
                a.append('>')
        elif( i[1] >= prog):
            a.append('<')
        else:
            a.append('?')
    b.append(a)
    dane.append(b)  
                        
##########################
#U Slowinskiego indeks poczatkowego byl 0, u Maslowskiej 1

### lista zawiera liste: <index_poczatkowy_b>, <lista_relacji_kolejnych_wariantow>
dane = [
    [1,['>','>','<']],
    [1,['>','>','>']],
    [1,['<','<','<']],
    [1,['>','~','<']],
    [1,['>','>','?']],
    [1,['?','?','?']] ]

### addNew(<index poczatkowy b>, <prog_lambda>, [ [<sigma(a,b0)>,<sigma(b0,a)>], ... ] )
addNew(0, 0.75, [  [1,0], [1,0.3], [0.9,0.4], [0.75,0.8], [0,1]  ])
addNew(0, 0.75, [  [1,0], [1,0.3], [0.9,0.4], [0.6, 0.6], [0,1]  ])
addNew(0, 0.75, [  [1,0], [1,0.3], [0.9,0.4], [0.8,0.85], [0,1]  ])
addNew(0, 0.75, [  [1,0], [1,0.3], [0.9,0.4], [0.6,0.85], [0,1]  ])
addNew(0, 0.75, [  [1,0], [1,0.3], [0.9,0.4], [0.7, 0.5], [0,1]  ])
addNew(0, 0.75, [  [1,0], [1,0.3], [0.9,0.4], [0.3, 0.9], [0,1]  ])

Solve(dane)

