LEFT = complex(0, 1)
RIGHT = complex(0, -1)

def read_infect_map(filename):
    with open(filename) as f:
        infect_map = dict()
        for i, line in enumerate(f):
            for j, c in enumerate(line):
                if c == '#':
                    infect_map[complex(i, j)] = 'I'
        return infect_map

def activity(initial_infection, steps=10000000):
    
    infection = dict(initial_infection)
    direction = complex(-1, 0)
    position = complex(12, 12)
    
    infections = 0
    
    for i in range(steps):

        status = infection.get(position, '')
        
        if status == '':
            direction *= LEFT
        elif status == 'W':
            direction = direction
        elif status == 'I':
            direction *= RIGHT
        else:
            direction *= RIGHT
            direction *= RIGHT
        
        if status == '':
            infection[position] = 'W'
        elif status == 'W':
            infection[position] = 'I'
            infections += 1
        elif status == 'I':
            infection[position] = 'F'
        else:
            del infection[position]
            
        position += direction
    
    return infections
    
    

infect_map = read_infect_map('input-22.txt')
print(activity(infect_map))
