import re
import arg_process


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        left = list()
        right = dict()
        for line in f.readlines():
            regex = re.compile(r'\d+')
            numbers = regex.findall(line)
            left.append(int(numbers[0]))
            num_right = int(numbers[1])
            if num_right in right:
                right[num_right] += 1
            else:
                right[num_right] = 1
    f.close()
    for num in left:
        if num in right:
            total += num * right[num]

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input11"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    main(input_file_name)
