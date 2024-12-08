import re
import arg_process
import time
import multiprocessing as mp
from functools import lru_cache
import numpy as np

EQUATION_REGEX = re.compile(r'\d+')


@lru_cache(maxsize=None)
def add(x: int, y: int) -> int:
    return x + y


@lru_cache(maxsize=None)
def mult(x: int, y: int) -> int:
    return x * y


@lru_cache(maxsize=None)
def concat(x: int, y: int) -> int:
    return int(f'{x}{y}')


@lru_cache(maxsize=None)
def ternary(n: int) -> str:
    return np.base_repr(n, base=3)


def calc_equation(nums: list, ops: list) -> int:
    result = nums[0]
    for i in range(len(ops)):
        result = ops[i](result, nums[i + 1])
    return result


@lru_cache(maxsize=None)
def calc_permutations(width: int) -> list:
    ops = []
    permutations = 3 ** width
    for i in range(permutations):
        op = []
        for c in f'{ternary(i).zfill(width)}':
            match c:
                case '0':
                    op.append(add)
                case '1':
                    op.append(mult)
                case '2':
                    op.append(concat)
        ops.append(op)
    return ops


def solve_equation(equation: str) -> int:
    numbers = EQUATION_REGEX.findall(equation)
    numbers = [int(x) for x in numbers]
    target = numbers[0]
    numbers = numbers[1:]

    width = len(numbers) - 1
    ops = calc_permutations(width)

    for op in ops:
        result = calc_equation(numbers, op)
        if result == target:
            return result
    return 0


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        equations = f.read()
        equations = equations.split('\n')
    f.close()

    p = mp.Pool()
    res = p.map(solve_equation, equations)
    total = np.sum(res)
    # for equation in equations:
    #    total += solve_equation(equation)

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input71"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    start = time.time()
    main(input_file_name)
    print(time.time() - start)
