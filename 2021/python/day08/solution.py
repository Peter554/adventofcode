import re
import typing


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    count = 0
    for line in lines:
        output_words = re.sub(r".*\|", "", line).split()
        for output_word in output_words:
            if len(output_word) in (2, 3, 4, 7):
                count += 1
    return count


def decode_words(words: list[str]) -> typing.Callable[[str], int]:
    def parse_word(word: str) -> int:
        n = 0
        for i, c in enumerate("abcdefg"):
            if c in word:
                n |= 1 << i
        return n

    codes = set([parse_word(w) for w in words])

    def pop_code(condition: typing.Callable[[int], bool]) -> int:
        matched_codes = list(filter(condition, codes))
        assert len(matched_codes) == 1
        codes.remove(matched_codes[0])
        return matched_codes[0]

    int_to_code: dict[int, int] = {}
    int_to_code[1] = pop_code(lambda c: bin(c).count("1") == 2)
    int_to_code[4] = pop_code(lambda c: bin(c).count("1") == 4)
    int_to_code[7] = pop_code(lambda c: bin(c).count("1") == 3)
    int_to_code[8] = pop_code(lambda c: bin(c).count("1") == 7)
    int_to_code[6] = pop_code(
        lambda c: bin(c).count("1") == 6 and c & int_to_code[1] != int_to_code[1]
    )
    int_to_code[9] = pop_code(
        lambda c: bin(c).count("1") == 6 and c & int_to_code[4] == int_to_code[4]
    )
    int_to_code[0] = pop_code(lambda c: bin(c).count("1") == 6)
    int_to_code[5] = pop_code(lambda c: c == (int_to_code[6] & int_to_code[9]))
    int_to_code[3] = pop_code(lambda c: c & int_to_code[1] == int_to_code[1])
    int_to_code[2] = pop_code(lambda c: True)

    code_to_int = {v: k for k, v in int_to_code.items()}

    def word_to_int(word: str) -> int:
        return code_to_int[parse_word(word)]

    return word_to_int


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    count = 0
    for line in lines:
        word_to_int = decode_words(line.replace(" | ", " ").split())
        output_words = re.sub(r".*\|", "", line).split()
        s = ""
        for output_word in output_words:
            s += str(word_to_int(output_word))
        count += int(s)
    return count
