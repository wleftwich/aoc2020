import re

datafile = 'data/19-1.txt'

with open(datafile) as fh:
    txt = fh.read()
    rulestxt, datatxt = txt.split('\n\n')

data = [y for y in (x.strip() for x in datatxt.split('\n')) if y]

def make_rules(lines):
    D = {}
    for line in lines:
        if not line:
            continue
        k, v = line.strip().split(':')
        v = v.replace('"', '')
        if '|' in v:
            v = '(?: ' + v + ' )'
        D[k] = v.split()
    return D

rules = make_rules(rulestxt.split('\n'))

def rules_to_re(rules):
    L = rules['0'].copy()
    while any(x.isdigit() for x in L):
        i, k = next((i,x) for (i, x) in enumerate(L) if x.isdigit())
        L[i:i+1] = rules[k].copy()
    L.insert(0, '^')
    L.append('$')
    return re.compile(''.join(L))

rules_re_1 = rules_to_re(rules)
part_1 = sum(bool(rules_re_1.match(x)) for x in data)

rules_2 = make_rules(rulestxt.split('\n'))
rules_2['8'] = ['(?:', '42', ')+']
rules_2['11'] = [
    '(?:',
    '(?:', '(?:', '42', ')', '{1}', '(?:', '31', ')', '{1}', ')', '|',
    '(?:', '(?:', '42', ')', '{2}', '(?:', '31', ')', '{2}', ')', '|',
    '(?:', '(?:', '42', ')', '{3}', '(?:', '31', ')', '{3}', ')', '|',
    '(?:', '(?:', '42', ')', '{4}', '(?:', '31', ')', '{4}', ')', '|',
    '(?:', '(?:', '42', ')', '{5}', '(?:', '31', ')', '{5}', ')', '|',
    '(?:', '(?:', '42', ')', '{6}', '(?:', '31', ')', '{6}', ')', '|',
    '(?:', '(?:', '42', ')', '{7}', '(?:', '31', ')', '{7}', ')', '|',
    '(?:', '(?:', '42', ')', '{8}', '(?:', '31', ')', '{8}', ')', '|',
    '(?:', '(?:', '42', ')', '{9}', '(?:', '31', ')', '{9}', ')',
    ')'
]

rules_re_2 = rules_to_re(rules_2)
part_2 = sum(bool(rules_re_2.match(x)) for x in data)
