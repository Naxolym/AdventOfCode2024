import arg_process
import time
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash(f'{self.x}{self.y}')


def dfs(start: Position, grid: list) -> int:
    directions = [Position(-1, 0)
        , Position(0, 1)
        , Position(1, 0)
        , Position(0, -1)]

    found = {}
    good_dir = [start]
    while True:
        cur = good_dir.pop()
        height = grid[cur.x][cur.y]
        for direction in directions:
            step = cur + direction
            if step.x < 0 or step.x >= len(grid[0]) or step.y < 0 or step.y >= len(grid):
                continue
            step_height = grid[step.x][step.y]
            if step_height - height != 1:
                continue
            if step_height == 9:
                if step not in found:
                    found[step] = 1
                continue
            good_dir.append(step)
        if len(good_dir) == 0:
            break
    return len(found)


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        file = f.read()
    f.close()
    file = file.split('\n')
    topology_map = [[int(x) for x in line] for line in file]
    trailheads = []
    for i in range(len(topology_map)):
        for j in range(len(topology_map[i])):
            if topology_map[i][j] == 0:
                trailheads.append(Position(i, j))
    for trailhead in trailheads:
        total += dfs(trailhead, topology_map)

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input101"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    start = time.time()
    main(input_file_name)
    print(time.time() - start)
