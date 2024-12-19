from collections import deque

def can_make(p, towels):
    # DFS
    q = deque()
    q.append(0)
    print()
    print(f"Looking for {p}")
    while q:
        ix = q.pop()
        print(f"So far, found {p[:ix]}; {ix} of {len(p)}")
        if ix == len(p):
            print(f"Can make {p}")
            return True
        for t in towels:
            if p[ix:].startswith(t):
                q.append(ix + len(t))
    print(f"Cannot make {p}")
    return False

with open('input') as input:
    data = input.readlines()

towels = [t.strip() for t in data[0].split(',')]

possible = sum(1 for pattern in data[2:] if can_make(pattern.strip(), towels))
print(possible)

