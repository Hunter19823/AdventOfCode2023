from icecream import ic


def parse_line(sentence):
    # Split the line by colon
    sentence = sentence.split(':')
    # Get the game number
    game_number = int(sentence[0].split(' ')[1])
    # Split the right half of the colon by a semi-colon.
    rounds = sentence[1].split(';')
    round_data = [
        [
            (color, int(count))
            for pouch_info in game_round.split(',')
            for count, color in [pouch_info.strip().split(' ')]
        ]
        for game_round in rounds
    ]
    return game_number, round_data


def aggregate_round_data(round_data):
    output = dict()
    for game_round in round_data:
        for color, count in game_round:
            if color not in output:
                output[color] = count
            output[color] = max(output[color], count)

    return output


def compare_aggregate_data(agg_data, expectation):
    for color, count in expectation.items():
        if color not in agg_data:
            return False
        if agg_data[color] > count:
            return False

    return True


expected = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

with open('input.txt', 'r') as f:
    line_data = [
        parse_line(line)
        for line in f.readlines()
    ]
    i = 0
    for game_number, data in line_data:
        aggregate_data = aggregate_round_data(data)
        if compare_aggregate_data(aggregate_data, expected):
            i += game_number

    print(i)