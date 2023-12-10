import math
import re


def read_numbers(line):
    return [int(num) for num in re.sub(r'\s+', '', line.split(':')[1]).strip().split(' ')]


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


def quadratic_formula(a, b, c):
    return (
        (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a),
        (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
    )


data = read_data('input.txt')

plot_points = []
number_of_ways_to_beat_record = 0
for time, distance in data:
    # Times with respect to distance is polynomial.
    # The polynomial is defined as:
    #  y = -x^2 + time * x
    intersections = quadratic_formula(
        -1,
        time,
        -distance
    )
    left = math.ceil(intersections[0])
    right = math.ceil(intersections[1])
    count = right - left
    if distance == calculate_distance(time, left):
        count -= 1
    print(left, right, right-left, count)
    number_of_ways_to_beat_record += count

print(number_of_ways_to_beat_record)
