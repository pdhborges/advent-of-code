def read_initial_state():
    with open('input-6.txt') as f:
        return list(map(int, f.read().strip().split()))


def reallocation_seq(state):
    state = list(state)
    while True:
        yield tuple(state)
        to_realloc = state.index(max(state))
        to_realloc_blocks = state[to_realloc]
        state[to_realloc] = 0
        for pos in range(to_realloc + 1, to_realloc + 1 + to_realloc_blocks):
            state[pos % len(state)] += 1

def cycle_length(initial_state):
    seen = {}
    for step, state in enumerate(reallocation_seq(initial_state)):
        if state in seen:
            return step - seen[state], len(seen)
        seen[state] = step

print(cycle_length(read_initial_state()))
        

