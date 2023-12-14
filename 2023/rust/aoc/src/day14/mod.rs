use anyhow::Result;
use std::{collections::HashMap, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let mut map = parse_input(&input);
    map.tilt_north();
    Ok(map.load())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let mut map = parse_input(&input);

    let mut hm = HashMap::new();
    let mut iterations_remaining = 1000000000;
    while iterations_remaining > 0 {
        map.tilt_north();
        map.tilt_west();
        map.tilt_south();
        map.tilt_east();
        iterations_remaining -= 1;
        if let Some(previous_iterations_remaining) = hm.get(&map) {
            // Cycle - fast forward!
            let cycle_length = previous_iterations_remaining - iterations_remaining;
            iterations_remaining %= cycle_length;
        } else {
            hm.insert(map.clone(), iterations_remaining);
        }
    }

    Ok(map.load())
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

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
enum Cell {
    Empty,
    RoundRock,
    CubeRock,
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
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
        for col_idx in 0..self.map[0].len() {
            let mut drop_idx = 0;
            for row_idx in 0..self.map.len() {
                if matches!(self.map[row_idx][col_idx], Cell::RoundRock) {
                    self.map[row_idx][col_idx] = Cell::Empty;
                    self.map[drop_idx][col_idx] = Cell::RoundRock;
                    drop_idx += 1;
                } else if matches!(self.map[row_idx][col_idx], Cell::CubeRock) {
                    drop_idx = row_idx + 1;
                }
            }
        }
    }

    fn tilt_south(&mut self) {
        for col_idx in 0..self.map[0].len() {
            let mut drop_idx = self.map.len() - 1;
            for row_idx in (0..self.map.len()).rev() {
                if matches!(self.map[row_idx][col_idx], Cell::RoundRock) {
                    self.map[row_idx][col_idx] = Cell::Empty;
                    self.map[drop_idx][col_idx] = Cell::RoundRock;
                    if drop_idx == 0 {
                        break;
                    }
                    drop_idx -= 1;
                } else if matches!(self.map[row_idx][col_idx], Cell::CubeRock) {
                    if row_idx == 0 {
                        break;
                    }
                    drop_idx = row_idx - 1;
                }
            }
        }
    }

    fn tilt_west(&mut self) {
        for row_idx in 0..self.map.len() {
            let mut drop_idx = 0;
            for col_idx in 0..self.map[0].len() {
                if matches!(self.map[row_idx][col_idx], Cell::RoundRock) {
                    self.map[row_idx][col_idx] = Cell::Empty;
                    self.map[row_idx][drop_idx] = Cell::RoundRock;
                    drop_idx += 1;
                } else if matches!(self.map[row_idx][col_idx], Cell::CubeRock) {
                    drop_idx = col_idx + 1;
                }
            }
        }
    }

    fn tilt_east(&mut self) {
        for row_idx in 0..self.map.len() {
            let mut drop_idx = self.map[0].len() - 1;
            for col_idx in (0..self.map[0].len()).rev() {
                if matches!(self.map[row_idx][col_idx], Cell::RoundRock) {
                    self.map[row_idx][col_idx] = Cell::Empty;
                    self.map[row_idx][drop_idx] = Cell::RoundRock;
                    if drop_idx == 0 {
                        break;
                    }
                    drop_idx -= 1;
                } else if matches!(self.map[row_idx][col_idx], Cell::CubeRock) {
                    if col_idx == 0 {
                        break;
                    }
                    drop_idx = col_idx - 1;
                }
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
        assert_eq!(part2(input_path).unwrap(), 64);

        let input_path = Path::new("./src/day14/input");
        assert_eq!(part2(input_path).unwrap(), 93102);
    }
}
