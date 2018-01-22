from collections import defaultdict, deque
from enum import Enum

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

class State(Enum):
    ENDED = 1
    STUCK = 2
    RUNNING = 3

class Program(object):
    def __init__(self, id, insts, inq, outq):
        self.regs = defaultdict(int)
        self.regs['p'] = id
        self.pc = 0
        self.insts = insts
        self.inq = inq
        self.outq = outq
        self.snd_count = 0
    
    def step(self):
        if not (0 <= self.pc < len(self.insts)):
            return State.ENDED
        op, args = self.insts[self.pc]
        if op == 'snd':
            self.outq.append(val(args[0], self.regs))
            self.pc += 1
            self.snd_count += 1
            return State.RUNNING
        elif op == 'set':
            self.regs[args[0]] = val(args[1], self.regs)
            self.pc += 1
            return State.RUNNING
        elif op == 'add':
            self.regs[args[0]] += val(args[1], self.regs)
            self.pc += 1
            return State.RUNNING
        elif op == 'mul':
            self.regs[args[0]] *= val(args[1], self.regs)
            self.pc += 1
            return State.RUNNING
        elif op == 'mod':
            self.regs[args[0]] = self.regs[args[0]] % val(args[1], self.regs)
            self.pc += 1
            return State.RUNNING
        elif op == 'rcv':
            if len(self.inq) == 0:
                return State.STUCK
            else:
                self.regs[args[0]] = self.inq.popleft()
                self.pc += 1
                return State.RUNNING
        elif op == 'jgz':
            x = val(args[0], self.regs)
            if x > 0:
                self.pc += val(args[1], self.regs)
            else:
                self.pc += 1
            return State.RUNNING
    

def process(prog_a, prog_b, nsteps=100000):
    for i in range(nsteps):
        res_a = prog_a.step()
        res_b = prog_b.step()

queue_a = deque()
queue_b = deque()

insts = read('input-18.txt')

prog_a = Program(0, insts, queue_a, queue_b)
prog_b = Program(1, insts, queue_b, queue_a)

process(prog_a, prog_b)

print(prog_b.snd_count)