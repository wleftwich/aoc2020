from itertools import product

def read_data(data, dim):
    S = set()
    for (i, row) in enumerate(reversed(data.split())):
        for (j, val) in enumerate(row):
            if val == '#':
                coords = [i, j] + [0] * (dim - 2)
                S.add(tuple(coords))
    return S

def make_deltas(dim):
    origin = tuple([0] * dim)
    return [x for x in product((-1, 0, 1), repeat=dim) if x != origin]

def add_tuples(a, b):
    return tuple(x + y for (x, y) in zip(a, b))

def apply_deltas(p, deltas):
    return (add_tuples(p, d) for d in deltas)

def iter_coords(S):
    ks = list(S)
    dim = len(ks[0])
    ranges = []
    for d in range(dim):
        a = min(x[d] for x in ks) - 1
        z = max(x[d] for x in ks) + 2
        ranges.append(range(a, z))
    return product(*ranges)

def cycle(cube):
    deltas = make_deltas(len(next(iter(cube))))
    S = set()
    for k in iter_coords(cube):
        active_nabe_count = 0
        for nk in apply_deltas(k, deltas):
            if nk in cube:
                active_nabe_count += 1
        if active_nabe_count == 3 or (k in cube and active_nabe_count == 2):
            S.add(k)
    return S

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
# took 82.1 msec

cube4 = read_data(testdata, 4)
for _ in range(6):
    cube4 = cycle(cube4)
part_2 = len(cube4)
# 848
# took 3.44 sec

cube5 = read_data(testdata, 5)
for _ in range(6):
    cube5 = cycle(cube5)
bonus = len(cube5)
# 5760
# took 2 min 10 sec

cube2 = read_data(testdata, 2)
for _ in range(6):
    cube2 = cycle(cube2)
flatland = len(cube2)
# 5
# took 1.05 msec


