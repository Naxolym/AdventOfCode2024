import re
import arg_process


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        for line in f.readlines():
            regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
            pairs = regex.findall(line)
            print(pairs)
            for pair in pairs:
                m = int(pair[0]) * int(pair[1])
                total += m
    f.close()

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
