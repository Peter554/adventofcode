use anyhow::Result;
use std::{fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(input
        .lines()
        .map(|line| {
            let digits = line
                .chars()
                .filter(char::is_ascii_digit)
                .collect::<Vec<_>>();
            let s = format!("{}{}", digits.first().unwrap(), digits.last().unwrap());
            s.parse::<i64>().unwrap()
        })
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let lines = input.lines().map(_first_and_last_digit).collect::<Vec<_>>();
    dbg!(&lines);
    Ok(lines
        .iter()
        .map(|(first_digit, last_digit)| {
            let s = format!("{}{}", first_digit, last_digit);
            s.parse::<i64>().unwrap()
        })
        .sum())
}

fn _first_and_last_digit(s: &str) -> (char, char) {
    let mut first_digit: Option<char> = None;
    let mut last_digit: Option<char> = None;

    let mut buf = String::new();
    for c in s.chars() {
        buf.push(c);
        let replaced_buf = _replace_numbers_dumb(&buf);
        if _contains_digit(&replaced_buf) {
            first_digit = Some(_first_digit(&replaced_buf));
            break;
        }
    }

    buf.clear();
    for c in s.chars().rev() {
        buf.push(c);
        let replaced_buf = _replace_numbers_dumb(&_reverse(&buf));
        if _contains_digit(&replaced_buf) {
            last_digit = Some(_first_digit(&replaced_buf));
            break;
        }
    }

    (first_digit.unwrap(), last_digit.unwrap())
}

fn _replace_numbers_dumb(s: &str) -> String {
    s.replace("one", "1")
        .replace("two", "2")
        .replace("three", "3")
        .replace("four", "4")
        .replace("five", "5")
        .replace("six", "6")
        .replace("seven", "7")
        .replace("eight", "8")
        .replace("nine", "9")
}

fn _contains_digit(s: &str) -> bool {
    s.chars().any(|c| char::is_ascii_digit(&c))
}

fn _first_digit(s: &str) -> char {
    s.chars().find(char::is_ascii_digit).unwrap()
}

fn _reverse(s: &str) -> String {
    s.chars().rev().collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input_path = Path::new("./src/day01/sample");
        assert_eq!(part1(input_path).unwrap(), 142);

        let input_path = Path::new("./src/day01/input");
        assert_eq!(part1(input_path).unwrap(), 53194);
    }

    #[test]
    fn test_part_2() {
        let input_path = Path::new("./src/day01/sample2");
        assert_eq!(part2(input_path).unwrap(), 281);

        let input_path = Path::new("./src/day01/input");
        assert_eq!(part2(input_path).unwrap(), 54249);
    }
}
