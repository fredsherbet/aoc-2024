from collections import deque
from itertools import product

class Monkey:
    def __init__(self, initial_secret):
        self.sell_values = calc_sequence(initial_secret)
        self.deltas = [None] + [a-b for a,b in zip(self.sell_values[1:], self.sell_values[:-1])]
        assert len(self.sell_values) == len(self.deltas)
        #print(sum(1 for d in self.deltas if d is not None))
        self.sell_map = {}
        signal = deque(maxlen=4)
        for d, s in zip(self.deltas, self.sell_values):
            signal.append(d)
            if tuple(signal) not in self.sell_map:
                self.sell_map[tuple(signal)] = s

    def print(self):
        for s, d in zip(self.sell_values, self.deltas):
            print(f"{s}: {d}")

    def sell_to(self, signal):
        if signal in self.sell_map:
            return self.sell_map[signal]
        return 0


def next_secret(n):
    n = prune(mix(n, n*64))
    n = prune(mix(n, n//32))
    n = prune(mix(n, n*2048))
    return n

def mix(a, b):
    return a^b

def prune(n):
    return n % 16777216

def calc_sequence(initial_secret):
    seq = [initial_secret % 10]
    secret = initial_secret
    for _ in range(2000):
        secret = next_secret(secret)
        seq.append(secret % 10)
    return seq


with open('input') as input:
    monkeys = [Monkey(int(l.strip())) for l in input]

print(f"Loaded {len(monkeys)} monkeys")
print(sum(m.sell_to((0,-1,1,1)) for m in monkeys))

best = 0
for signal in product(range(-9, 10), repeat=4):
    sold = sum(m.sell_to(signal) for m in monkeys)
    if sold > best:
        best = sold
        print(f"New best signal {signal}; earns {best}")
        #print(f"{signal} sells {[m.sell_to(signal) for m in monkeys]}")


print(best)

