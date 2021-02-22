from itertools import combinations 
from numpy import linspace, array

data=array([
    ['*', '@', '#'],
    ['*', '*', '*'],
    ['*', '@', '#'],
    ['#', '@', '*'],
    ['*', '#', '@'],
    ['#', '*', '@'],
    ['*', '*', '*'],
    ['#', '@', '*'],
    ['#', '#', '$']
])
dec=['X','X','X','Y','Y','Y','Z','Z','Z']
columns=['A','B','C']


valid_reducts=[]
lower=[]
upper=[]

def is_not_worse(reducted_data):
    for index in lower:
            reducted_row = reducted_data[index]
            if any([dec[i] != dec[index] for i, x in enumerate(reducted_data) if (x == reducted_row).all() ]):
                return False
    return True

for index, row in enumerate(data):
    same_rows = [dec[i] == dec[index] for i, x in enumerate(data) if (x == row).all() ]
    if all(same_rows):
        lower.append(index)
    else:
        upper.append(index)

for size in range(1, len(columns)+1):
    column_indexes = list(range(len(columns)))
    comb = combinations(column_indexes, size)
    for reduct in list(comb):
        nested_reducts = [set(reduct).issuperset(item) for item in valid_reducts]
        if any(nested_reducts):
            continue

        reducted_data = data[:,reduct]
        
        if is_not_worse(reducted_data):
            valid_reducts.append(reduct)


for reduct in valid_reducts:
    print([columns[item] for item in reduct])
