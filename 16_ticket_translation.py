%%time

import re

with open(datafile) as fh:
    data_txt = fh.read()
fd_txt, yt_txt, nt_txt = data_txt.split('\n\n')

my_ticket = [int(x) for x in yt_txt.split('\n')[1].split(',')]

nearby_tickets = []
for line in nt_txt.strip().split('\n')[1:]:
    nearby_tickets.append([int(x) for x in line.split(',')])

fields = []
for line in fd_txt.strip().split('\n'):
    fieldname = line.split(':')[0]
    a1, z1, a2, z2 = (int(x) for x in re.findall(r'\d+', line))
    fields.append((fieldname, range(a1, z1+1), range(a2, z2+1)))


def is_in_field(v, field):
    return v in field[1] or v in field[2]


error_rate = 0
for nt in nearby_tickets:
    for v in nt:
        if not any(is_in_field(v, f) for f in fields):
            error_rate += v
            
part_1 = error_rate


def is_valid(ticket, fields=fields):
    for v in ticket:
        if not any(is_in_field(v, f) for f in fields):
            return False
    return True


valid_tickets = [x for x in nearby_tickets if is_valid(x)]
valid_tickets.append(my_ticket)

fieldsets = [set(range(len(fields))) for _ in fields]
for t in valid_tickets:
    for i, v in enumerate(t):
        for j, field in enumerate(fields):
            if not is_in_field(v, field):
                fieldsets[j].discard(i)

visited = set()
while any(len(x) > 1 for x in fieldsets):
    single = next(y for y in (next(iter(x)) for x in fieldsets if len(x) == 1) if y not in visited)
    visited.add(single)
    for fieldset in fieldsets:
        if len(fieldset) > 1:
            fieldset.discard(single)

field_indices = [x.pop() for x in fieldsets]
sorted_fieldnames = [y for (x, y) in sorted(zip(field_indices, (x[0] for x in fields)))]

my_fielded_ticket = list(zip(sorted_fieldnames, my_ticket))

part_2 = 1
for name, v in my_fielded_ticket:
    if name.startswith('departure'):
        part_2 *= v
