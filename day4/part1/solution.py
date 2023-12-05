from icecream import ic
import re

with open('input.txt', 'r') as f:
    text_data = f.readlines()


def read_card_data(line):
    # Replace all whitespace with a single space
    line = re.sub(r'\s+', ' ', line)
    label, card_data = line.split(':')
    card_number = int(label.split(' ')[-1])

    winning_numbers, scratched_off_numbers = card_data.split('|')
    winning_numbers = [
        int(number)
        for number in winning_numbers.strip().split(' ')
    ]
    scratched_off_numbers = [
        int(number)
        for number in scratched_off_numbers.strip().split(' ')
    ]

    return card_number, winning_numbers, scratched_off_numbers


def get_score(card_data):
    # Get the union of the winning numbers and the scratched off numbers
    card_number, winning_numbers, scratched_off_numbers = card_data
    matches = ic(set(winning_numbers) & set(scratched_off_numbers))

    return int(2 ** (len(matches) - 1))


print(sum([
    get_score(read_card_data(line))
    for line in text_data
]))
