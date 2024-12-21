
# Be careful! I need to work out the sequence to type the door code.
# I don't really need pads that I control; I want pads that tell me the sequence
# to press to get what I want.
#
# E.g. door pad - I ask it to press "5", and it spits out the sequence of insttructions it'll need

class Pad:
    def __init__(self, layout, starting_pos):
        self.layout = layout
        self.y, self.x = starting_pos

    def up(self):
        self.y -= 1
        assert self.y >= 0

    def down(self):
        self.y += 1
        assert self.y < len(self.layout)

    def left(self):
        self.x -= 1
        assert self.x >= 0

    def right(self):
        self.x += 1
        assert self.x < len(self.layout[0])

    def press(self, y, x):
        commands = []
        while self.y > y:
            commands.append('^')
            self.y -= 1
        while self.y < y:
            commands.append('v')
            self.y += 1
        while x > self.x:
            commands.append('>')
            self.x += 1
        while x < self.x:
            commands.append('<')
            self.x -= 1
        commands.append('A')
        return commands


class DoorPad(Pad):
    def __init__(self):
        Pad.__init__(self, [[7,8,9],[4,5,6],[1,2,3],[' ',0,'A']], (3, 2))
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

    def press(self, val):
        y, x = self.map[val]
        return Pad.press(self, y, x)


with open('input') as input:
    codes = [l.strip() for l in input]

door = DoorPad()
for c in codes:
    print(f"{c}: ", end="")
    for v in c:
        print("".join(door.press(v)), end="")
    print()


