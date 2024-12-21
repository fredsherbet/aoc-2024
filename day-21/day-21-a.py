from collections import deque
from itertools import product

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
            #if r == y:
            #    while c < x:
            #        c += 1
            #        seq += '>'
            #    while c > x:
            #        c -= 1
            #        seq += '<'
            #    sequences.append(seq)
            #    continue
            #if c == x:
            #    while r < y:
            #        r += 1
            #        seq += 'v'
            #    while r > y:
            #        r -= 1
            #        seq += '^'
            #    sequences.append(seq)
            #    continue
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
        self.pos = self.map[val]
        return s

    def seq(self, s):
        self.pos = self.map['A']
        sequences = [self.press(b) for b in s]
        #print(f"Pressing seq {s}; found {sequences}")
        #print(f"{','.join(str(s) for s in product(*sequences))}")
        for s in product(*sequences):
            yield "".join(b for b in s)


# Load up Door codes
with open('input') as input:
    door_codes = [l.strip() for l in input]


door = DoorPad()
rad = DirPad()
cold = DirPad()
human = DirPad()
complexity = 0
for code in door_codes:
    print(f"Calculating code {code}")
    s = ''
    last = 'A'
    for c in code:
        best = None
        for seq in door.press(c, last):
            #print(f"{seq} using rad:")
            for seq2 in rad.seq(seq):
                #print(f"{seq2} using cold:")
                for seq3 in cold.seq(seq2):
                    if best is None or len(best) > len(seq3):
                        #print(f"Found {best}")
                        best = seq3
            last = c
        s += best
    print(f"{s}: {len(s)} * {int(code[:3])}")
    complexity += len(s) * int(code[:3])

print(complexity)

