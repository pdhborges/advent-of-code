from itertools import islice
from collections import defaultdict

def distance(point):
    return abs(point[0]) + abs(point[1])

def neighbours(point):
    x, y = point
    return ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1))

def spiral_seq():
    yield 0, 0
    x, y = 1, 0
    inc_x, inc_y = 0, 1
    while True:
        yield x, y
        if abs(x) == abs(y):
            if x <= 0 and y <= 0:
                inc_x, inc_y = 1, 0
            elif x > 0 and y <= 0:
                x += 1
                y -= 1
                inc_x, inc_y = 0, 1
            elif x <= 0 and y > 0:
                inc_x, inc_y = 0, -1
            else:
                inc_x, inc_y = -1, 0
        x += inc_x
        y += inc_y

def sequential_spiral(nth):
    return next(islice(spiral_seq(), nth - 1, nth))

def neighbour_spiral(limit):
    matrix = defaultdict(int)
    matrix[(0, 0)] = 1
    for point in islice(spiral_seq(), 1, None):
        value = sum(matrix[neighbour] for neighbour in neighbours(point))
        if value > limit:
            return value
        else:
            matrix[point] = value

print(distance(sequential_spiral(368078)))
print(neighbour_spiral(368078))