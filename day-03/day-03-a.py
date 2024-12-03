
def calc_line(line):
    l = line.strip().strip('mul()').split(',')
    return int(l[0]) * int(l[1])


with open('processed-input-a') as input:
    result = sum(calc_line(l) for l in input.readlines())

print(result)