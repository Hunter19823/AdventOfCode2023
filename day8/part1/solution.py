def read_mapping(line):
    key, value = line.split('=')

    left, right = tuple(''.join([
        character
        for character in value
        if character.isalpha() or character == ','
    ]).split(','))

    return key.strip(), (left, right)


def read_file(filename):
    with open(filename, 'r') as f:
        starting_instructions = f.readline().strip()
        f.readline()
        return starting_instructions, [
            read_mapping(line.strip())
            for line in f.readlines()
        ]


def build_mapping(instruction_list):
    return {
        key: value
        for key, value in instruction_list
    }


def solve(problem_data):
    direction_map = {
        'R': 1,
        'L': 0,
    }

    mapping = build_mapping(problem_data[1])

    print(f"{problem_data=}")

    direction_sequence = [
        direction_map[direction]
        for direction in problem_data[0]
    ]

    start = 'AAA'
    end = 'ZZZ'

    current_node = start
    current_direction_index = 0

    steps = 1

    while True:
        current_direction = direction_sequence[current_direction_index]
        next_node = mapping[current_node][current_direction]
        print(f"{current_node=} -> {next_node=} ({current_direction=})")
        if next_node == end:
            break
        current_node = next_node
        current_direction_index = (current_direction_index + 1) % len(direction_sequence)
        steps += 1

    print(f"It took a total of {steps=} to get to the destination node.")


data = read_file('test-input.txt')
solve(data)

data = read_file('test-input2.txt')
solve(data)

data = read_file('input.txt')
solve(data)
