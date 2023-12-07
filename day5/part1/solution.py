initial_seeds = []
source_mappings = {}


def read_initial_seeds(line):
    return [int(initial_seed_number) for initial_seed_number in line.split(': ')[1].split(' ')]


def register_map(map_label, map_ranges):
    source, destination = tuple(map_label.split(' ')[0].split('-to-'))

    map_ranges.sort(key=lambda x: x[1])

    if source not in source_mappings:
        source_mappings[source] = {}
    source_mappings[source][destination] = map_ranges

    return {
        'source': source,
        'destination': destination,
        'label': map_label,
        'ranges': map_ranges
    }


def is_connected(start, end):
    if start not in source_mappings:
        return False

    # Depth-first search
    visited = set()
    stack = [start]

    while stack:
        current = stack.pop()
        visited.add(current)

        if current == end:
            return True

        if current not in source_mappings:
            continue

        for destination in source_mappings[current]:
            if destination not in visited:
                stack.append(destination)

    if end in visited:
        return True

    return False


def get_path_to(start, end):
    if start not in source_mappings:
        return None

    if source_mappings[start] == end:
        return [(start, end)]

    # Depth-first search, keeping track of path
    visited = set()
    stack = [start]
    path = [[]]

    while stack:
        current = stack.pop()
        visited.add(current)

        if current == end:
            break

        if current not in source_mappings:
            continue

        for destination in source_mappings[current]:
            if destination not in visited:
                stack.append(destination)
                path.append(path.pop() + [(current, destination)])

    if end in visited:
        return path[-1]

    return None


def map_source_to_destination(source, destination, value):
    if source not in source_mappings:
        return None
    if destination not in source_mappings[source]:
        return None

    for range_data in source_mappings[source][destination]:
        destination_start, source_start, range_width = range_data
        # If the value is less than the source starting range, and the ranges are sorted,
        # then we can stop looking and assume the destination-value is itself
        if value < source_start:
            return value

        # If the value is within the range of the source, then we can map it to the destination
        if value <= source_start + range_width - 1:
            return destination_start + (value - source_start)

    # If the value is greater than the source ending range, then we can assume the destination-value is itself

    return value


with open('input.txt') as f:
    initial_seeds += read_initial_seeds(f.readline().strip())

    current_line = f.readline()
    label = None
    ranges = []

    while current_line:
        if current_line == '\n':
            if label is not None:
                source_mapping = register_map(label, ranges)

                label = None
                ranges = []

        if current_line[0].isalpha():
            label = current_line.strip()
        elif current_line[0].isdigit():
            ranges.append(tuple([int(number) for number in current_line.strip().split(' ')]))

        current_line = f.readline()

    if label is not None:
        source_mapping = register_map(label, ranges)

print(source_mappings)
print(is_connected('seed', 'location'))

seed_path = get_path_to('seed', 'location')

print(seed_path)

locations = []
for seed in initial_seeds:
    seed_value = seed
    for start, end in seed_path:
        seed_value = map_source_to_destination(start, end, seed_value)
    locations.append((seed, seed_value))

locations.sort(key=lambda x: x[1])
print(locations)

