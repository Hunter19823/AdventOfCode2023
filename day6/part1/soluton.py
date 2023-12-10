import re


def read_numbers(line):
    return [int(num) for num in re.sub(r'\s+', ' ', line.split(':')[1]).strip().split(' ')]


def read_data(filename):
    with open(filename) as f:
        return [
            (time, distance)
            for time, distance in zip(
                read_numbers(f.readline()),
                read_numbers(f.readline())
            )
        ]


def calculate_distance(maximum_time, hold_time):
    velocity_per_hold_time = 1
    distance_traveled = velocity_per_hold_time * hold_time * (maximum_time - hold_time)
    return distance_traveled


data = read_data('input.txt')

number_of_ways_to_beat_record = 1
for time, distance in data:
    records = []
    for held_time in range(time+1):
        records.append((held_time, calculate_distance(time, held_time)))

    records = [
        record
        for record in records
        if record[1] > distance
    ]
    number_of_ways_to_beat_record *= len(records)

print(number_of_ways_to_beat_record)
