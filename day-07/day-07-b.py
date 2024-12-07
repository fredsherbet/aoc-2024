from itertools import product

def can_make_target(t, values):
    return any(s == t for s in possible_results(t, values))

def possible_results(limit, values):
    num_ops = len(values) - 1
    for ops in product('*+|', repeat=num_ops):
        res = values[0]
        for n,o in zip(values[1:], ops):
            if o == '*':
                res *= n
            elif o == '+':
                res += n
            elif o == '|':
                #print(f"Doing {res}||{n} -> {res}*10**{len(str(n))}+{n}")
                res = res*(10**len(str(n))) + n

            if res > limit:
                # All operators make numbers bigger, so stop if we go past
                # our target
                break

        #print(f"{values} {ops} == {res}")
        yield res

with open('input') as input:
    res = 0
    for l in input.readlines():
        [t, values] = l.strip().split(':')
        t = int(t)
        values = [int(v) for v in values.strip().split()]
        if can_make_target(t, values):
            res += t

    print(res)

