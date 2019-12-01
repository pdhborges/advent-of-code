from itertools import chain

def to_grid(symbolic_grid):
    return tuple(symbolic_grid.split('/'))
    
def flip(grid):
    return tuple(row[::-1] for row in grid)

def rotate(grid):
    rows = []
    for i in range(len(grid)):
        rows.append(''.join(row[i] for row in grid))
    return tuple(reversed(rows))

def read_rewrites(filename):
    with open(filename) as f:
        rewrites = dict()
        for rule in f:
            pattern, rewrite = map(to_grid, rule.strip().split(' => '))
            for i in range(4):
                rewrites[pattern] = rewrite
                rewrites[flip(pattern)] = rewrite
                pattern = rotate(pattern)
        return rewrites

def vstack(grids):
    return tuple(chain(*grids))
    
def hstack(grids):
    return tuple(''.join(x) for x in zip(*grids))

def count(grid, c):
    return sum(row.count(c) for row in grid)

def vsplit(grid, blk):
    return tuple(grid[i:i+blk] for i in range(0, len(grid), blk))

def hsplit(grid, blk):
    grids = []
    for i in range(0, len(grid[0]), blk):
        grids.append(tuple(line[i:i+blk] for line in grid))
    return tuple(grids)

def iterate(grid, rewrites):
    
    if len(grid) % 2 == 0:
        blk = 2
    else:
        blk = 3
    
    expanded = []
    for lg in vsplit(grid, blk):
        expanded_lg = []
        for g in hsplit(lg, blk):
            expanded_lg.append(rewrites[g])
        expanded.append(hstack(expanded_lg))
    expanded = vstack(expanded)
    return expanded


rewrites = read_rewrites('input-21.txt')
grid = to_grid('.#./..#/###')
for i in range(18):
    grid = iterate(grid, rewrites)
print(count(grid, '#'))