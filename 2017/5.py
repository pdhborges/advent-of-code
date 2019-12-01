def read_inst(filename):
    with open(filename) as f:
        return [int(line) for line in f]

def run_inst_part1(insts):
    pc = 0
    steps = 0
    while 0 <= pc < len(insts):
        jump = insts[pc]
        insts[pc] += 1
        pc += jump
        steps += 1
    return steps

def run_inst_part2(insts):
    pc = 0
    steps = 0
    while 0 <= pc < len(insts):
        jump = insts[pc]
        if jump >= 3:
            insts[pc] -= 1
        else:
            insts[pc] += 1
        pc += jump
        steps += 1
    return steps


print(run_inst_part1(read_inst('input-5.txt')))
print(run_inst_part2(read_inst('input-5.txt')))