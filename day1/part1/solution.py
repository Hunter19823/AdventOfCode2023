# Read input.txt
with open('input.txt', 'r') as f:
    # Print the result
    print(
        # Sum all the numbers
        sum(
            [
                # Take the first and last numeric characters, put them together, then
                # parse them as an integer
                int(f"{numbers[0]}{numbers[-1]}")
                # Map all the lines to only numeric sequences.
                for numbers in map(
                    # Use the following function to map a line to a numeric sequence
                    lambda line: ''.join([
                        # Only keep the numeric characters from the
                        # current
                        character
                        for character in line if character.isdigit()
                    ]),
                    f.readlines()
                )
            ]
        )
    )
