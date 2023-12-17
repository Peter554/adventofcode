use anyhow::Result;
use array2d::Array2D;
use std::{
    collections::{BinaryHeap, HashMap},
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let grid = parse_input(&input);

    let mut shortest_paths: HashMap<State, i64> = HashMap::new();
    let mut q = BinaryHeap::new();
    q.push((
        0,
        State {
            row_idx: 0,
            column_idx: 0,
            direction: Direction::Right,
            moves_forward: 0,
        },
    ));
    q.push((
        0,
        State {
            row_idx: 0,
            column_idx: 0,
            direction: Direction::Down,
            moves_forward: 0,
        },
    ));
    while let Some((cost, state)) = q.pop() {
        if shortest_paths.contains_key(&state) {
            continue;
        }
        let candidate_next_states = match state.direction {
            Direction::Up | Direction::Down => vec![
                state.go_forward(),
                state.go_in_direction(Direction::Left),
                state.go_in_direction(Direction::Right),
            ],
            Direction::Left | Direction::Right => vec![
                state.go_forward(),
                state.go_in_direction(Direction::Up),
                state.go_in_direction(Direction::Down),
            ],
        };
        for next_state in candidate_next_states
            .into_iter()
            .filter(|next_state| is_inside_grid(next_state, &grid))
            .filter(|next_state| next_state.moves_forward <= 3)
        {
            let next_state_cost =
                cost - grid[(next_state.row_idx as usize, next_state.column_idx as usize)];
            q.push((next_state_cost, next_state))
        }
        shortest_paths.insert(state, cost);
    }

    Ok(-shortest_paths
        .into_iter()
        .filter(|(state, _)| {
            state.row_idx as usize == grid.num_rows() - 1
                && state.column_idx as usize == grid.num_columns() - 1
        })
        .map(|(_, cost)| cost)
        .max()
        .unwrap())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let grid = parse_input(&input);

    let mut shortest_paths: HashMap<State, i64> = HashMap::new();
    let mut q = BinaryHeap::new();
    q.push((
        0,
        State {
            row_idx: 0,
            column_idx: 0,
            direction: Direction::Right,
            moves_forward: 0,
        },
    ));
    q.push((
        0,
        State {
            row_idx: 0,
            column_idx: 0,
            direction: Direction::Down,
            moves_forward: 0,
        },
    ));
    while let Some((cost, state)) = q.pop() {
        if shortest_paths.contains_key(&state) {
            continue;
        }
        let candidate_next_states = match state.direction {
            Direction::Up | Direction::Down => vec![
                state.go_forward(),
                state.go_in_direction(Direction::Left),
                state.go_in_direction(Direction::Right),
            ],
            Direction::Left | Direction::Right => vec![
                state.go_forward(),
                state.go_in_direction(Direction::Up),
                state.go_in_direction(Direction::Down),
            ],
        };
        for next_state in candidate_next_states
            .into_iter()
            .filter(|next_state| is_inside_grid(next_state, &grid))
            .filter(|next_state| {
                let changed_direction = next_state.direction != state.direction;
                if changed_direction {
                    state.moves_forward >= 4
                } else {
                    next_state.moves_forward <= 10
                }
            })
        {
            let next_state_cost =
                cost - grid[(next_state.row_idx as usize, next_state.column_idx as usize)];
            q.push((next_state_cost, next_state))
        }
        shortest_paths.insert(state, cost);
    }

    Ok(-shortest_paths
        .into_iter()
        .filter(|(state, _)| {
            state.row_idx as usize == grid.num_rows() - 1
                && state.column_idx as usize == grid.num_columns() - 1
        })
        .filter(|(state, _)| state.moves_forward >= 4)
        .map(|(_, cost)| cost)
        .max()
        .unwrap())
}

fn parse_input(input: &str) -> Array2D<i64> {
    let data = input
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| c.to_digit(10).unwrap() as i64)
                .collect()
        })
        .collect::<Vec<_>>();
    Array2D::from_rows(&data).unwrap()
}

#[derive(Debug, PartialEq, Eq, Clone, Hash, PartialOrd, Ord)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug, PartialEq, Eq, Clone, Hash, PartialOrd, Ord)]
struct State {
    row_idx: isize,
    column_idx: isize,
    direction: Direction,
    moves_forward: u8,
}

impl State {
    fn new(row_idx: isize, column_idx: isize, direction: Direction, moves_forward: u8) -> State {
        State {
            row_idx,
            column_idx,
            direction,
            moves_forward,
        }
    }

    fn go_in_direction(&self, direction: Direction) -> State {
        let moves_forward = if direction == self.direction {
            self.moves_forward + 1
        } else {
            1
        };
        match direction {
            Direction::Up => {
                State::new(self.row_idx - 1, self.column_idx, direction, moves_forward)
            }
            Direction::Down => {
                State::new(self.row_idx + 1, self.column_idx, direction, moves_forward)
            }
            Direction::Left => {
                State::new(self.row_idx, self.column_idx - 1, direction, moves_forward)
            }
            Direction::Right => {
                State::new(self.row_idx, self.column_idx + 1, direction, moves_forward)
            }
        }
    }

    fn go_forward(&self) -> State {
        self.go_in_direction(self.direction.clone())
    }
}

fn is_inside_grid(state: &State, grid: &Array2D<i64>) -> bool {
    state.row_idx >= 0
        && (state.row_idx as usize) < grid.num_rows()
        && state.column_idx >= 0
        && (state.column_idx as usize) < grid.num_columns()
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day17/sample");
        assert_eq!(part1(input_path).unwrap(), 102);

        let input_path = Path::new("./src/day17/input");
        assert_eq!(part1(input_path).unwrap(), 755);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day17/sample");
        assert_eq!(part2(input_path).unwrap(), 94);

        let input_path = Path::new("./src/day17/sample2");
        assert_eq!(part2(input_path).unwrap(), 71);

        let input_path = Path::new("./src/day17/input");
        assert_eq!(part2(input_path).unwrap(), 881);
    }
}
