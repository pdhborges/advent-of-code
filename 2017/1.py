from pathlib import Path
from collections import deque

def read(filename):
    return Path(filename).read_text().rstrip()

def circular_lshift(seq, amount):
    shifted = deque(seq)
    shifted.rotate(-amount)
    return shifted
    
def score(seq, nexts_seq):
    return sum(int(x) for x, next_x in zip(seq, nexts_seq) if x == next_x)

seq = read('input-1.txt')
nexts_seq = circular_lshift(seq, 1)

print(score(seq, nexts_seq))

nexts_seq = circular_lshift(seq, len(seq) // 2)

print(score(seq, nexts_seq))