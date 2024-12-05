import re
import arg_process

INSTRUCTION_SEPARATOR_REGEX = re.compile(r'\n\n')
RULE_REGEX = re.compile(r'(\d+)\|(\d+)')


def separate_instructions(instructions: str) -> tuple[str, str]:
    split = INSTRUCTION_SEPARATOR_REGEX.split(instructions)
    return split[0], split[1]


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        instructions = f.read()
    f.close()

    (ordering_rules, updates) = separate_instructions(instructions)
    ruleset = re.split('\n', ordering_rules)
    updateset = re.split('\n', updates)
    for update in updateset:
        bad_update = False
        while True:
            for rule in ruleset:
                numbers = RULE_REGEX.findall(rule)[0]
                first = re.search(numbers[0], update)
                if first is None:
                    continue
                first_index = first.start()
                second = re.search(numbers[1], update)
                if second is None:
                    continue
                second_index = second.start()
                if second_index < first_index:
                    bad_update = True
                    update = (update[:second_index] + first.group(0) +
                              update[second_index + 2:first_index] + second.group(0) +
                              update[first_index + 2:])
                    continue
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
                break
        if bad_update:
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
