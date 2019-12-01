from collections import Counter

def parse_node(line):
    components = line.split()
    name = components[0]
    weight = int(components[1].strip('()'))
    above = []
    if '->' in components:
        above = [name.strip(',') for name in components[3:]]
    return name, {'weight' : weight, 'above' : above, 'tree_sum' : 0}

def read_tree(filename):
    with open(filename) as f:
        return dict(parse_node(line) for line in f)

def root(tree):
    all_nodes = set(name for name in tree)
    non_root_nodes = set(name for node in tree.values() for name in node['above'])
    return (all_nodes - non_root_nodes).pop()

def fill_sum(subtree_root, tree):
    current_node = tree[subtree_root]
    current_node['tree_sum'] = current_node['weight'] + sum(fill_sum(above, tree) for above in current_node['above'])
    return current_node['tree_sum']

def find_mismatch(sub_root, tree):
    current_node = tree[sub_root]
    mismatch = pick_mismatch_tree(current_node['above'], tree)
    if mismatch is None:
        return current_node['weight']
    return find_mismatch(mismatch, tree)

def pick_mismatch_tree(candidates, tree):
    freq = Counter(tree[candidate]['tree_sum'] for candidate in candidates)
    if not freq or len(freq) == 1:
        return None
    return next(candidate for candidate in candidates if tree[candidate]['tree_sum'] == freq.most_common()[-1][0])

def right_value(root, tree):
    mistmatch = find_mismatch(root, tree)
    freq = Counter(tree[above]['tree_sum'] for above in tree[root]['above']).most_common()
    diff = freq[0][0] - freq[1][0]
    return mistmatch + diff

tree = read_tree('input-7.txt')
root_node = root(tree)
print(root_node)
fill_sum(root_node, tree)
print(right_value(root_node, tree))