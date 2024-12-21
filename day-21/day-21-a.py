
# Be careful! I need to work out the sequence to type the door code.
# I don't really need pads that I control; I want pads that tell me the sequence
# to press to get what I want.
#
# E.g. door pad - I ask it to press "5", and it spits out the sequence of insttructions it'll need

class Pad:
    def __init__(self, starting_pos):
        self.y, self.x = starting_pos

    def up(self):
        self.y -= 1
        assert self.y >= 0

    def down(self):
        self.y += 1

    def left(self):
        self.x -= 1
        assert self.x >= 0

    def right(self):
        self.x += 1

    def press(self, y, x):
        commands = []
        while x > self.x:
            commands.append('>')
            self.x += 1
        while x < self.x:
            commands.append('<')
            self.x -= 1
        while self.y > y:
            commands.append('^')
            self.y -= 1
        while self.y < y:
            commands.append('v')
            self.y += 1
        commands.append('A')
        return commands


class DoorPad(Pad):
    def __init__(self):
        Pad.__init__(self, (3, 2))
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

class DirPad(Pad):
    def __init__(self):
        Pad.__init__(self, (0, 2))
        self.map = {
                '^': (0, 1),
                'A': (0, 2),
                '<': (1, 0),
                'v': (1, 1),
                '>': (1, 2)
            }

    def press(self, val):
        y, x = self.map[val]
        return Pad.press(self, y, x)


# Load up Door codes
with open('input') as input:
    door_codes = [l.strip() for l in input]

# Calculate codes for first directional pad to control door robot
door = DoorPad()
dir_codes = []
for c in door_codes:
    dir_codes.append("".join("".join(door.press(v)) for v in c))

print("Dir codes")
for c,d in zip(door_codes, dir_codes):
    print(f"{c}: {d}")

# Calculate codes for second directional pad to control robot in high levels of radiation
dir = DirPad()
dir2_codes = []
for d in dir_codes:
    dir2_codes.append("".join("".join(dir.press(v)) for ins in d for v in ins))

print("Second layer of directional codes")
for c,d in zip(door_codes, dir2_codes):
    print(f"{c}: {d}")

# Calculate codes for third directional pad (controlled by a human), to control the robot that's cold
dir2 = DirPad()
dir3_codes = []
for d in dir2_codes:
    dir3_codes.append("".join("".join(dir.press(v)) for ins in d for v in ins))

print("Third layer of directional codes")
for c,d in zip(door_codes, dir3_codes):
    print(f"{c}: {d}")

# Complexity calculations
complexity = 0
for c,d in zip(door_codes, dir3_codes):
    complexity += len(d) * int(c[:3])
    print(f"+ {len(d)} {int(c[:3])}")

print(complexity)

