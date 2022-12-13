from typing import Any
import functools

Packet = Any  # tuple[int | Packet, ...]


def parse_packet(s: str) -> Packet:
    s = s.replace("[", "(")
    s = s.replace("]", ",)")
    s = s.replace("(,)", "()")
    return eval(s)


def compare_packets(l: Packet, r: Packet) -> int:
    for l_v, r_v in zip(l, r):
        if isinstance(l_v, int) and isinstance(r_v, int):
            if l_v < r_v:
                return -1
            elif l_v > r_v:
                return +1
        elif isinstance(l_v, tuple) and isinstance(r_v, tuple):
            t = compare_packets(l_v, r_v)
            if t != 0:
                return t
        elif isinstance(l_v, tuple):
            t = compare_packets(l_v, (r_v,))
            if t != 0:
                return t
        else:
            t = compare_packets((l_v,), r_v)
            if t != 0:
                return t
    l_size, r_size = len(l), len(r)
    if l_size < r_size:
        return -1
    elif l_size > r_size:
        return +1
    else:
        return 0


def part_1(file_path: str) -> int:
    with open(file_path) as f:
        raw_packet_pairs = f.read().split("\n\n")
    packet_pairs: list[tuple[Packet, Packet]] = [
        (
            parse_packet(raw_packet_pair.split()[0]),
            parse_packet(raw_packet_pair.split()[1]),
        )
        for raw_packet_pair in raw_packet_pairs
    ]
    correctly_ordered_packet_pairs = []
    for idx, packet_pair in enumerate(packet_pairs):
        l, r = packet_pair
        if compare_packets(l, r) == -1:
            correctly_ordered_packet_pairs.append(idx + 1)
    return sum(correctly_ordered_packet_pairs)


def part_2(file_path: str) -> int:
    with open(file_path) as f:
        raw_packets = [line.strip() for line in f.readlines() if line.strip()]
    packets: list[Packet] = [parse_packet(raw_packet) for raw_packet in raw_packets]
    DIVIDER_PACKET_1 = ((2,),)
    DIVIDER_PACKET_2 = ((6,),)
    packets.append(DIVIDER_PACKET_1)
    packets.append(DIVIDER_PACKET_2)
    packets = sorted(packets, key=functools.cmp_to_key(compare_packets))
    return (packets.index(DIVIDER_PACKET_1) + 1) * (packets.index(DIVIDER_PACKET_2) + 1)
