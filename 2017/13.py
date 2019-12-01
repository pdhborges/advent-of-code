from collections import OrderedDict
from copy import deepcopy

def parse(line):
    layer, lenght = line.strip().split(': ')
    return int(layer), int(lenght)

def read(filename):
    with open(filename) as f:
        return OrderedDict(parse(line) for line in f)

def update(configuration):
    for key in configuration:
        curr_layer = configuration[key]
        curr, step, limit = curr_layer
        
        if curr == 0 and step == -1:
            curr_layer[0] = 1
            curr_layer[1] = 1
        elif curr == limit - 1 and step == 1:
            curr_layer[0] = limit - 2
            curr_layer[1] = -1
        else:
            curr_layer[0] = curr + step
            curr_layer[1] = step

def caughts(firewall):
    curr_conf = dict((key, [0, 1, value]) for key, value in firewall.items())
    last_layer = max(firewall) + 1
    for i in range(20000000):
        init_conf = deepcopy(curr_conf)
        fail = False
        for j in range(last_layer):
            if j in init_conf and init_conf[j][0] == 0:
                fail = True
                break
            update(init_conf)
        if not fail:
            return i
        update(curr_conf)
    return -1

firewall = read('input-13.txt')
print(caughts(firewall))
# print(sum(layer * lenght for layer, lenght in caughts(firewall)))