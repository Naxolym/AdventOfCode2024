import re
import arg_process

A_REGEX = re.compile(r'A')


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        search_grid = []
        for line in f.readlines():
            search_grid.append(line)
    f.close()

    for i in range(1, len(search_grid) - 1):
        found = A_REGEX.finditer(search_grid[i])
        for match in found:
            j = match.start()
            if j == 0 or j == len(search_grid[i]) - 1:
                continue
            if (search_grid[i - 1][j - 1] == 'S' and search_grid[i + 1][j + 1] == 'M'
                    or
                    search_grid[i - 1][j - 1] == 'M' and search_grid[i + 1][j + 1] == 'S'
            ):
                if (search_grid[i - 1][j + 1] == 'S' and search_grid[i + 1][j - 1] == 'M'
                        or
                        search_grid[i - 1][j + 1] == 'M' and search_grid[i + 1][j - 1] == 'S'
                ):
                    total += 1

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input41"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    main(input_file_name)
