use anyhow::Result;
use std::{fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let mut map = parse_input(&input);
    map.tilt_north();
    Ok(map.load())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let _ = input;
    Ok(42)
}

fn parse_input(input: &str) -> Map {
    let map = input
        .lines()
        .map(|row| {
            row.chars()
                .map(|c| match c {
                    '.' => Cell::Empty,
                    'O' => Cell::RoundRock,
                    '#' => Cell::CubeRock,
                    _ => panic!(),
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    Map { map }
}

#[derive(Debug, PartialEq, Eq, Clone)]
enum Cell {
    Empty,
    RoundRock,
    CubeRock,
}

struct Map {
    map: Vec<Vec<Cell>>,
}

impl Map {
    fn load(&self) -> i64 {
        self.map
            .iter()
            .map(|row| {
                row.iter()
                    .filter(|cell| matches!(cell, Cell::RoundRock))
                    .count()
            })
            .enumerate()
            .map(|(row_idx, round_rock_count)| round_rock_count * (self.map.len() - row_idx))
            .sum::<usize>() as i64
    }

    fn tilt_north(&mut self) {
        loop {
            let mut next_map = self.map.clone();
            for (row_idx, row) in self.map.iter().enumerate() {
                if row_idx == self.map.len() - 1 {
                    break;
                }
                for (col_idx, cell) in row.iter().enumerate() {
                    if matches!(cell, Cell::Empty)
                        && matches!(next_map[row_idx + 1][col_idx], Cell::RoundRock)
                    {
                        next_map[row_idx][col_idx] = Cell::RoundRock;
                        next_map[row_idx + 1][col_idx] = Cell::Empty;
                    }
                }
            }
            if next_map == self.map {
                return;
            } else {
                self.map = next_map;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day14/sample");
        assert_eq!(part1(input_path).unwrap(), 136);

        let input_path = Path::new("./src/day14/input");
        assert_eq!(part1(input_path).unwrap(), 109385);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day14/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day14/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
