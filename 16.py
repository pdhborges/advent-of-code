def parse(move):
    if move[0] == 's':
        return ('s', int(move[1:]))
    a, b = move[1:].split('/')
    if move[0] == 'x':
        return ('x', int(a), int(b))
    else:
        return ('p', a, b)

def read(filename):
    with open(filename) as f:
        return [parse(move) for move in f.read().strip().split(',')]

def dance(start, moves):        
    start = list(start)
    for move in moves:
        if move[0] == 's':
            start = start[-move[1]:] + start[:-move[1]]
        if move[0] == 'x':
            temp = start[move[1]]
            start[move[1]] = start[move[2]]
            start[move[2]] = temp
        if move[0] == 'p':
            a = start.index(move[1])
            b = start.index(move[2])
            temp = start[a]
            start[a] = start[b]
            start[b] = temp
    return start

def opera(moves, n):
    start = list('abcdefghijklmnop')
    for i in range(n):
        start = dance(start, moves)
    return start

moves = read('input-16.txt')
print(''.join(dance(list('abcdefghijklmnop'), moves)))

# the daces have a period of lenght 60. 40 is 1000000000 % 60
print(''.join(opera(moves, 40)))
