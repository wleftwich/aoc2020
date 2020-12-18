from itertools import product

def read_data(data, dim):
    actives = set()
    for (i, row) in enumerate(data.split()):
        for (j, val) in enumerate(row):
            if val == '#':
                coords = [i, j] + [0] * (dim - 2)
                actives.add(tuple(coords))
    return actives


def add_tuples(a, b):
    return tuple(x + y for (x, y) in zip(a, b))


def cycle(actives):
    result = set()
    inactives = set()
    deltas = list(product((-1, 0, 1), repeat=len(next(iter(actives)))))
    for cube in actives:
        neighborhood = set(add_tuples(cube, d) for d in deltas)
        if len(neighborhood.intersection(actives)) in [3, 4]:
            result.add(cube)
        inactives.update(neighborhood.difference(actives))
    for cube in inactives:
        neighborhood = set(add_tuples(cube, d) for d in deltas)
        if len(neighborhood.intersection(actives)) == 3:
            result.add(cube)
    return result


testdata = """\
.#.
..#
###
"""

cube3 = read_data(testdata, 3)
for _ in range(6):
    cube3 = cycle(cube3)
part_1 = len(cube3)
# 112
# took 55.8 msec

cube4 = read_data(testdata, 4)
for _ in range(6):
    cube4 = cycle(cube4)
part_2 = len(cube4)
# 848
# took 1.56 sec

cube5 = read_data(testdata, 5)
for _ in range(6):
    cube5 = cycle(cube5)
d5 = len(cube5)
# 5760
# took 1 min

cube2 = read_data(testdata, 2)
for _ in range(6):
    cube2 = cycle(cube2)
flatland = len(cube2)
# 5
# took 967 microsec

import time
t0 = time.time()
cube6 = read_data(testdata, 6)
for _ in range(6):
    cube6 = cycle(cube6)
    print(len(cube6), time.time() - t0)
d6 = len(cube6)
# 245 1.339268684387207
# 464 10.454355955123901
# 15744 74.04311347007751
# (quit)


