
def is_safe(levels):
    fixes_available = 1
    if levels[0] > levels[-1]:
        # decreasing
        bounds = (-3, -1)
        if levels[0] < levels[1] and levels[1] < levels[2]:
            bounds = (1, 3)
            print (f"Flip order of levels: {levels}; increasing")
    else:
        # increasing
        bounds = (1, 3)
        if levels[0] > levels[1] and levels[1] > levels[2]:
            bounds = (-3, -1)
            print (f"Flip order of levels: {levels}; decreasing")

    ix = 1

    # Want to remove first level?
    removed_first = False
    delta = levels[1] - levels[0]
    if delta < bounds[0] or bounds[1] < delta:
        print(f"Removing first level of {levels}")
        removed_first = True
        fixes_available -= 1
        ix = 2

    while ix < len(levels):
        delta = levels[ix] - levels[ix-1] 
        if delta < bounds[0] or bounds[1] < delta:
            # Problem between ix-1 and ix
            if fixes_available <= 0:
                print (f"{levels} unsafe because ran out of fixes")
                #if removed_first: print(f"Removed first, then ran out of fixes for {levels}")
                return False
            # Try removing level ix
            fixes_available -= 1
            if ix+1 == len(levels):
                # ix is the last level, so removing it definely helps
                return True
            delta = levels[ix+1] - levels[ix-1]
            if delta < bounds[0] or bounds[1] < delta:
                # Still unsafe
                print(f"{levels} unsafe because removing {levels[ix]} doesn't help")
                return False
            # We can remove level ix, and have checked ix+1; skip ahead
            ix += 2
            continue
        ix += 1
    if removed_first: print(f"Removed first, and made the row safe")
    return True


with open('input') as input:
    safe_count = sum(1 for l in input.readlines() if is_safe([int(n) for n in l.split()]))
print(f"Number of safe levels: {safe_count}")

        