import copy
from collections import defaultdict, Counter

datafile = 'data/21-1.txt'

def parse_data(lines):
    L = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        ingredient_str, allergen_str = line.split('(contains')
        ingredients = tuple(ingredient_str.split())
        allergens = tuple(allergen_str.replace(',', ' ').replace(')', ' ').split())
        L.append((ingredients, allergens))
    return L

with open(datafile) as fh:
    data = parse_data(fh)

foods = defaultdict(list)
allergen_ingredients = defaultdict(set)
ingredient_counts = Counter()
for ingredients, allergens in data:
    for ingredient in ingredients:
        ingredient_counts[ingredient] += 1    
    for allergen in allergens:
        S = set()
        foods[allergen].append(S)
        for ingredient in ingredients:
            S.add(ingredient)
            allergen_ingredients[allergen].add(ingredient)

for k, v in foods.items():
    allergen_ingredients[k].intersection_update(set.intersection(*v))

ingredients_possibly_allergens = set.union(*allergen_ingredients.values())
inert_ingredients = set(ingredient_counts).difference(ingredients_possibly_allergens)
part_1 = sum(v for k, v in ingredient_counts.items() if k in inert_ingredients)

# Part 2

allergens = copy.deepcopy(allergen_ingredients)

singletons = [(k, next(iter(v))) for (k, v) in allergens.items() if len(v) == 1]
singletoncount = len(singletons)
while True:
    for (allergen, ingredient) in singletons:
        for k, v in allergens.items():
            if k != allergen:
                v.discard(ingredient)
    singletons = [(k, next(iter(v))) for (k, v) in allergens.items() if len(v) == 1]
    new_singletoncount = len(singletons)
    if new_singletoncount == singletoncount:
        print ('all done')
        break
    singletoncount = new_singletoncount

assert not any(len(v) > 1 for v in allergens.values())

dangerous_ingredients = [next(iter(v)) for (k, v) in sorted(allergens.items(), key=lambda x: x[0])]
part_2 = ','.join(dangerous_ingredients)


