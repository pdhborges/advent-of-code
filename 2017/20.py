from operator import itemgetter
from collections import defaultdict

def components(dim):
    dim = dim.strip('p=<>va')
    return list(map(int, dim.split(',')))

def parse(line):
    return list(map(components, line.split(', ')))

def read_particles(filename):
    with open(filename) as f:
        return [parse(line.strip()) for line in f]
        
def manhathan(pos):
    return abs(pos[0]) + abs(pos[1]) + abs(pos[2])

def simulate(particles, steps=3000):
    for i in range(steps):
        for particle in particles:
            p, v, a = particle
            v[0] += a[0]
            v[1] += a[1]
            v[2] += a[2]
            p[0] += v[0]
            p[1] += v[1]
            p[2] += v[2]
        
        repeats = defaultdict(int)
        for p in particles:
            repeats[tuple(p[0])] += 1
        
        clean_col = []
        for p in particles:
            if repeats[tuple(p[0])] == 1:
                clean_col.append(p)
        
        particles = clean_col
    
    return particles
            
particles = read_particles('input-20.txt')
print(len(simulate(particles)))