import re
import arg_process


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        full_line = ''
        for line in f.readlines():
            full_line += line
    f.close()

    regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    do_not = re.compile(r'don\'t')
    do = re.compile(r'do\(\)')
    splat = do_not.split(full_line)
    clean_line = splat[0]
    for i in range(1, len(splat)):
        splatoon = do.split(splat[i])
        clean_line += ''.join(splatoon[1:])

    pairs = regex.findall(clean_line)
    for pair in pairs:
        m = int(pair[0]) * int(pair[1])
        total += m

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input31"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    main(input_file_name)
