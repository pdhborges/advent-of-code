from operator import lt, le, eq, ne, ge, gt, sub, add
from collections import namedtuple, defaultdict

Inst = namedtuple('Inst', ['reg', 'op', 'val', 'creg', 'cop', 'cval'])

to_op = {
    'inc' : add, 'dec' : sub
}

to_cop = {
    '<' : lt, '<=' : le, '==' : eq,
    '!=' : ne, '>=' : ge, '>' : gt
}

def parse_inst(line):
    reg, op, val, _, creg, cop, cval = line.split()
    return Inst(reg, to_op[op], int(val), creg, to_cop[cop], int(cval))

def read_program(filename):
    with open(filename) as f:
        return [parse_inst(line) for line in f]

def eval_program(program):
    regs = defaultdict(int)
    max_reg = 0
    for inst in program:
        if inst.cop(regs[inst.creg], inst.cval):
             regs[inst.reg] = inst.op(regs[inst.reg], inst.val)
             max_reg = max(max_reg, max(regs.values()))
    return regs, max_reg

program = read_program('input-8.txt')
regs, max_reg = eval_program(program)
print(max(regs.values()))
print(max_reg)