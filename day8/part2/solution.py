import math

from icecream import ic


def read_mapping(line):
    key, value = line.split('=')

    left, right = tuple(''.join([
        character
        for character in value
        if character not in ('(', ')', ' ')
    ]).split(','))

    return key.strip(), (left, right)


def read_file(filename):
    direction_map = {
        'R': 1,
        'L': 0,
    }
    with open(filename, 'r') as f:
        starting_instructions = [
            direction_map[direction]
            for direction in f.readline().strip()
        ]
        f.readline()
        return starting_instructions, build_mapping([
            read_mapping(line.strip())
            for line in f.readlines()
        ])


def build_mapping(instruction_list):
    return {
        key: value
        for key, value in instruction_list
    }


def is_starting(node):
    return node[-1] == 'A'


def is_ending(node):
    return node[-1] == 'Z'


def get_starting_nodes(mapping):
    return [
        node
        for node in mapping.keys()
        if is_starting(node)
    ]


def get_ending_nodes(mapping):
    return [
        node
        for node in mapping.keys()
        if is_ending(node)
    ]


def get_steps_until_end(mapping, starting_node, direction_sequence, starting_offset=0):
    current_node = starting_node
    current_direction_index = starting_offset

    steps = 1
    while True:
        current_direction = direction_sequence[current_direction_index]
        next_node = mapping[current_node][current_direction]
        if is_ending(next_node):
            return steps, next_node, current_direction_index
        current_node = next_node
        current_direction_index = (current_direction_index + 1) % len(direction_sequence)
        steps += 1


def find_cycle(mapping, starting_node, direction_sequence):
    current_node = starting_node
    current_direction_index = 0

    steps = 1
    seen = set()
    path = [(starting_node, steps, current_direction_index)]
    seen_ending_once = False
    while True:
        current_direction = direction_sequence[current_direction_index]
        next_node = mapping[current_node][current_direction]

        if is_ending(next_node):
            path.append((next_node, steps, current_direction_index))

        if (next_node, current_direction_index) in seen and is_ending(next_node) and seen_ending_once:
            # Return the steps to get to the node, the node itself,
            # and the steps to get to the node again.
            print(f"Found a cycle from {starting_node=} to {next_node=}")
            print(f"Path of Cycle: {path=}")
            duplicate_nodes = [
                (node, steps, direction_index)
                for node, steps, direction_index in path
                if node == next_node and direction_index == current_direction_index
            ]
            cycle_start = duplicate_nodes[0][1]
            cycle_end = duplicate_nodes[1][1]
            cycle_length = cycle_end - cycle_start
            print(
                f"The cycle starts at: "
                f"{cycle_start} steps and ends at {cycle_end} steps, "
                f"repeating every {cycle_length} steps."
            )

            return cycle_start, cycle_length

        if (next_node, current_direction_index) in seen and is_ending(next_node):
            seen_ending_once = True

        seen.add((next_node, current_direction_index))

        current_node = next_node

        current_direction_index = (current_direction_index + 1) % len(direction_sequence)
        steps += 1


def least_common_multiple(numbers):
    return math.lcm(*numbers)


def solve(problem_data):
    direction_sequence, mapping = problem_data

    print(f"{problem_data=}")
    starting_nodes = get_starting_nodes(mapping)
    cycle_info = []
    for starting_node in starting_nodes:
        cycle_info.append(find_cycle(mapping, starting_node, direction_sequence))

    print(f"{cycle_info=}")
    lcm = least_common_multiple([
        cycle_length
        for cycle_start, cycle_length in cycle_info
    ])

    print(f"\n\nLeast Common Multiple: {lcm=}\n\n")


data = read_file('test-input.txt')
solve(data)

data = read_file('test-input2.txt')
solve(data)

data = read_file('test-input3.txt')
solve(data)

data = read_file('input.txt')
solve(data)
