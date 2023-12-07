use anyhow::Result;
use std::{collections::HashSet, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (numbers, symbols) = parse_input(&input)?;
    let symbol_neighborhoods = symbols.iter().fold(HashSet::new(), |mut hs, s| {
        hs.extend(s.neighborhood.clone());
        hs
    });
    Ok(numbers
        .iter()
        .filter(|n| !symbol_neighborhoods.is_disjoint(&n.points))
        .map(|n| n.value as i64)
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (numbers, symbols) = parse_input(&input)?;
    Ok(symbols
        .iter()
        .filter(|s| s.value == '*')
        .filter_map(|s| {
            let neighborhood_numbers = numbers
                .iter()
                .filter(|n| !s.neighborhood.is_disjoint(&n.points))
                .collect::<Vec<_>>();
            if neighborhood_numbers.len() == 2 {
                Some(neighborhood_numbers[0].value as i64 * neighborhood_numbers[1].value as i64)
            } else {
                None
            }
        })
        .sum())
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Point {
    row: usize,
    col: usize,
}

#[derive(Debug)]
struct Number {
    value: u16,
    points: HashSet<Point>,
}

impl Number {
    fn new(value: u16, row: usize, col: usize) -> Self {
        let mut points = HashSet::new();
        for delta_col_idx in 0..value.to_string().len() {
            points.insert(Point {
                row,
                col: col + delta_col_idx,
            });
        }
        Number { value, points }
    }
}

#[derive(Debug)]
struct Symbol {
    value: char,
    neighborhood: HashSet<Point>,
}

impl Symbol {
    fn new(value: char, row: usize, col: usize) -> Self {
        let mut neighborhood = HashSet::new();
        for row_idx in row - 1..=row + 1 {
            for col_idx in col - 1..=col + 1 {
                if row == row_idx && col == col_idx {
                    continue;
                }
                neighborhood.insert(Point {
                    row: row_idx,
                    col: col_idx,
                });
            }
        }
        Symbol {
            value,
            neighborhood,
        }
    }
}

fn parse_input(input: &str) -> Result<(Vec<Number>, Vec<Symbol>)> {
    let mut numbers = vec![];
    let mut symbols = vec![];
    for (row_idx, row) in input.lines().enumerate() {
        let mut row = row.chars().enumerate().peekable();
        while row.peek().is_some() {
            match row.next() {
                Some((_, '.')) => {}
                Some((col_idx, first_digit @ '0'..='9')) => {
                    let mut digits = String::from(first_digit);
                    while let Some((_, '0'..='9')) = row.peek() {
                        let (_, digit) = row.next().unwrap();
                        digits.push(digit);
                    }
                    numbers.push(Number::new(digits.parse()?, row_idx, col_idx));
                }
                Some((col_idx, symbol)) => {
                    symbols.push(Symbol::new(symbol, row_idx, col_idx));
                }
                _ => panic!(),
            }
        }
    }
    Ok((numbers, symbols))
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day03/sample");
        assert_eq!(part1(input_path).unwrap(), 4361);

        let input_path = Path::new("./src/day03/input");
        assert_eq!(part1(input_path).unwrap(), 549908);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day03/sample");
        assert_eq!(part2(input_path).unwrap(), 467835);

        let input_path = Path::new("./src/day03/input");
        assert_eq!(part2(input_path).unwrap(), 81166799);
    }
}
