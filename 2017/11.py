def read(filename):
    with open(filename) as f:
        return f.read().strip().split(',')

direction = {
    'n' : complex(1, 0),
    'ne' : complex(1, -1),
    'se' : complex(0, -1),
    's' : complex(-1, 0),
    'sw' : complex(-1, 1),
    'nw' : complex(0, 1)
}

def center_dist(pos):
    if pos.real * pos.imag >= 0:
        return pos.real + pos.imag
    else:
        return max(abs(pos.real), abs(pos.imag))

pos = complex(0, 0)
farthest_dist = 0
for step in read('input-11.txt'):
    pos += direction[step]
    farthest_dist = max(farthest_dist, center_dist(pos))

print(center_dist(pos))
print(farthest_dist)