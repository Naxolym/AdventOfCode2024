import re
import arg_process


def is_sorted(mylist: list) -> bool:
    ascending = all(mylist[i] < mylist[i + 1] for i in range(len(mylist) - 1))
    descending = all(mylist[i] > mylist[i + 1] for i in range(len(mylist) - 1))
    return ascending or descending


def check_slope(mylist: list) -> bool:
    MIN_DIST = 1
    MAX_DIST = 3
    return all(MIN_DIST <= abs(mylist[i] - mylist[i + 1]) <= MAX_DIST for i in range(len(mylist) - 1))


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        for report in f.readlines():
            regex = re.compile(r'\d+')
            levels = [int(x) for x in regex.findall(report)]
            if is_sorted(levels) and check_slope(levels):
                total += 1
                continue
            for i in range(len(levels)):
                new_levels = levels[:i] + levels[i + 1:]
                if not is_sorted(new_levels):
                    continue
                if not check_slope(new_levels):
                    continue
                total += 1
                break
    f.close()

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input21"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    main(input_file_name)
