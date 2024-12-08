import re
import arg_process
from dataclasses import dataclass
from enum import IntEnum


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def from_text(cls, string: str):
        match string:
            case '^':
                return cls.UP
            case '>':
                return cls.RIGHT
            case 'v':
                return cls.DOWN
            case '<':
                return cls.LEFT


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Guard:
    position: Position
    direction: Direction

    def update_position(self) -> Position:
        match self.direction:
            case Direction.UP:
                self.position = Position(self.position.x - 1, self.position.y)
                return self.position
            case Direction.RIGHT:
                self.position = Position(self.position.x, self.position.y + 1)
                return self.position
            case Direction.DOWN:
                self.position = Position(self.position.x + 1, self.position.y)
                return self.position
            case Direction.LEFT:
                self.position = Position(self.position.x, self.position.y - 1)
                return self.position

    def update_direction(self):
        self.direction = (self.direction + 1) % 4


class Grid:
    height: int
    length: int
    grid: list[str]
    visited: list[list]
    steps: int
    guard: Guard

    def __init__(self, grid: list[str]):
        self.grid = grid
        self.height = len(grid)
        self.length = len(grid[0])
        self.visited = [[0 for y in range(self.length)] for x in range(self.height)]
        self.steps = 0
        for line in range(len(grid)):
            found = re.search('[\^>v<]', grid[line])
            if found is None:
                continue
            self.guard = Guard(Position(line, found.start()), Direction.from_text(found.group(0)))

    def is_loop(self) -> bool:
        if self.steps > 2 * self.height * self.length:
            return True
        return False

    def move_guard(self) -> bool:
        if self.is_loop():
            return False
        self.visited[self.guard.position.x][self.guard.position.y] = 1
        prev_position = self.guard.position
        self.guard.update_position()
        if (self.guard.position.x < 0 or self.guard.position.x >= self.height
                or self.guard.position.y < 0 or self.guard.position.y >= self.length):
            return False
        if self.grid[self.guard.position.x][self.guard.position.y] == '#':
            self.guard.update_direction()
            self.guard.position = prev_position
            return True
        self.steps += 1
        return True

    def count_visited(self) -> int:
        visits = 0
        for l in self.visited:
            visits += sum(l)
        return visits


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        grid = f.read()
        grid = grid.split('\n')
    f.close()
    griddy = Grid(grid)
    success = True
    while success:
        success = griddy.move_guard()
    obstacle_positions = griddy.visited
    for i in range(len(obstacle_positions)):
        for j in range(len(obstacle_positions[i])):
            if obstacle_positions[i][j] == 0:
                continue
            if grid[i][j] == '^':
                continue
            grid_mod = grid[:i]
            grid_mod.append(grid[i][:j] + '#' + grid[i][j + 1:])
            for line in grid[i + 1:]:
                grid_mod.append(line)
            griddy = Grid(grid_mod)
            success = True
            while success:
                success = griddy.move_guard()
            if griddy.is_loop():
                total += 1

    print(f'total = {total}')


if __name__ == "__main__":
    input_file = "input61"
    input_file_suffix = ""
    try:
        input_file_suffix = arg_process.process_args()
    except arg_process.ArgumentException as e:
        print(e.args[0])
    input_file_name = f'{input_file}_{input_file_suffix}.txt'
    main(input_file_name)
