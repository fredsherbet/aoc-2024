
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
    if line[col] == 'M':
        # 2 candidates: 
        #
        # M.S  M.M
        # .A.  .A.
        # M.S  S.S
        candidates[id] = {
            (row+2, col): 'M',
            (row+1, col+1): 'A',
            (row, col+2): 'S',
            (row+2, col+2): 'S'
        }
        id += 1
        candidates[id] = {
            (row+2, col): 'S',
            (row+1, col+1): 'A',
            (row, col+2): 'M',
            (row+2, col+2): 'S'
        }
        id += 1

    if line[col] == 'S':
        # 2 candidates: 
        #
        # S.S  S.M
        # .A.  .A.
        # M.M  S.M
        candidates[id] = {
            (row+2, col): 'M',
            (row+1, col+1): 'A',
            (row, col+2): 'S',
            (row+2, col+2): 'M'
        }
        id += 1
        candidates[id] = {
            (row+2, col): 'S',
            (row+1, col+1): 'A',
            (row, col+2): 'M',
            (row+2, col+2): 'M'
        }
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