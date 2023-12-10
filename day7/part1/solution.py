from enum import Enum

def read_file(filename):
    with (open(filename) as f):
        return [
            (line_data[0], int(line_data[1]))
            for line in [
                line
                for line in f.readlines()
            ]
            for line_data in [
                line.split(' ')
            ]
        ]


class Rank(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __ne__(self, other):
        return self.value != other.value

    def __str__(self):
        return f"{self.name}={self.value}"

    def __repr__(self):
        return f"{self.name}={self.value}"


def rank(hand):
    unique_characters = set(
        [
            character
            for character in hand
        ]
    )
    # Five of a kind.
    if len(unique_characters) == 1:
        return Rank.FIVE_OF_A_KIND
    character_counts = [
        (character, hand.count(character))
        for character in unique_characters
    ]
    character_counts.sort(key=lambda x: x[1], reverse=True)

    if len(unique_characters) == 2:
        # Four of a kind.
        if character_counts[0][1] == 4:
            return Rank.FOUR_OF_A_KIND
        # Full house.
        if character_counts[0][1] == 3:
            return Rank.FULL_HOUSE
    if len(unique_characters) == 3:
        # Three of a kind.
        if character_counts[0][1] == 3:
            return Rank.THREE_OF_A_KIND
        # Two pair.
        if character_counts[0][1] == 2 and character_counts[1][1] == 2:
            return Rank.TWO_PAIR
    if len(unique_characters) == 4:
        # Pair.
        if character_counts[0][1] == 2:
            return Rank.ONE_PAIR
    # High card.
    return Rank.HIGH_CARD


def get_strength(hand):
    # In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand.
    # A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
    # The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
    strengths = {
        'A': 13,
        'K': 12,
        'Q': 11,
        'J': 10,
        'T': 9,
        '9': 8,
        '8': 7,
        '7': 6,
        '6': 5,
        '5': 4,
        '4': 3,
        '3': 2,
        '2': 1,
    }
    size = len(hand)

    return sum(
        [
            100 ** (size - index - 1) * strengths[character]
            for index, character in enumerate(hand)
        ]
    )


data = read_file('input.txt')

print(data)
data.sort(key=lambda x: get_strength(x[0]), reverse=False)
print(data)
data.sort(key=lambda x: rank(x[0]), reverse=True)
print(data)

for i, (hand, bid) in enumerate(data):
    print(f'{i + 1}: {rank(hand)} {get_strength(hand)} {hand} {bid} {bid*(i+1)=}')

print(
    sum(
        [
            (i + 1) * bid
            for i, (hand, bid) in enumerate(data)
        ]
    )
)
