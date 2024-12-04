import re
import arg_process

XMAS_REGEX = re.compile(r'XMAS')


def search_horizontal(line: str) -> int:
    found = 0
    findings = XMAS_REGEX.findall(line)
    found += len(findings)
    line = line[::-1]
    findings = XMAS_REGEX.findall(line)
    found += len(findings)
    return found


def transpose(m: list[str]) -> list[str]:
    transposed_matrix = []
    for i in range(len(m[0]) - 1):
        line = ''
        for j in range(len(m)):
            line += m[j][i]
        transposed_matrix.append(line)
    return transposed_matrix


def diagonal_transpose(m: list[str]) -> list[str]:
    horizontal_max = len(m[0]) - 1
    vertical_max = len(m)
    diagonal_matrix = ['' for j in range(vertical_max + horizontal_max)]
    for i in range(horizontal_max):
        for j in range(vertical_max):
            diagonal_matrix[i - j + vertical_max] += m[i][j]
    return diagonal_matrix


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        search_grid = []
        for line in f.readlines():
            search_grid.append(line)
    f.close()

    for line in search_grid:
        found = search_horizontal(line)
        total += found

    transposed = transpose(search_grid)

    for line in transposed:
        found = search_horizontal(line)
        total += found

    diag_transposed = diagonal_transpose(search_grid)
    for line in diag_transposed:
        found = search_horizontal(line)
        total += found

    reverse_search_grid = []
    for line in search_grid:
        reverse_search_grid.append(line[-2::-1] + '\n')

    diag_transposed = diagonal_transpose(reverse_search_grid)
    print(diag_transposed)
    for line in diag_transposed:
        found = search_horizontal(line)
        total += found

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
