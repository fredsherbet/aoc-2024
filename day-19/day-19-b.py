from collections import deque

def can_make(p, towels, ix=0, memo=None):
    # Dynamic programming - recursive, and memo (top down)

    if memo is None: memo = {}
    if ix >= len(p):
        return 1
    if ix in memo and memo[ix] > 0:
        return memo[ix]
    memo[ix] = 0
    for t in towels:
        if p[ix:].startswith(t):
            memo[ix] += can_make(p, towels, ix+len(t), memo)
    print(f"From {ix} can make design in {memo[ix]} ways")
    return memo[ix]


with open('input') as input:
    data = input.readlines()

towels = [t.strip() for t in data[0].split(',')]

designs = sum(can_make(pattern.strip(), towels) for pattern in data[2:])
print(designs)

