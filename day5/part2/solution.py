from icecream import ic

initial_seeds = []
source_mappings = {}
"""
The source mappings are a dictionary of dictionaries, where the first key is the source name,
and the second key is the destination name. The value is a list of tuples, where each tuple
represents a destination starting number, a source starting number, and a range width.
The tuples are sorted by the destination, starting number, range.

The range is 1-indexed, so a range of 1 is a single number, and a range of 2 is two numbers.

For example a tuple of (10, 5, 3) means that:
- A value of 5 maps to a value of 10
- A value of 6 maps to a value of 11
- A value of 7 maps to a value of 12

:type source_mappings: dict[str, dict[str, list[tuple[int, int, int]]]]
:param source_mappings: The mapping of source to destination, and the ranges that the source maps to the destination.
"""


def read_initial_seeds(line):
    seeds = [int(initial_seed_number) for initial_seed_number in line.split(': ')[1].split(' ')]
    return [
        tuple(seeds[i:i + 2])
        for i in range(0, len(seeds), 2)
    ]


def register_map(map_label, map_ranges):
    source, destination = tuple(map_label.split(' ')[0].split('-to-'))

    map_ranges.sort(key=lambda x: x[1])

    if source not in source_mappings:
        source_mappings[source] = {}
    source_mappings[source][destination] = map_ranges


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


def format_interval(starting_number, interval_range):
    # Example:
    # Input:
    # 5, 3
    # Output:
    #     |--|
    if interval_range <= 0:
        return ' ' * (starting_number - 1) + 'X'
    output = ' ' * (starting_number - 1)
    output += '|'
    if interval_range > 1:
        output += '-' * (interval_range - 1)
        output += '|'
    return output


def map_source_to_possible_destinations(source, destination, value_pair):
    """
    The goal of this function is to take a starting value and range,
    plus a source and destination for a mapping, and return a list of
    value-ranges that the starting value-range maps to in the destination.

    :type source: str
    :type destination: str
    :type value_pair: (int, int)
    :param source: The source name for the mapping
    :param destination: The destination name for the mapping
    :param value_pair: The starting value and range to map
    :return: The list of value-ranges that the starting value-range maps to in the destination
    """
    if source not in source_mappings:
        return None
    if destination not in source_mappings[source]:
        return None

    output = []

    value_start, value_range = value_pair
    value_end = value_start + value_range - 1
    # print("Mapping:", source, destination, value_pair)
    print(format_interval(value_start, value_range), "Value Pair", value_pair)

    # Store a list of any overlapping ranges, and the destination range they would map to.
    for range_data in source_mappings[source][destination]:
        destination_start, source_start, range_width = range_data
        print(format_interval(source_start, range_width), "Source", (source_start, range_width))
        print(
            format_interval(destination_start, range_width),
            "Destination", (destination_start, range_width),
            "( offset=", destination_start - source_start, ")"
        )
        source_end = source_start + range_width - 1
        # Any intervals that are within the source range, will be mapped to the destination and added to the output
        # Any intervals that are outside the source range, will be added to the output

        # If the interval is fully to the left of the source-range
        if value_start < source_start and value_end < source_start:
            # This interval exists to the left of the source-range, so we can stop looking
            # and add the value-range to the output
            output.append((value_start, value_range))
            # Subtract the interval range from the value-range
            # Update the value-start to be 1 to the right of the interval end
            value_range = 0
            value_start = value_end + 1
            print(format_interval(output[-1][0], output[-1][1]), "LEFT OF RANGE", output[-1])
            break
        # If the interval is fully to the right of the source-range
        elif value_start > source_end and value_end > source_end:
            # This interval exists to the right of the source-range, so we can ignore this
            # range until we find an interval that intersects the source-range
            print(format_interval(value_start, value_range), "RIGHT OF RANGE", (value_start, value_range))
            continue
        # If the interval is fully within the source-range
        elif value_start >= source_start and value_end <= source_end:
            # This interval is fully within the source-range, so we map the entire
            # interval to the destination
            output.append((destination_start + (value_start - source_start), value_range))
            # Subtract the interval range from the value-range
            # Update the value-start to be 1 to the right of the interval end
            value_range = value_range - value_range
            value_start = value_end + 1
            print(format_interval(output[-1][0], output[-1][1]), "FULLY WITHIN RANGE", output[-1])
            print(format_interval(value_start, value_range), "RIGHT OF RANGE", (value_start, value_range))
            break
        # If the interval intersects the left-side of the source-range
        elif value_start < source_start and value_end <= source_end:
            # The result is two ranges,
            # one to the left of the source-range which is unmapped,
            # and one within the source-range which is mapped to the destination

            # The left-side range is the value-start to the source-start (non-inclusive)
            output.append((value_start, source_start - value_start))

            # The right-side range is the source-start to the value-end (inclusive)
            output.append((destination_start, value_range - (source_start - value_start)))

            # Subtract the interval range from the value-range
            # Update the value-start to be 1 to the right of the interval end
            value_range = value_range - (source_start - value_start)
            value_start = value_end + 1
            print(format_interval(output[-2][0], output[-2][1]), "LEFT OUTSIDE RANGE", output[-2])
            print(format_interval(output[-1][0], output[-1][1]), "INTERSECTS RANGE", output[-1])
            print(format_interval(value_start, value_range), "RIGHT OF INTERSECTION", (value_start, value_range))
            break
        # If the interval intersects the right-side of the source-range
        elif value_start >= source_start and value_end > source_end:
            # The result is two ranges,
            # one within the source-range that is mapped,
            # and we need to update the value-range and value-start to be the remaining range
            # starting 1 after the source-end

            # The left-side range is the value-start to the source-end (inclusive)
            output.append((destination_start + (value_start - source_start), source_end - value_start + 1))

            # Subtract the interval range from the value-range
            # Update the value-start to be 1 to the right of the interval end
            value_range = value_range - (source_end - value_start + 1)
            value_start = source_end + 1

            print(format_interval(output[-1][0], output[-1][1]), "INTERSECTS RANGE", output[-1])
            print(format_interval(value_start, value_range), "RIGHT OF INTERSECTION", (value_start, value_range))
            break

        # If the interval encompasses the source-range

        # If the value-start is less than the source-start, then we need to add an interval
        # from the value-start to the source-start (non-inclusive)
        if value_start < source_start:
            output.append((value_start, source_start - value_start))
            print(format_interval(output[-1][0], output[-1][1]), "LEFT OF RANGE", output[-1])

        # Add the mapped range for the intersection of the value-range and the source-range
        output.append((destination_start, range_width))
        print(format_interval(output[-1][0], output[-1][1]), "INTERSECTS RANGE", output[-1])

        # Subtract the interval range from the value-range
        # Update the value-start to be 1 to the right of the interval end
        value_range = value_range - range_width
        value_start = source_end + 1
        print(format_interval(value_start, value_range), "RIGHT OF INTERSECTION", (value_start, value_range))

        # If the value-range is now 0, then we can stop looking
        if value_range == 0:
            break

    # If there is any remaining value-range, then we can add it to the output unmapped
    if value_range > 0:
        output.append((value_start, value_range))
        print(format_interval(output[-1][0], output[-1][1]), "RIGHT OF RANGE ALL RANGES", output[-1])

    print(source, destination, value_pair, '=', output)

    return output


with open('test-input.txt') as f:
    initial_seeds += read_initial_seeds(f.readline().strip())

    current_line = f.readline()
    label = None
    ranges = []

    while current_line:
        if current_line == '\n':
            if label is not None:
                register_map(label, ranges)

                label = None
                ranges = []

        if current_line[0].isalpha():
            label = current_line.strip()
        elif current_line[0].isdigit():
            ranges.append(tuple([int(number) for number in current_line.strip().split(' ')]))

        current_line = f.readline()

    if label is not None:
        register_map(label, ranges)

print(initial_seeds)
print(source_mappings)
print(is_connected('seed', 'location'))

seed_path = get_path_to('seed', 'location')

print(seed_path)

locations = []
for seed in initial_seeds:
    seed_ranges = [seed]
    for start, end in seed_path:
        new_seed_ranges = []
        for seed_range in seed_ranges:
            for new_seed_range in map_source_to_possible_destinations(start, end, seed_range):
                # print("Seed:", seed, "Start:", start, "End:", end, "Range:", seed_range, "=", new_seed_range,
                #       end='\n\n')
                new_seed_ranges.append(new_seed_range)
        seed_ranges = new_seed_ranges
    seed_ranges.sort(key=lambda x: x[0])
    locations += seed_ranges

locations.sort(key=lambda x: x[0])
for (start, location_range) in locations:
    print(format_interval(start, location_range), (start, location_range))
print(locations)
