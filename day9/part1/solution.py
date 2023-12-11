def read_file(filename):
    with open(filename, 'r') as f:
        return [
            [int(num) for num in line.split(' ')]
            for line in f.readlines()
        ]


def format_line(line):
    return [
        (x, y)
        for (x, y) in enumerate(line)
    ]


data = read_file('test-input.txt')
for line in data:
    print(format_line(line))

data = read_file('input.txt')

for line in data:
    print(format_line(line))
