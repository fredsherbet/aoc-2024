import re

HEIGHT = 103
WIDTH = 101

#HEIGHT = 7
#WIDTH = 11

class Robot:
    def __init__(self, p, v):
        self.p = p
        self.v = v

    def step(self):
        global HEIGHT
        global WIDTH
        self.p = ((self.p[0] + self.v[0]) % WIDTH,
                  (self.p[1] + self.v[1]) % HEIGHT)

    @property
    def quadrant(self):
        global HEIGHT
        global WIDTH
        if self.p[0] == WIDTH//2 or self.p[1] == HEIGHT//2:
            #print(f"Robot in middle {r.p} ({r.v})")
            return 0
        if self.p[1] < HEIGHT // 2:
            if self.p[0] < WIDTH // 2:
                return 1
            return 2
        if self.p[0] < WIDTH // 2:
            return 3
        return 4


def maybe_print_map(t, robots):
    global HEIGHT
    global WIDTH
    worth_printing = False
    for y in range(HEIGHT):
        in_a_row = 0
        for x in range(WIDTH):
            if any(r.p == (x,y) for r in robots):
                in_a_row += 1
            else:
                in_a_row = 0
            if in_a_row >= 10:
                worth_printing = True
                break
        if worth_printing: break

    if not worth_printing: return

    print(f"At time {t}")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if any(r.p == (x,y) for r in robots):
                print('*', end="")
            else:
                print(' ', end="")
        print()
    print()


robots = []
with open('input') as input:
    for l in input.readlines():
        m = re.match(r"p=([0-9]+),([0-9]+) v=([0-9-]+),([0-9-]+)", l.strip())
        assert m, f"cannot match on line {l}"
        x, y, vx, vy = m.groups()
        robots.append(Robot((int(x), int(y)), (int(vx), int(vy))))

t = 0
while True:
    for r in robots:
        r.step()
    maybe_print_map(t, robots)
    t += 1

q1 = sum(1 for r in robots if r.quadrant == 1)
q2 = sum(1 for r in robots if r.quadrant == 2)
q3 = sum(1 for r in robots if r.quadrant == 3)
q4 = sum(1 for r in robots if r.quadrant == 4)

print(f"{q1}*{q2}*{q3}*{q4}")
print(q1*q2*q3*q4)
