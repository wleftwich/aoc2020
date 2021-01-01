# Scroll down for embarrassing but working earlier effort

from collections import Counter, defaultdict

datafile = 'data/24-1.txt'

with open(datafile) as fh:
    data = [y for y in (x.strip() for x in fh) if y]


BLACK, WHITE = 1, 0

DRXNS = {
    'e': 1+0j,
    'ne': 0+1j,
    'nw': -1+1j,
    'w': -1+0j,
    'sw': 0-1j,
    'se': 1-1j
}


def track2tile(track):
    return sum(DRXNS[x] for x in tokenize_track(track))


def tokenize_track(track):
    buffer = ''
    for c in track:
        if c in ('e', 'w'):
            yield buffer + c
            buffer = ''
        else:
            buffer = c
    if buffer:
        raise ValueError('buffer is not empty')

        
def countblack(floor):
    return sum(floor.values())


def makefloor():
    return defaultdict(int)


def flip(tile, floor):
    floor[tile] = 1 - floor[tile]

    
def countblack(floor):
    return sum(floor.values())


floor = makefloor()
for track in data:
    flip(track2tile(track), floor)

part_1 = countblack(floor)


# Part 2

def neighbors(tile):
    return (tile + d for d in DRXNS.values())
        
def update_floor(floor):
    newfloor = makefloor()
    white_tiles = defaultdict(int)
    black_tiles = (k for (k, v) in floor.items() if v == BLACK])

    for bt in black_tiles:
        black_nabe_count = 0
        for nabe in neighbors(bt):
            if floor[nabe] == BLACK:
                black_nabe_count += 1
            else:
                white_tiles[nabe] += 1
        if black_nabe_count == 0 or black_nabe_count > 2:
            newfloor[bt] = WHITE
        else:
            newfloor[bt] = BLACK
            
    for wt, black_nabe_count in white_tiles.items():
        if black_nabe_count == 2:
            newfloor[wt] = BLACK
            
    return newfloor



floor = makefloor()
for track in data:
    flip(track2tile(track), floor)

for _ in range(100):
    floor = update_floor(floor)

part_2 = countblack(floor)


first_attempt = """

## Naive coordinate system leads to complicated code


BLACK, WHITE = -1, 1

def track2tile(track):
    return normalize_tile(Counter(tokenize_track(track)).items())

def tokenize_track(track):
    buffer = ''
    for c in track:
        if c in ('e', 'w'):
            yield buffer + c
            buffer = ''
        else:
            buffer = c
    if buffer:
        raise ValueError('buffer is not empty')

def normalize_tile(tile):
    D = defaultdict(int)
    D.update({k: v for (k, v) in tile})
    while True:
        count = sum(D.values())
        normalize_tile_step(D) # modify dict in place
        if sum(D.values()) == count:
            return tuple(sorted((k, v) for (k, v) in D.items() if k != 'zero' and v != 0))

def normalize_tile_step(D):
    combos = [
        (('e', 'w'), 'zero'),
        (('e', 'sw'), 'se'),
        (('e', 'nw'), 'ne'),
        (('ne', 'w'), 'nw'),
        (('se', 'w'), 'sw'),
        (('ne', 'sw'), 'zero'),
        (('ne', 'se'), 'e'),
        (('nw', 'sw'), 'w'),
        (('nw', 'se'), 'zero'),
    ]
    for ((a, b), c) in combos:
        av, bv = D.get(a), D.get(b)
        if not (av and bv):
            continue
        if av >= bv:
            D[c] += bv
            D[b] = 0
            D[a] = av - bv
        else:
            D[c] += av
            D[a] = 0
            D[b] = bv - av


def makefloor():
    return defaultdict(lambda: WHITE)


def flip(tile, floor):
    floor[tile] *= -1


def countblack(floor):
    return sum(v == BLACK for v in floor.values())


def neighbors(tile):
    D = defaultdict(int)
    D.update({k: v for (k, v) in tile})
    for drxn in ('e', 'ne', 'nw', 'w', 'sw', 'se'):
        E = D.copy()
        E[drxn] += 1
        yield normalize_tile(E.items())

"""
