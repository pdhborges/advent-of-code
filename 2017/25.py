from collections import defaultdict


def run(nsteps):
    state = 'A'
    tape = defaultdict(int)
    cursor = 0
    
    for step in range(nsteps):
        if state == 'A':
            if tape[cursor] == 0:
                tape[cursor] = 1
                cursor += 1
                state = 'B'
            else:
                tape[cursor] = 0
                cursor -= 1
                state = 'E'
        elif state == 'B':
            if tape[cursor] == 0:
                tape[cursor] = 1
                cursor -= 1
                state = 'C'
            else:
                tape[cursor] = 0
                cursor += 1
                state = 'A'
        elif state == 'C':
            if tape[cursor] == 0:
                tape[cursor] = 1
                cursor -= 1
                state = 'D'
            else:
                tape[cursor] = 0
                cursor += 1
                state = 'C'
        elif state == 'D':
            if tape[cursor] == 0:
                tape[cursor] = 1
                cursor -= 1
                state = 'E'
            else:
                tape[cursor] = 0
                cursor -= 1
                state = 'F'
        elif state == 'E':
            if tape[cursor] == 0:
                tape[cursor] = 1
                cursor -= 1
                state = 'A'
            else:
                tape[cursor] = 1
                cursor -= 1
                state = 'C'
        elif state == 'F':
            if tape[cursor] == 0:
                tape[cursor] = 1
                cursor -= 1
                state = 'E'
            else:
                tape[cursor] = 1
                cursor += 1
                state = 'A'
    
    return sum(tape.values())
    
print(run(12386363))