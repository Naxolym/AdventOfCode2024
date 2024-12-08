import re
import arg_process

EQUATION_REGEX = re.compile(r'\d+')


def add(x: int, y: int) -> int:
    return x + y


def mult(x: int, y: int) -> int:
    return x * y


def calc_equation(nums: list, ops: list) -> int:
    result = nums[0]
    for i in range(len(ops)):
        result = ops[i](result, nums[i + 1])
    return result


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        equations = f.read()
        equations = equations.split('\n')
    f.close()

    for equation in equations:
        numbers = EQUATION_REGEX.findall(equation)
        numbers = [int(x) for x in numbers]
        target = numbers[0]
        numbers = numbers[1:]

        ops = []
        width = len(numbers) - 1
        permutations = 2 ** width
        for i in range(permutations):
            op = []
            for c in f'{i:0{width}b}':
                match c:
                    case '0':
                        op.append(add)
                    case '1':
                        op.append(mult)
            ops.append(op)
        for op in ops:
            result = calc_equation(numbers, op)
            if result == target:
                total += result
                break

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input71"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    main(input_file_name)
