from typing import List


def get_digits(code: int) -> List[int]:
    return list(map(lambda x: int(x), list(str(code))))


def contains_repeating(digits: List[int]) -> bool:
    for idx, _ in enumerate(digits):
        if idx == 0:
            continue
        if digits[idx] == digits[idx - 1]:
            return True

    return False


def contains_repeating_strict(digits: List[int]) -> bool:
    padded_digits = [-1] + digits + [-1]

    for i in range(1, len(digits)):
        match = padded_digits[i] == padded_digits[i + 1]
        different_left = padded_digits[i - 1] != padded_digits[i]
        different_right = padded_digits[i + 2] != padded_digits[i + 1]

        if match and different_left and different_right:
            return True

    return False


def are_increasing(digits: List[int]) -> bool:
    for idx, _ in enumerate(digits):
        if idx == 0:
            continue
        if digits[idx] < digits[idx - 1]:
            return False

    return True


def is_valid(code: int) -> bool:
    digits = get_digits(code)
    return contains_repeating(digits) and are_increasing(digits)


def is_valid_2(code: int) -> bool:
    digits = get_digits(code)
    return contains_repeating_strict(digits) and are_increasing(digits)


if __name__ == "__main__":
    lower = 172851
    upper = 675869

    all_codes = range(lower, upper + 1)
    valid_codes = [code for code in all_codes if is_valid(code)]

    print("Part 1")
    print("# of valid codes = {}".format(len(valid_codes)))

    valid_codes = [code for code in all_codes if is_valid_2(code)]

    print("Part 2")
    print("# of valid codes = {}".format(len(valid_codes)))
