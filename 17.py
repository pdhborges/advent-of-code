def run(shift, inserts=2017):
    curr_i = 0
    for i in range(1, inserts + 1):
        curr_i = ((curr_i + shift) % i) + 1
        if curr_i == 1: print(i)
    return curr_i


shift = 386
run(shift, 50000000)