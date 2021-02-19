# Kendall calculator
Check or calculate kendall coefficient for UTA method

# Sample input
```python
a>b>c>d -> ['a', 'b', 'c', 'd']
a~b>c>d -> [['a', 'b'], 'c', 'd']
```

```python
[Ranking_A, Ranking_B, oczekiwany_wynik]
```

```python3
dane = [
(   ['d', ['e', 'f']],      ['d', 'e', 'f'],            2/3     ),
(   ['e', 'f', 'g', 'h'],   [['e','f'],'g','h'],        5/6     ),
(   ['d', 'e', 'f'],        [['d', 'e'], 'f'],          1/2     ),
(   ['e', 'f', 'g', 'h'],   [['e', 'f', 'g'], 'h'],    -1/2     ),
(   ['h', ['g', 'f'], 'e'], ['e', 'f', 'g', 'h'],      -3/4     ),
(   ['e', 'f', 'g', 'h'],   ['h', 'g', ['f', 'e']],    -5/6     ),
]
```
Jeśli masz sam policzyć podaj cokolwiek, np. 0