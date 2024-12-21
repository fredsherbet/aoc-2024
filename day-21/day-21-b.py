from collections import deque
from itertools import product

# Ideas
# * Calculate the best way to get from each key on the dpad to each other key (only a few combos, so trivial?)
# * Don't need to calculate the sequence, just the complexity - what's the complexity of each of the above?
#
# Sequences we need:
# * A^, A>, Av, A<
# * ^>, ^<
# * v>, v<
# * >^, >v
# * <^, <v
# * ^A, >A, vA, <A
#
# I'm convinced that a longer sequence can not end up simpler than a shorter sequence. That lets us eliminate
# some paths to explore.
#
# Write a program to calculate the complexity of each of the above moves, and then calculate the complexity
# of each of our codes



# Be careful! I need to work out the sequence to type the door code.
# I don't really need pads that I control; I want pads that tell me the sequence
# to press to get what I want.
#
# E.g. door pad - I ask it to press "5", and it spits out the sequence of insttructions it'll need

class Pad:
    def __init__(self, starting_pos, banned):
        self.y, self.x = starting_pos
        self.banned = banned

    def press(self, y, x, from_y, from_x):
        sequences = []
        q = deque()
        q.append((from_y, from_x, ""))
        while q:
            r, c, seq = q.popleft()
            #print(f"Try from {r},{c}; so far: {seq}")
            assert len(seq) < 9
            if (r,c) == (y,x):
                #print(f"Found {seq}")
                sequences.append(seq + 'A')
                continue
            if (r,c) == self.banned:
                continue
            if r > y:
                q.append((r-1, c, seq + '^'))
            if r < y:
                q.append((r+1, c, seq + 'v'))
            if c > x:
                q.append((r, c-1, seq + '<'))
            if c < x:
                q.append((r, c+1, seq + '>'))

        #print(f"Found all sequences to press {y},{x}: {sequences}")
        return sequences


class DoorPad(Pad):
    def __init__(self):
        Pad.__init__(self, (3,2), (3,0))
        self.map = {
                '7': (0, 0),
                '8': (0, 1),
                '9': (0, 2),
                '4': (1, 0),
                '5': (1, 1),
                '6': (1, 2),
                '1': (2, 0),
                '2': (2, 1),
                '3': (2, 2),
                '0': (3, 1),
                'A': (3, 2)
            }

    def press(self, val, from_val):
        y, x = self.map[val]
        from_y, from_x = self.map[from_val]
        return Pad.press(self, y, x, from_y, from_x)

class DirPad(Pad):
    def __init__(self):
        Pad.__init__(self, (0,2), (0,0))
        self.map = {
                '^': (0, 1),
                'A': (0, 2),
                '<': (1, 0),
                'v': (1, 1),
                '>': (1, 2)
            }

    def press(self, val):
        y, x = self.map[val]
        s = Pad.press(self, y, x, self.pos[0], self.pos[1])
        print(f"Press {val} on dpad (starting from {self.pos}; got {len(s)} options)")
        self.pos = self.map[val]
        return s

    def seqs(self, s):
        self.pos = self.map['A']
        sequences = [self.press(b) for b in s]
        #print(f"Pressing seq {s}; found {sequences}")
        #print(f"{','.join(str(s) for s in product(*sequences))}")
        return ["".join(b for b in s) for s in product(*sequences)]


# Load up Door codes
with open('input') as input:
    door_codes = [l.strip() for l in input]


door = DoorPad()
dir_chain = []
for _ in range(2):
    dir_chain.append(DirPad())

complexity = 0
for code in door_codes:
    print(f"Calculating code {code}")
    last = 'A'
    for c in code:
        seqs = door.press(c, last)
        for pad in dir_chain:
            seqs2 = []
            for s in seqs:
                seqs2.extend(pad.seqs(s))
            min_length = min(len(s) for s in seqs2)
            seqs = [s for s in seqs2 if len(s) == min_length]
        last = c
    print(seqs)
    s = seqs[0]
    print(f"{s}: {len(s)} * {int(code[:3])}")
    complexity += len(s) * int(code[:3])

print(complexity)

