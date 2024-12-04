
# Ideas
# * Hunt through, going forward, keeping track of cells that would continue an XMAS (or SAMX)
# * Graph???
#
# HLD
#
# * Hunt algorithm
# * How to keep track of candidates?
# 
# Candidates are a list (set) of what letters are needed in what cells

candidates = {}
id = 123

def update_candidates(candidates, row, col, line):
    found = 0
    for c in list(candidates):
        found += update_candidate(candidates, c, row, col, line)
    return found

def update_candidate(candidates, candidate_id, row, col, line):
    c = candidates[candidate_id]
    if (row,col) not in c:
        # This candidate doesn't care about this cell.
        return 0
    if c[(row,col)] != line[col]:
        # This candidate is no good
        del candidates[candidate_id]
        return 0
    # Candidate still in running; no longer need to find this cell
    del c[(row,col)]
    if c:
        # We've got more to find
        return 0
    # We've completed this word!
    return 1

def add_candidates(candidates, row, col, line):
    global id
    if line[col] == 'X':
        # Going straight down
        candidates[id] = {(row+1, col): 'M', (row+2, col): 'A', (row+3, col): 'S'}
        id += 1
        # Going right
        candidates[id] = {(row, col+1): 'M', (row, col+2): 'A', (row, col+3): 'S'}
        id += 1
        # Going diagonally down and backwards
        candidates[id] = {(row+1, col-1): 'M', (row+2, col-2): 'A', (row+3, col-3): 'S'}
        id += 1
        # Going diagonally down and forwards
        candidates[id] = {(row+1, col+1): 'M', (row+2, col+2): 'A', (row+3, col+3): 'S'}
        id += 1
    if line[col] == 'S':
        # Going straight down (but reversed)
        candidates[id] = {(row+1, col): 'A', (row+2, col): 'M', (row+3, col): 'X'}
        id += 1
        # Going right (but reversed)
        candidates[id] = {(row, col+1): 'A', (row, col+2): 'M', (row, col+3): 'X'}
        id += 1
        # Going diagonally down and backwards (but reversed)
        candidates[id] = {(row+1, col-1): 'A', (row+2, col-2): 'M', (row+3, col-3): 'X'}
        id += 1
        # Going diagonally down and forwards (but reversed)
        candidates[id] = {(row+1, col+1): 'A', (row+2, col+2): 'M', (row+3, col+3): 'X'}
        id += 1
        

row = 0
found = 0
with open('input') as input:
    for line in input.readlines():
        for col in range(len(line)):
            found += update_candidates(candidates, row, col, line)
            add_candidates(candidates, row, col, line)
        row += 1

print(f"Found {found}")