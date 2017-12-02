def read_matrix(filename):
    with open(filename) as f:
        return [list(map(int, line.split())) for line in f]

def checksum(matrix):
    return sum(max(line) - min(line) for line in matrix)

def evenlysum(matrix):
    
    def evenly_divisors(line):
        for i in range(len(line)):
            for j in range(i + 1, len(line)):
                if line[i] % line[j] == 0:
                    return line[i] // line[j]
                elif line[j] % line[i] == 0:
                    return line[j] // line[i]
    
    return sum(evenly_divisors(line) for line in matrix)

    
matrix = read_matrix('input-2.txt')

print(checksum(matrix))
print(evenlysum(matrix))