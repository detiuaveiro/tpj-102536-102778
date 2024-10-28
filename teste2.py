from itertools import cycle

lst = [1, 2, 3, 4, 5]

gen = cycle(lst)

for _ in range(10):
    print(next(gen))