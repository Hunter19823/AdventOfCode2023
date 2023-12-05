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


cards = [
    read_card_data(line)
    for line in text_data
]

cache = {}


def get_winning_count(card_data):
    card_number, winning_numbers, scratched_off_numbers = card_data

    if card_number in cache:
        return cache[card_number]

    # Get the union of the winning numbers and the scratched off numbers
    matches = set(winning_numbers) & set(scratched_off_numbers)

    cache[card_number] = len(matches)

    return len(matches)


copy_cache = {}


def get_copy_count(card_data):
    if card_data[0] in copy_cache:
        return copy_cache[card_data[0]]

    wins = (get_winning_count(card_data))

    if wins == 0:
        return 1

    total = 1 + sum([
        get_copy_count(cards[card_data[0] + offset])
        for offset in range(wins)
    ])

    copy_cache[card_data[0]] = total

    return total


print(sum([
    get_copy_count(card_data)
    for card_data in cards
]))
