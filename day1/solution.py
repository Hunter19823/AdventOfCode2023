# Read input.txt
with open('input.txt', 'r') as f:
    # Print the result
    print(
        # Sum all the numbers
        sum(
            [
                # Parse the number made from the first and last character
                int(f'{numeric[0]}{numeric[-1]}')
                # Loop through every line in the file
                for line in f.readlines()
                # Loop through every character in the line,
                # selecting only numeric characters
                for numeric in line if numeric.isdigit()
            ]
        )
    )
