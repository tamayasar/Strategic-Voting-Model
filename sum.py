from itertools import combinations_with_replacement

n = 8
p = [-9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9]

sums = [sum(comb) for comb in combinations_with_replacement(p, n)]

print(sums.index(1))
