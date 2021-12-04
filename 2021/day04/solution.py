import uuid
import copy
import itertools


class BingoCard:
    def __init__(self, numbers_to_positions: dict[int, tuple[int, int]]):
        assert len(numbers_to_positions) == 25
        assert set(numbers_to_positions.values()) == set(
            itertools.product(range(5), range(5))
        )

        self._id = uuid.uuid4().int
        self._numbers_to_positions = copy.deepcopy(numbers_to_positions)
        self._positions_to_numbers = {
            v: k for k, v in self._numbers_to_positions.items()
        }
        self._marks: set[tuple[int, int]] = set()

    def __hash__(self) -> int:
        return self._id

    def mark(self, number: int) -> None:
        if number in self._numbers_to_positions:
            self._marks.add(self._numbers_to_positions[number])

    @property
    def has_bingo(self) -> bool:
        for row in range(5):
            row_completed = True
            for col in range(5):
                if (row, col) not in self._marks:
                    row_completed = False
                    break
            if row_completed:
                return True
        for col in range(5):
            col_completed = True
            for row in range(5):
                if (row, col) not in self._marks:
                    col_completed = False
                    break
            if col_completed:
                return True
        return False

    @property
    def unmarked_numbers(self) -> list[int]:
        positions = set(self._positions_to_numbers) - self._marks
        return [self._positions_to_numbers[p] for p in positions]


def _parse_raw_data(raw_data: str) -> tuple[list[int], set[BingoCard]]:
    numbers = [int(n) for n in raw_data.split("\n\n")[0].split(",")]
    cards: set[BingoCard] = set()
    for data in raw_data.split("\n\n")[1:]:
        numbers_to_positions = {}
        for i, row in enumerate(data.split("\n")):
            row = row.replace("  ", " ").strip()
            for j, number in enumerate(row.split(" ")):
                numbers_to_positions[int(number)] = (i, j)
        cards.add(
            BingoCard(
                numbers_to_positions=numbers_to_positions,
            )
        )
    return numbers, cards


def part_1(file_path: str) -> int:
    with open(file_path, "r") as f:
        numbers, cards = _parse_raw_data(f.read())

    for number in numbers:
        for card in cards:
            card.mark(number)

        for card in cards:
            if card.has_bingo:
                return number * sum(card.unmarked_numbers)

    raise Exception("solution not found")


def part_2(file_path: str) -> int:
    with open(file_path, "r") as f:
        numbers, cards = _parse_raw_data(f.read())

    unfinished_cards = cards
    finished_cards: list[BingoCard] = []

    for number in numbers:
        for card in unfinished_cards:
            card.mark(number)

        for card in unfinished_cards.copy():
            if card.has_bingo:
                unfinished_cards.remove(card)
                finished_cards.append(card)

        if len(unfinished_cards) == 0:
            return number * sum(finished_cards[-1].unmarked_numbers)

    raise Exception("solution not found")
