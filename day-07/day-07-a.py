from itertools import product

def can_make_target(t, values):
    return any(s == t for s in possible_results(values))

def possible_results(values):
    num_ops = len(values) - 1
    for ops in product('*+', repeat=num_ops):
        res = values[0]
        for n,o in zip(values[1:], ops):
            if o == '*':
                res *= n
            elif o == '+':
                res += n
        print(f"{values} {ops} == {res}")
        yield res

with open('input') as input:
    res = 0
    for l in input.readlines():
        [t, values] = l.strip().split(':')
        t = int(t)
        values = [int(v) for v in values.strip().split()]
        if can_make_target(t, values):
            res += t
            print(f"Found another good one! {t}; total is now {res}")

print(res)

