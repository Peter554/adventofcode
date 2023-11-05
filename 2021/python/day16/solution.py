from __future__ import annotations

import typing
import dataclasses


@dataclasses.dataclass(frozen=True)
class LiteralPacket:
    version: int
    value: int


@dataclasses.dataclass(frozen=True)
class OperatorPacket:
    version: int
    type_id: int
    sub_packets: tuple[Packet, ...]

    @property
    def value(self) -> int:
        if self.type_id == 0:
            return sum([sub_packet.value for sub_packet in self.sub_packets])
        elif self.type_id == 1:
            v = 1
            for sub_packet in self.sub_packets:
                v *= sub_packet.value
            return v
        elif self.type_id == 2:
            return min([sub_packet.value for sub_packet in self.sub_packets])
        elif self.type_id == 3:
            return max([sub_packet.value for sub_packet in self.sub_packets])
        elif self.type_id == 5:
            return 1 if self.sub_packets[0].value > self.sub_packets[1].value else 0
        elif self.type_id == 6:
            return 1 if self.sub_packets[0].value < self.sub_packets[1].value else 0
        elif self.type_id == 7:
            return 1 if self.sub_packets[0].value == self.sub_packets[1].value else 0
        else:
            raise Exception("invalid packet")


Packet = typing.Union[LiteralPacket, OperatorPacket]


def parse_packet(start_idx: int, bits: str) -> tuple[int, Packet]:
    i = start_idx
    version = int(bits[i : i + 3], 2)
    i += 3
    type_id = int(bits[i : i + 3], 2)
    i += 3
    if type_id == 4:
        value_bits = ""
        while True:
            chunk = bits[i : i + 5]
            i += 5
            value_bits += chunk[1:]
            if chunk[0] == "0":
                break
        value = int(value_bits, 2)
        return i, LiteralPacket(version=version, value=value)
    else:
        sub_packets = []
        length_type_id = bits[i]
        i += 1
        if length_type_id == "0":
            n_sub_packet_bits = int(bits[i : i + 15], 2)
            i += 15
            i_done = i + n_sub_packet_bits
            while i < i_done:
                i, sub_packet = parse_packet(i, bits)
                sub_packets.append(sub_packet)
        else:
            n_sub_packets = int(bits[i : i + 11], 2)
            i += 11
            for _ in range(n_sub_packets):
                i, sub_packet = parse_packet(i, bits)
                sub_packets.append(sub_packet)
        return i, OperatorPacket(
            version=version, type_id=type_id, sub_packets=tuple(sub_packets)
        )


def sum_versions(packet: Packet) -> int:
    if isinstance(packet, LiteralPacket):
        return packet.version
    elif isinstance(packet, OperatorPacket):
        return packet.version + sum([sum_versions(p) for p in packet.sub_packets])
    else:
        raise Exception("invalid packet")


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        hx = f.read().strip()
    bits = ""
    for h in list(hx):
        bits += bin(int(h, 16))[2:].zfill(4)
    _, packet = parse_packet(0, bits)
    return sum_versions(packet)


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        hx = f.read().strip()
    bits = ""
    for h in list(hx):
        bits += bin(int(h, 16))[2:].zfill(4)
    _, packet = parse_packet(0, bits)
    return packet.value
