
# Optimisation - blink each rock 25 times, then each of them 25 times twice more

GRANULARITY = 5
BLINKS = 75
CACHE = {}

for c in range(BLINKS, 0, -GRANULARITY):
    CACHE[c] = {}


class Rock:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

    def blink(self):
        if self.val == 0:
            self.val = 1
            return self
        elif len(str(self.val)) % 2 == 0:
            self.split()
            return self.next
        else:
            self.val *= 2024
            return self

    def split(self):
        sval = str(self.val)
        self.val = int(sval[:len(sval)//2])
        self.next = Rock(int(sval[len(sval)//2:]), self.next)

class Rocks:
    def __init__(self):
        self.first_rock = None

    def add_rock(self, value):
        self.first_rock = Rock(value, self.first_rock)

    def blink(self):
        r = self.first_rock
        while r:
            r = r.blink().next

    def count_rocks(self):
        return sum(1 for _ in self.rocks)

    @property
    def rocks(self):
        r = self.first_rock
        while r:
            yield r
            r = r.next


def blinks_and_count(val, blinks):
    if blinks <= 0:
        return 1
    global CACHE
    global GRANULARITY
    if val in CACHE[blinks]:
        return CACHE[blinks][val]
    print(f"Blinking {val} {blinks} times")
    rocks = Rocks()
    rocks.add_rock(val)
    assert blinks % GRANULARITY == 0
    for _ in range(GRANULARITY):
        rocks.blink()
    total = 0
    for r in rocks.rocks:
        total += blinks_and_count(r.val, blinks-GRANULARITY)
    CACHE[blinks][val] = total
    return total


total = 0
with open('input') as input:
    for rock in reversed(input.read().strip().split()):
        #print(f"Blinking {rock} {BLINKS} times")
        total += blinks_and_count(int(rock), BLINKS)

print(total)
