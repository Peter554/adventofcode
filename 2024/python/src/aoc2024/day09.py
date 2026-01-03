import uuid
from dataclasses import dataclass
from pathlib import Path


def part_1(input: Path) -> int:
    blocks = []
    address = 0
    occupied = True
    file_id = 0
    for c in input.read_text().strip():
        for _ in range(int(c)):
            blocks.append(Block(address, 1, file_id if occupied else None))
            address += 1
        occupied = not occupied
        if occupied:
            file_id += 1

    disk = Disk(blocks)
    disk.defragment()
    return disk.checksum()


def part_2(input: Path) -> int:
    blocks = []
    address = 0
    occupied = True
    file_id = 0
    for c in input.read_text().strip():
        size = int(c)
        blocks.append(Block(address, size, file_id if occupied else None))
        address += size
        occupied = not occupied
        if occupied:
            file_id += 1

    disk = Disk(blocks)
    disk.defragment()
    return disk.checksum()


@dataclass
class Block:
    address: int
    size: int
    file_id: int | None

    @property
    def is_vacant(self):
        return self.file_id is None

    @property
    def is_occupied(self):
        return not self.is_vacant


class Disk:
    def __init__(self, blocks: list[Block]):
        blocks = sorted(blocks, key=lambda b: b.address)
        self.occupied_blocks: list[Block] = [b for b in blocks if b.is_occupied]
        # Using a dict as a simple alternative to a doubly linked list,
        # since insertion order is preserved and delete is O(1).
        self.vacant_blocks: dict[str, Block] = {
            uuid.uuid4().hex: b for b in blocks if b.is_vacant
        }

    def defragment(self) -> None:
        for occupied_block in reversed(self.occupied_blocks):
            # Find the vacant block to occupy
            vacant_block_to_occupy_key: str | None = None
            for vacant_block_key, vacant_block in self.vacant_blocks.items():
                if vacant_block.address > occupied_block.address:
                    break
                if vacant_block.size < occupied_block.size:
                    continue
                vacant_block_to_occupy_key = vacant_block_key
                break

            # Occupy the vacant block
            if vacant_block_to_occupy_key is not None:
                vacant_block_to_occupy = self.vacant_blocks[vacant_block_to_occupy_key]
                occupied_block.address = vacant_block_to_occupy.address
                if vacant_block_to_occupy.size == occupied_block.size:
                    del self.vacant_blocks[vacant_block_to_occupy_key]
                else:
                    vacant_block_to_occupy.address += occupied_block.size
                    vacant_block_to_occupy.size -= occupied_block.size

    def checksum(self) -> int:
        return sum(
            i * (b.file_id or 0)
            for b in self.occupied_blocks
            for i in range(b.address, b.address + b.size)
        )
