def replace_number_words(sentence):
    replacements = {
        'one': 'on1ne',
        'two': 'tw2wo',
        'three': 'thre3hree',
        'four': 'fou4our',
        'five': 'fiv5ive',
        'six': 'si6ix',
        'seven': 'seve7even',
        'eight': 'eigh8ight',
        'nine': 'nin9ine'
    }
    for word, replacement in replacements.items():
        while word in sentence:
            sentence = sentence.replace(word, replacement)
    return sentence


def remove_non_numeric_characters(sentence):
    return ''.join([
        character
        for character in sentence if character.isdigit()
    ])


def extract_numeric_strict(sentence):
    return remove_non_numeric_characters(replace_number_words(sentence))


def get_sum_of_lines(lines):
    return sum(
        [
            int(f"{numbers[0]}{numbers[-1]}")
            for numbers in map(extract_numeric_strict, lines)
        ]
    )


with open('input.txt', 'r') as f:
    print(get_sum_of_lines(f.readlines()))
