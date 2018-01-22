def read_components(filename):
    with open(filename) as f:
        return dict((tuple(map(int, line.strip().split('/'))), True) for line in f)

def can_plug(end, component):
    return end == component[0] or end == component[1]

def other_end(end, component):
    return component[1] if component[0] == end else component[0]

def strength(component):
    return component[0] + component[1]

def strongest(end, inventory):
    curr_strongest = 0
    
    for component in inventory:
        if inventory[component] and can_plug(end, component):
            inventory[component] = False
            total_strength = strength(component) + strongest(other_end(end, component), inventory)
            inventory[component] = True
            if total_strength > curr_strongest:
                curr_strongest = total_strength

    return curr_strongest
    
def longest_strongest(end, inventory):
    best = (0, 0)
    
    for component in inventory:
        if inventory[component] and can_plug(end, component):
            inventory[component] = False
            l, s = longest_strongest(other_end(end, component), inventory)
            curr = (1 + l, strength(component) + s)
            inventory[component] = True
            if curr > best:
                best = curr

    return best

print(longest_strongest(0, read_components('input-24.txt')))