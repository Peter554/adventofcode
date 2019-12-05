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


if __name__ == "__main__":
    lower = 172851
    upper = 675869

    all_codes = range(lower, upper + 1)
    valid_codes = [code for code in all_codes if is_valid(code)]

    print('Part 1')
    print('# of valid codes = {}'.format(len(valid_codes)))
