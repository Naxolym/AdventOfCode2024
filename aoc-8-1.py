import re
import arg_process
from dataclasses import dataclass
import time

ANTENNA_REGEX = re.compile(r'[a-zA-Z0-9]')


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


@dataclass
class Antenna:
    frequency: str
    position: Position

    def __hash__(self):
        return hash(self.frequency)


def parse_antennae(grid: list) -> dict:
    grouped_ants = {}
    for line in range(len(grid)):
        antennae = ANTENNA_REGEX.finditer(grid[line])
        if antennae is None:
            continue
        for antenna in antennae:
            frequency = antenna.group(0)
            if frequency not in grouped_ants:
                grouped_ants[frequency] = []
            grouped_ants[frequency].append(Antenna(antenna.group(0), Position(line, antenna.start())))
    for frequency in grouped_ants:
        grouped_ants[frequency].sort(key=lambda x: x.position.y)
    return grouped_ants


def calc_slope(p1: Position, p2: Position) -> Position:
    return p2 - p1


def node_in_grid(node: Position, grid: list) -> bool:
    length = len(grid[0])
    height = len(grid)
    if node.x < 0 or node.x >= height:
        return False
    if node.y < 0 or node.y >= length:
        return False
    return True


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        grid = f.read()
    f.close()

    grid = grid.split('\n')
    antennae = parse_antennae(grid)
    nodes = {}
    for frequency in antennae:
        for i in range(len(antennae[frequency])):
            for j in range(i + 1, len(antennae[frequency])):
                a1 = antennae[frequency][i].position
                a2 = antennae[frequency][j].position
                slope = calc_slope(a1, a2)
                n1 = a1 - slope
                n2 = a2 + slope
                if node_in_grid(n1, grid):
                    nodes[n1] = 1
                if node_in_grid(n2, grid):
                    nodes[n2] = 1
    total = len(nodes)

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input81"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    start = time.time()
    main(input_file_name)
    print(time.time() - start)
