from operator import xor
from functools import reduce

def read_lengths(filename):
    with open(filename) as f:
        return list(map(int, f.read().strip().split(',')))

def read_data(filename):
    with open(filename) as f:
        return f.read().strip()

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

buf = list(range(256))
round(buf, read_lengths('input-10.txt'), [0], [0])
print(buf[0] * buf[1])

print(hash(read_data('input-10.txt')))