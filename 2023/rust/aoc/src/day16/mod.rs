use anyhow::Result;
use itertools::Itertools;
use std::{collections::HashSet, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let grid = parse_input(&input);
    let start = State::new(0, 0, Direction::Right);
    Ok(count_energized_tiles(&grid, start))
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let grid = parse_input(&input);

    let mut start_configurations = vec![];
    for row_idx in 0..grid.len() {
        start_configurations.push(State::new(row_idx as isize, 0, Direction::Right));
        start_configurations.push(State::new(
            row_idx as isize,
            grid[0].len() as isize - 1,
            Direction::Left,
        ));
    }
    for col_idx in 0..grid[0].len() {
        start_configurations.push(State::new(0, col_idx as isize, Direction::Down));
        start_configurations.push(State::new(
            grid.len() as isize - 1,
            col_idx as isize,
            Direction::Up,
        ));
    }

    Ok(start_configurations
        .into_iter()
        .map(|start| count_energized_tiles(&grid, start))
        .max()
        .unwrap())
}

fn parse_input(s: &str) -> Vec<Vec<Cell>> {
    s.lines()
        .map(|row| {
            row.chars()
                .map(|c| match c {
                    '.' => Cell::Empty,
                    '/' => Cell::MirrorLU,
                    '\\' => Cell::MirrorRU,
                    '-' => Cell::SplitterH,
                    '|' => Cell::SplitterV,
                    _ => panic!(),
                })
                .collect()
        })
        .collect()
}

#[derive(Debug, PartialEq, Eq, Hash)]
enum Cell {
    Empty,
    MirrorLU,  // /
    MirrorRU,  // \
    SplitterH, // -
    SplitterV, // |
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug, PartialEq, Eq, Hash)]
struct State {
    row_idx: isize,
    col_idx: isize,
    direction: Direction,
}

impl State {
    fn new(row_idx: isize, col_idx: isize, direction: Direction) -> State {
        State {
            row_idx,
            col_idx,
            direction,
        }
    }

    fn step(&self, direction: Direction) -> State {
        match direction {
            Direction::Up => State::new(self.row_idx - 1, self.col_idx, direction),
            Direction::Down => State::new(self.row_idx + 1, self.col_idx, direction),
            Direction::Left => State::new(self.row_idx, self.col_idx - 1, direction),
            Direction::Right => State::new(self.row_idx, self.col_idx + 1, direction),
        }
    }
}

fn count_energized_tiles(grid: &Vec<Vec<Cell>>, start: State) -> i64 {
    let mut visited = HashSet::new();
    let mut q = vec![start];
    while let Some(state) = q.pop() {
        if visited.contains(&state) {
            continue;
        }
        let cell = &grid[state.row_idx as usize][state.col_idx as usize];
        let mut next_states = match cell {
            Cell::Empty => {
                vec![state.step(state.direction.clone())]
            }
            Cell::MirrorLU => match state.direction {
                Direction::Up => vec![state.step(Direction::Right)],
                Direction::Down => vec![state.step(Direction::Left)],
                Direction::Left => vec![state.step(Direction::Down)],
                Direction::Right => vec![state.step(Direction::Up)],
            },
            Cell::MirrorRU => match state.direction {
                Direction::Up => vec![state.step(Direction::Left)],
                Direction::Down => vec![state.step(Direction::Right)],
                Direction::Left => vec![state.step(Direction::Up)],
                Direction::Right => vec![state.step(Direction::Down)],
            },
            Cell::SplitterH => match state.direction {
                Direction::Up | Direction::Down => {
                    vec![state.step(Direction::Left), state.step(Direction::Right)]
                }
                Direction::Left | Direction::Right => {
                    vec![state.step(state.direction.clone())]
                }
            },
            Cell::SplitterV => match state.direction {
                Direction::Up | Direction::Down => {
                    vec![state.step(state.direction.clone())]
                }
                Direction::Left | Direction::Right => {
                    vec![state.step(Direction::Up), state.step(Direction::Down)]
                }
            },
        };
        next_states.retain(|state| is_inside_grid(state, grid));
        q.extend(next_states);
        visited.insert(state);
    }
    visited
        .iter()
        .map(|state| (state.row_idx as usize, state.col_idx as usize))
        .unique()
        .count() as i64
}

fn is_inside_grid(state: &State, grid: &Vec<Vec<Cell>>) -> bool {
    state.row_idx >= 0
        && (state.row_idx as usize) < grid.len()
        && state.col_idx >= 0
        && (state.col_idx as usize) < grid[0].len()
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day16/sample");
        assert_eq!(part1(input_path).unwrap(), 46);

        let input_path = Path::new("./src/day16/input");
        assert_eq!(part1(input_path).unwrap(), 7870);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day16/sample");
        assert_eq!(part2(input_path).unwrap(), 51);

        let input_path = Path::new("./src/day16/input");
        assert_eq!(part2(input_path).unwrap(), 8143);
    }
}
