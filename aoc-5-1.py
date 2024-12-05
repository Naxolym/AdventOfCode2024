import re
import arg_process

INSTRUCTION_SEPARATOR_REGEX = re.compile(r'\n\n')
RULE_REGEX = re.compile(r'(\d+)\|(\d+)')


def separate_instructions(instructions: str) -> tuple[str, str]:
    split = INSTRUCTION_SEPARATOR_REGEX.split(instructions)
    return split[0], split[1]


def available_numbers(rules: str) -> list[int]:
    numbers = re.findall(r'\d+', rules, re.MULTILINE)
    numbers = [int(x) for x in numbers]
    return list(set(numbers))


def rule_as_negative_set(full_set: list[int], rules: str) -> dict:
    ruleset = re.split('\n', rules)
    negative_set = {}
    for rule in ruleset:
        numbers = RULE_REGEX.findall(rule)[0]
        first = int(numbers[0])
        second = int(numbers[1])
        if first not in negative_set:
            negative_set[first] = full_set
        if second in negative_set[first]:
            negative_set[first].remove(second)
    return negative_set


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        instructions = f.read()
    f.close()

    (ordering_rules, updates) = separate_instructions(instructions)
    ruleset = re.split('\n', ordering_rules)
    updateset = re.split('\n', updates)
    for update in updateset:
        good_update = True
        for rule in ruleset:
            numbers = RULE_REGEX.findall(rule)[0]
            found = re.search(numbers[0], update)
            if found is None:
                continue
            first_index = found.start()
            found = re.search(numbers[1], update)
            if found is None:
                continue
            second_index = found.start()
            if second_index < first_index:
                good_update = False
                break
        if good_update:
            numberset = re.split(',', update)
            middle_number = numberset[len(numberset) // 2]
            total += int(middle_number)

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input51"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    main(input_file_name)
