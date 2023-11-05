use aoc::day02;

#[test]
fn test_part1() {
    assert_eq!(day02::part1("./data/day02/sample"), 58 + 43);
    assert_eq!(day02::part1("./data/day02/input"), 1598415);
}

#[test]
fn test_part2() {
    assert_eq!(day02::part2("./data/day02/sample"), 34 + 14);
    assert_eq!(day02::part2("./data/day02/input"), 3812909);
}
