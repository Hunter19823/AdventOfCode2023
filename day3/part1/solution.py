with open('input.txt', 'r') as f:
    text_data = f.readlines()

number_sequences = []
symbol_coordinates = set()

for y, line in enumerate(text_data):
    coordinates = []
    current_number_sequence = None
    for x, character in enumerate(line):
        # If the character is numeric, add it to the current number sequence
        # And also add the coordinates as well.
        if character.isdigit():
            if current_number_sequence is None:
                current_number_sequence = character
            else:
                current_number_sequence += character
            coordinates.append((x, y))
        elif character != '.' and character != '\n':
            # Character is special character.
            # Mark the surrounding coordinates as potential intersections.
            [
                symbol_coordinates.add((x + x_offset, y + y_offset))
                for x_offset in range(-1, 2)
                for y_offset in range(-1, 2)
            ]
            pass

        if not character.isdigit() and current_number_sequence is not None:
            number_sequences.append((current_number_sequence, coordinates))
            current_number_sequence = None
            coordinates = []

output = 0
for number, coordinates in number_sequences:
    for coordinate in coordinates:
        if coordinate in symbol_coordinates:
            output += int(number)
            break

max_size = max(len(line) for line in text_data) + 1, len(text_data) + 1
grid = [['.' for _ in range(max_size[0])] for _ in range(max_size[1])]
for y, line in enumerate(text_data):
    for x, character in enumerate(line):
        if character == '\n':
            continue
        if (x, y) in symbol_coordinates:
            # grid[y][x] = 'X'
            grid[y][x] = character

for number, coordinates in number_sequences:
    for i, coordinate in enumerate(coordinates):
        grid[coordinate[1]][coordinate[0]] = number[i]


print('\n'.join([''.join(line) for line in grid]))

print(output)