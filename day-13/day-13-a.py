import re
import math


def is_integer(x):
    return abs(x - round(x)) < 0.00001


def parse_button(l):
    match = re.match(r"Button .*: X\+?([0-9-]*), Y\+?([0-9-]*)", l)
    assert match, f"{l} does not match button pattern {match}"
    x, y = match.groups()
    return (int(x), int(y))

def parse_prize(l):
    match = re.match(r"Prize: X=([0-9-]*), Y=([0-9-]*)", l)
    assert match, f"{l} does not match prize pattern"
    x, y = match.groups()
    return (int(x), int(y))

def play(a, b, p):
    # Use a simultaneous equation to find an amount of a and b that gets to p
    xa, ya = a
    xb, yb = b
    xp, yp = p

    # xa*A + xb*B = xp
    # ya*A + yb*B = yp
    # ...
    # B = (yp - ya*xp/xa) / (yb - ya*xb/xa)
    # A = (xp - B*xb)/xa
    B = (yp - ya*xp/xa) / (yb - ya*xb/xa)
    A = (xp - B*xb)/xa
    if B > 100 or A > 100:
        return (0, 0)
    if not (is_integer(A) and is_integer(A)):
        return (0, 0)

    return (3*int(A+0.2) + int(B+0.2), 1)

prizes_won = 0
tokens_spent = 0

with open('input') as input:
    while True:
        l = input.readline()
        if not l:
            # End of the file
            break
        l = l.strip()
        if not l:
            # Skip blank line
            continue
        assert l.startswith('Button A')
        a = parse_button(l)
        l = input.readline().strip()
        assert l.startswith('Button B')
        b = parse_button(l)
        l = input.readline().strip()
        assert l.startswith('Prize')
        p = parse_prize(l)

        (tokens, win) = play(a, b, p)
        tokens_spent += tokens
        prizes_won += win

print(tokens_spent)
