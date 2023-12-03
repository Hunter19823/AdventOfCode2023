def parse_line(sentence):
    # Split the line by colon
    sentence = sentence.split(':')
    # Get the game number
    game_number = int(sentence[0].split(' ')[1])
    # Split the right half of the colon by a semi-colon.
    rounds = sentence[1].split(';')
    round_data = [
        [
            (color, count)
            for pouch_info in game_round.split(',')
            for color, count in [pouch_info.strip().split(' ')]
        ]
        for game_round in rounds
    ]
    return game_number, round_data


def aggregate_round_data(round_data):
    output = {
        color: count
        for game_round in round_data
        for color, count in game_round
    }
    output = {
        color: max(output[color], count)
        for game_round in round_data
        for color, count in game_round
    }
    return output


with open('input.txt', 'r') as f:
    # Read the first line
    line = f.readline()
    print(line, "=", parse_line(line))
    print(aggregate_round_data(parse_line(line)[1]))
