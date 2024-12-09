import arg_process
import time


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        disk_map = f.readline()
    f.close()
    files = [int(x) for x in disk_map[::2]]
    spaces = [int(x) for x in disk_map[1::2]]
    files_unzip = []
    for i in range(len(files)):
        files_unzip += [i] * files[i]
    files_compact = []
    index = 0
    target_length = len(files_unzip)
    while len(files_compact) < target_length:
        files_compact += [index] * files[index]
        pop_amount = spaces[index] * -1
        index += 1
        if pop_amount == 0:
            continue
        files_unzip, popped = files_unzip[:pop_amount], files_unzip[pop_amount:]
        files_compact += popped[::-1]

    files_compact = files_compact[:target_length]

    for i in range(len(files_compact)):
        total += i * files_compact[i]
    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input91"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    start = time.time()
    main(input_file_name)
    print(time.time() - start)
