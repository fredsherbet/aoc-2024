
skipping = False

def calc_line(line):
    global skipping
    if line == 'do()':
        skipping = False
        return 0
    if line == "don't()":
        skipping = True
        return 0
    if skipping:
        return 0
    l = line.strip('mul()').split(',')
    return int(l[0]) * int(l[1])

with open('processed-input-b') as input:
    result = sum(calc_line(l.strip()) for l in input.readlines())

print(result)