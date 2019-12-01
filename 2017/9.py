from collections import namedtuple, deque

Group = namedtuple('Group', ['groups', 'gc'])

def read(filename):
    with open(filename) as f:
        return deque(f.read().strip())

def skip_garbage(stream):
    assert stream[0] == '<'
    stream.popleft()
    count = 0
    while len(stream) > 0:
        next_c = stream.popleft()
        if next_c == '>':
            break
        elif next_c == '!':
            stream.popleft()
        else:
            count += 1
    return count

def parse_group(stream):
    assert stream[0] == '{'
    stream.popleft()
    groups = []
    gc = 0
    while len(stream) > 0:
        next_c = stream[0]
        if next_c == '}':
            stream.popleft()
            return Group(groups, gc)
        elif next_c == '{':
            groups.append(parse_group(stream))
        elif next_c == '<':
            gc += skip_garbage(stream)
        elif next_c == ',':
            stream.popleft()

def score(group, level = 1):
    return level + sum(score(g, level + 1) for g in group.groups)

def garbage_count(group):
    return group.gc + sum(garbage_count(g) for g in group.groups)

groups = parse_group(read('input-9.txt'))
print(score(groups))
print(garbage_count(groups))