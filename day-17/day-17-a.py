from computer import Computer

with open('input') as input:
    data = [l.strip() for l in input]

a = int(data[0].split(':')[1].strip())
b = int(data[1].split(':')[1].strip())
c = int(data[2].split(':')[1].strip())
program = [int(i.strip()) for i in data[4].split(':')[1].split(',')]
computer = Computer(a, b, c, program)

out = []
while not computer.is_halted():
    out.append(computer.execute_instruction())

print(','.join(str(o) for o in out if o is not None))
