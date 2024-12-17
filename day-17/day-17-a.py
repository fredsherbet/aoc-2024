
class Computer:
    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.i_ix = 0

    def is_halted(self):
        return 0 > self.i_ix or self.i_ix >= len(self.program)

    def execute_instruction(self):
        opcode = self.program[self.i_ix]
        operand = self.program[self.i_ix+1]
        self.i_ix += 2
        if self.is_combo(opcode):
            operand = self.combo(operand)

        #print(f"{opcode}, {operand}")

        if opcode == 0:
            # adv
            self.a = self.dv(self.a, operand)
        elif opcode == 1:
            # bxl
            self.b = self.x(self.b, operand)
        elif opcode == 2:
            # bst
            self.b = self.st(operand)
        elif opcode == 3:
            # jnz
            self.jnz(self.a, operand)
        elif opcode == 4:
            # bxc
            self.b = self.x(self.b, self.c)
        elif opcode == 5:
            # out
            return self.out(operand)
        elif opcode == 6:
            # bdv
            self.b = self.dv(self.a, operand)
        elif opcode == 7:
            # cdv
            self.c = self.dv(self.a, operand)

    def dv(self, numerator, d_pow):
        return numerator // (2**d_pow)

    def x(self, a, b):
        # Bitwise XOR
        return a^b

    def st(self, val):
        return val % 8

    def jnz(self, val, ix):
        if val != 0:
            self.i_ix = ix

    def out(self, val):
        return val % 8

    def is_combo(self, opcode):
        return opcode in [0, 2, 5]

    def combo(self, operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        assert False


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
