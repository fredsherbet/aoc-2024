
def is_safe(levels):
    if levels[0] > levels[1]:
        # decreasing
        bounds = (-3, -1)
    else:
        # increasing
        bounds = (1, 3)
    for ix in range(1, len(levels)):
        delta = levels[ix] - levels[ix-1] 
        if delta < bounds[0] or bounds[1] < delta:
            return False
    return True


with open('input') as input:
    safe_count = 0
    for l in input.readlines():
        levels = [int(n) for n in l.split()]
        if is_safe(levels):
            safe_count += 1
            continue
        if any(is_safe(levels[:remove] + levels[remove+1:]) for remove in range(len(levels))):
            safe_count += 1
            continue
print(f"Number of safe levels: {safe_count}")

        