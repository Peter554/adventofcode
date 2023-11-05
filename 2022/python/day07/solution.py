from __future__ import annotations

import dataclasses
import re


@dataclasses.dataclass
class File:
    name: str
    size: int


@dataclasses.dataclass
class Directory:
    name: str
    parent: Directory | None
    children: dict[str, Directory]
    files: dict[str, File]

    @property
    def size(self) -> int:
        return sum(file.size for file in self.files.values()) + sum(
            child.size for child in self.children.values()
        )


@dataclasses.dataclass
class FileSystem:
    root: Directory
    pwd: Directory


def parse_file_system(terminal_output: list[str]) -> FileSystem:
    assert terminal_output[0] == "$ cd /"
    root = Directory("/", None, {}, {})
    fs = FileSystem(root, root)
    for line in terminal_output[1:]:
        if match := re.match(r"^\$ cd ([a-z]+)$", line):
            fs.pwd = fs.pwd.children[match.group(1)]
        elif line == "$ cd ..":
            assert fs.pwd.parent is not None
            fs.pwd = fs.pwd.parent
        elif line == "$ ls":
            # assuming the terminal output is valid, we can skip this line, for a quick solution...
            continue
        elif match := re.match(r"^dir ([a-z]+)$", line):
            child_name = match.group(1)
            if child_name not in fs.pwd.children:
                fs.pwd.children[child_name] = Directory(child_name, fs.pwd, {}, {})
        elif match := re.match(r"^([0-9]+) ([a-z.]+)$", line):
            file_size = int(match.group(1))
            file_name = match.group(2)
            fs.pwd.files[file_name] = File(file_name, file_size)
        else:
            assert False
    return fs


def list_all_directories(root: Directory) -> list[Directory]:
    all_directories = [root]
    for child in root.children.values():
        all_directories.extend(list_all_directories(child))
    return all_directories


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        terminal_output = [line.strip() for line in f.readlines()]
    fs = parse_file_system(terminal_output)
    all_directories = list_all_directories(fs.root)
    return sum(
        directory.size for directory in all_directories if directory.size <= 100000
    )


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        terminal_output = [line.strip() for line in f.readlines()]
    fs = parse_file_system(terminal_output)
    all_directories = list_all_directories(fs.root)
    unused_space = 70000000 - fs.root.size
    space_needed = 30000000 - unused_space
    directories_by_size = sorted(
        [(d.size, d) for d in all_directories], key=lambda x: x[0]
    )
    for directory_size, _ in directories_by_size:
        if directory_size >= space_needed:
            return directory_size
    assert False
