def side_to_side_strings(strings, spacesBetween: int = 1):
    line_sizes = []
    summed_string = ""
    how_many_lines = max(len(i.split("\n")) for i in strings)

    for string in strings:
        max_count = 0
        actual_count = 0

        for char in string:
            if char == '\n':
                max_count = max([actual_count, max_count])
                actual_count = 0
            else:
                actual_count += 1

        max_count = max(actual_count, max_count)
        line_sizes.append(max_count)

    for i in range(how_many_lines):
        for string_number, string in enumerate(strings, 0):
            partial = ""

            try:
                partial += string.split('\n')[i]
            except:
                pass

            for _space in range(line_sizes[string_number] - len(partial) + spacesBetween):
                partial += " "

            summed_string += partial

        summed_string += "\n"

    return summed_string
