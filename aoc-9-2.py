import arg_process
import time
from dataclasses import dataclass


@dataclass
class DiskElement:
    startpos: int
    length: int


@dataclass
class File(DiskElement):
    identifier: int

    def compute_checksum(self) -> int:
        checksum = 0
        for i in range(self.length):
            checksum += (self.startpos + i) * self.identifier
        return checksum


@dataclass
class Space(DiskElement):
    pass


class DiskException(Exception):

    def __str__(self):
        return self.args[0]


class Disk:
    size: int
    files: list[File]
    spaces: list[Space]

    def __init__(self, disk_map: str):
        disk_map = [int(x) for x in disk_map]
        self.size = sum(disk_map)
        curpos = 0
        self.files = []
        self.spaces = []
        for i in range(len(disk_map)):
            element_length = disk_map[i]
            if element_length == 0:
                continue
            if i % 2 == 0:
                self.files.append(File(curpos, element_length, i // 2))
            else:
                self.spaces.append(Space(curpos, element_length))
            curpos += element_length

    def move_file_to_space(self, file_index: int, space_index: int):
        if file_index >= len(self.files):
            raise DiskException('File Index too big!')
        if space_index >= len(self.spaces):
            raise DiskException('Space Index too big!')
        file = self.files[file_index]
        space = self.spaces[space_index]
        if file.length > space.length:
            raise DiskException('File bigger than available Space!')
        file.startpos = space.startpos
        self.files[file_index] = file
        space.length = space.length - file.length
        if space.length == 0:
            self.spaces.pop(space_index)
            return
        space.startpos = space.startpos + file.length
        self.spaces[space_index] = space

    def compute_checksum(self) -> int:
        checksum = 0
        for file in self.files:
            checksum += file.compute_checksum()
        return checksum

    def compact(self):
        for file in range(len(self.files) - 1, -1, -1):
            for space in range(len(self.spaces)):
                if self.spaces[space].startpos > self.files[file].startpos:
                    break
                if self.files[file].length > self.spaces[space].length:
                    continue
                try:
                    self.move_file_to_space(file, space)
                    break
                except DiskException as e:
                    print(e)

    def __str__(self) -> str:
        return (f'Size: {self.size} \n'
                f'Files: {self.files} \n'
                f'Spaces: {self.spaces}')


def main(input_file_name: str):
    total = 0
    with open(input_file_name, "r") as f:
        disk_map = f.readline()
    f.close()
    d = Disk(disk_map)
    d.compact()
    total = d.compute_checksum()

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
