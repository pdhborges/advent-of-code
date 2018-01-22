UP = complex(-1, 0)
DOWN = complex(1, 0)
LEFT = complex(0, -1)
RIGHT = complex(0, 1)
END = complex(0, 0)

def read_matrix(filename):
    with open(filename) as f:
        return f.read().splitlines()

def value(matrix, pos):
    return matrix[int(pos.real)][int(pos.imag)]

def dirs_around(matrix, current_pos):
    return [d for d in [UP, DOWN, LEFT, RIGHT] if value(matrix, current_pos + d) != ' ']

def next_dir(matrix, current_pos, current_dir):
    pos_value = value(matrix, current_pos)
    if pos_value == ' ':
        return END
    elif pos_value == '|':
        return current_dir
    elif pos_value == '-':
        return current_dir
    elif pos_value == '+':
        around = dirs_around(matrix, current_pos)
        around.remove(-current_dir)
        return around[0]
    else:
        return current_dir

def walk(matrix):
    current_pos = complex(0, matrix[0].index('|'))
    current_dir = DOWN
    letters = []
    steps = 0
    while True:
        nxt_dir = next_dir(matrix, current_pos, current_dir)
        nxt_pos = current_pos + nxt_dir

        if value(matrix, current_pos) in 'ABCDEFGHIJKLMNOPQKRSTUVXWYZ':
            letters.append(value(matrix, current_pos))

        if nxt_dir == END:
            return ''.join(letters), steps
        else:
            steps += 1
            current_pos = nxt_pos
            current_dir = nxt_dir

matrix = read_matrix('input-19.txt')
print(walk(matrix))




