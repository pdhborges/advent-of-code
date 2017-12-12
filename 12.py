def read_graph(filename):
    with open(filename) as f:
        return [list(map(int, line.split(None, 2)[2].split(', '))) for line in f]

def group_size(graph, group_elem):
    visited = [False] * len(graph)
    
    def visit(current):
        if not visited[current]:
            visited[current] = True
            for connected in graph[current]:
                visit(connected)
                
    visit(group_elem)
    return sum(visited)

def number_of_groups(graph):
    visited = [False] * len(graph)
    
    def visit(node):
        if not visited[node]:
            visited[node] = True
            for connected in graph[node]:
                visit(connected)
                
    n_groups = 0                
    for node, in_group in enumerate(visited):
        if not in_group:
            visit(node)
            n_groups += 1
    return n_groups

graph = read_graph('input-12.txt')
print(group_size(graph, 0))
print(number_of_groups(graph))