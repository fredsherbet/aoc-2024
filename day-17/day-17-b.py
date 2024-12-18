from computer import Computer
from input import prog

def find_cands(cands, want):
    next_cands = []
    for cand in cands:
        for a in range(4096):
            a = cand*8**4 + a
            c = Computer(a, 0, 0, prog)
            out = []
            while not c.is_halted():
                v = c.execute_instruction()
                if v is not None:
                    out.append(v)
            if out == want:
                print(f"{a}\t {','.join(str(o) for o in out)}")
                next_cands.append(a)
    return next_cands

cands = find_cands([0], prog[12:])
cands = find_cands(cands, prog[8:])
cands = find_cands(cands, prog[4:])
cands = find_cands(cands, prog)

