from collections import defaultdict

def read(filename):
    with open(filename) as f:
        insts = (line.strip().split(' ') for line in f)
        return [(inst[0], tuple(inst[1:])) for inst in insts]

def isint(exp):
    try: 
        int(exp)
        return True
    except ValueError:
        return False

def val(exp, regs):
    if isint(exp):
        return int(exp)
    return regs[exp]

def run(insts):
    regs = defaultdict(int)
    regs['a'] = 1
    pc = 0
    mul_count = 0
    while 0 <= pc < len(insts):
        op, args = insts[pc]
        if op == 'set':
            regs[args[0]] = val(args[1], regs)
            if args[0] == 'f':
                print(regs, pc)
            pc += 1
        elif op == 'sub':
            regs[args[0]] -= val(args[1], regs)
            pc += 1
        elif op == 'mul':
            regs[args[0]] *= val(args[1], regs)
            mul_count += 1
            pc += 1
        elif op == 'jnz':
            x = val(args[0], regs)
            if x != 0:
                pc += val(args[1], regs)
            else:
                pc += 1
    return mul_count


print(run(read('input-23.txt')))