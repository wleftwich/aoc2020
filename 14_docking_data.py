import re
from itertools import product

with open(datafile) as fh:
    data = [y for y in (x.strip() for x in fh) if y]

    
def parse_command(line):
    if line.startswith('mask'):
        return ('mask', line[len('mask = '):])
    elif line.startswith('mem'):
        return ('mem', tuple(int(x) for x in re.findall(r'\d+', line)))
    else:
        raise ValueError('Unknown command: %s' % line)

# Part 1
        
def make_mask(maskstr):
    return {
        'con': int(maskstr.replace('X', '1'), 2),
        'dis': int(maskstr.replace('X', '0'), 2)
    }
    

def apply_mask(mask, n):
    for k, v in mask.items():
        if k == 'dis':
            n = n | v
        elif k == 'con':
            n = n & v
        else:
            raise ValueError("Unknown mask type: %s %s" % (k, v))
    return n

mask = None
registers = {}
for line in data:
    cmd, arg = parse_command(line)
    if cmd == 'mask':
        mask = make_mask(arg)
    else:
        k, v = arg
        registers[k] = apply_mask(mask, v)

part_1 = sum(registers.values())

# Part 2

def make_floatmasks(maskstr):
    basemask = make_mask(maskstr)
    del basemask['con']
    D = {
        'base': basemask,
        'masks': []
    }
    xis = [i for (i, x) in enumerate(maskstr) if x == 'X']
    for bits in product(['0', '1'], repeat=len(xis)):
        L = ['X'] * 36
        for i, b in zip(xis, bits):
            L[i] = b
        D['masks'].append(make_mask(''.join(L)))
    return D

        
def apply_floatmasks(floatmasks, n):
    base = apply_mask(floatmasks['base'], n)
    masks = floatmasks['masks']
    if not masks:
        yield base
    for m in masks:
        yield apply_mask(m, base)


floatmasks = None
registers = {}
for line in data:
    cmd, arg = parse_command(line)
    if cmd == 'mask':
        floatmasks = make_floatmasks(arg)
    else:
        k, v = arg
        for reg in apply_floatmasks(floatmasks, k):
            registers[reg] = v

part_2 = sum(registers.values())
