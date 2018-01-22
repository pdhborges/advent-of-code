from operator import xor
from functools import reduce

def circular_get(lst, start, lenght):
    return [lst[(start + i) % len(lst)] for i in range(lenght)]

def circular_set(lst, start, set_lst):
    for i in range(len(set_lst)):
        lst[(start + i) % len(lst)] = set_lst[i]

def round(buf, lengths, start, shift):
    for length in lengths:
        rev = list(reversed(circular_get(buf, start[0], length)))
        circular_set(buf, start[0], rev)
        start[0] += length + shift[0]
        shift[0] += 1

def data_to_lenghts(data):
    return [ord(c) for c in data] + [17, 31, 73, 47, 23]

def sparse_to_dense(sparse):
    return [reduce(xor, sparse[i * 16:(i + 1) * 16]) for i in range(16)]

def dense_hex(dense):
    return ''.join("%0.2x" % n for n in dense)

def hash(data):
    start = [0]
    shift = [0]
    lengths = data_to_lenghts(data)
    buf = list(range(256))
    for _ in range(64):
        round(buf, lengths, start, shift)
    return dense_hex(sparse_to_dense(buf))

def dense_bin(dense_hex):
    return ''.join(format(int(c, 16), '04b') for c in dense_hex)

def clear_region(matrix, i, j):
    if matrix[i][j] == '1':
        matrix[i][j] = '0'
        if i - 1 >= 0:
            clear_region(matrix, i - 1, j)
        if i + 1 < 128:
            clear_region(matrix, i + 1, j)
        if j - 1 >= 0:
            clear_region(matrix, i, j - 1)
        if j + 1 < 128:
            clear_region(matrix, i, j + 1)

def count_regions(matrix):
    regions = 0
    for i in range(128):
        for j in range(128):
            if matrix[i][j] == '1':
                clear_region(matrix, i, j)
                regions += 1
    return regions

data = 'hwlqcszp'
hashes = list((hash(data + '-' + str(row)) for row in range(128)))
matrix = [list(dense_bin(h)) for h in hashes]

print(sum(row.count('1') for row in matrix))
print(count_regions(matrix))
