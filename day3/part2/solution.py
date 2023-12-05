with open('input.txt', 'r') as f:
    text_data = f.readlines()


def get_number_at_index(x_cord, y_cord):
    char = text_data[y_cord][x_cord]
    if not char.isdigit():
        return None
    # Starting at current index, go left until you find a number.
    # Then go right until you find a non-number.
    # Then return the full number.

    left_index = x_cord
    while left_index > 0 and text_data[y_cord][left_index - 1].isdigit():
        left_index -= 1

    right_index = x_cord
    while right_index < len(text_data[y_cord]) - 1 and text_data[y_cord][right_index + 1].isdigit():
        right_index += 1

    return text_data[y_cord][left_index:right_index + 1]


def get_neighboring_numbers(x_cord, y_cord):
    result = [
        get_number_at_index(x_cord - 1, y_cord),
        get_number_at_index(x_cord + 1, y_cord)
    ]
    # Add the left and right numbers.

    for i in [-1, 1]:
        # If the middle character is not a number, add right and left.
        if not text_data[y_cord + i][x_cord].isdigit():
            result.append(get_number_at_index(x_cord - 1, y_cord + i))
            result.append(get_number_at_index(x_cord + 1, y_cord + i))
            continue
        # If the middle character is a number, Just add the middle character.
        result.append(get_number_at_index(x_cord, y_cord + i))

    # Remove all the None values.
    result = [number for number in result if number is not None]
    return result


output = 0

for y, line in enumerate(text_data):
    for x, character in enumerate(line):
        # If the character is numeric, add it to the current number sequence
        # And also add the coordinates as well.
        if character == '*':
            # Character is gear.
            neighboring_numbers = get_neighboring_numbers(x, y)
            if len(neighboring_numbers) == 2:
                output += int(neighboring_numbers[0]) * int(neighboring_numbers[1])
                continue

print(output)
