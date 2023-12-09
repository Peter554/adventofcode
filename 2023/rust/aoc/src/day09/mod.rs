use anyhow::Result;
use std::{collections::VecDeque, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(input
        .lines()
        .map(|line| {
            line.split_ascii_whitespace()
                .map(|s| s.parse::<i64>().unwrap())
                .collect::<Vec<_>>()
        })
        .map(extrapolate)
        .map(|numbers| *numbers.last().unwrap())
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(input
        .lines()
        .map(|line| {
            line.split_ascii_whitespace()
                .map(|s| s.parse::<i64>().unwrap())
                .collect::<VecDeque<_>>()
        })
        .map(extrapolate_backwards)
        .map(|numbers| numbers[0])
        .sum())
}

fn extrapolate(mut numbers: Vec<i64>) -> Vec<i64> {
    if numbers.iter().all(|n| *n == 0) {
        numbers.push(0);
        return numbers;
    }
    let diffs = numbers
        .windows(2)
        .map(|window| window[1] - window[0])
        .collect::<Vec<_>>();
    let diffs = extrapolate(diffs);
    numbers.push(*numbers.last().unwrap() + diffs.last().unwrap());
    numbers
}

fn extrapolate_backwards(mut numbers: VecDeque<i64>) -> VecDeque<i64> {
    if numbers.iter().all(|n| *n == 0) {
        numbers.push_front(0);
        return numbers;
    }
    let diffs = numbers
        .iter()
        .collect::<Vec<_>>()
        .windows(2)
        .map(|window| window[1] - window[0])
        .collect::<VecDeque<_>>();
    let diffs = extrapolate_backwards(diffs);
    numbers.push_front(numbers[0] - diffs[0]);
    numbers
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day09/sample");
        assert_eq!(part1(input_path).unwrap(), 114);

        let input_path = Path::new("./src/day09/input");
        assert_eq!(part1(input_path).unwrap(), 1806615041);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day09/sample");
        assert_eq!(part2(input_path).unwrap(), 2);

        let input_path = Path::new("./src/day09/input");
        assert_eq!(part2(input_path).unwrap(), 1211);
    }
}
