use anyhow::Result;
use maplit::hashset;
use std::{
    collections::{HashMap, HashSet},
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);
    for s_connections in [
        hashset! {Connection::North, Connection::East},
        hashset! {Connection::North, Connection::West},
        hashset! {Connection::South, Connection::West},
        hashset! {Connection::South, Connection::East},
    ] {
        match find_loop(&input.s_location, &s_connections, &input.pipes) {
            Some(path) => return Ok(path.len() as i64 / 2),
            None => continue,
        }
    }
    panic!()
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let _ = input;
    Ok(42)
}

fn find_loop(
    start_point: &Point,
    start_connections: &HashSet<Connection>,
    pipes: &HashMap<Point, HashSet<Connection>>,
) -> Option<Vec<Point>> {
    let mut pipes = pipes.clone();
    *pipes.get_mut(start_point).unwrap() = start_connections.clone();

    let mut current_point = start_point.clone();
    let mut path = vec![];
    let mut visited = HashSet::new();
    loop {
        path.push(current_point.clone());
        visited.insert(current_point.clone());
        let neighbors = get_neighbors(&current_point, &pipes);
        if neighbors.len() != 2 {
            return None;
        }
        let unvisited_neighbors = neighbors.difference(&visited).cloned().collect::<Vec<_>>();
        if unvisited_neighbors.is_empty() {
            return Some(path);
        } else {
            current_point = unvisited_neighbors[0].clone();
        }
    }
}

fn get_neighbors(point: &Point, pipes: &HashMap<Point, HashSet<Connection>>) -> HashSet<Point> {
    pipes
        .get(point)
        .unwrap()
        .iter()
        .filter_map(|connection| match connection {
            Connection::North => {
                let candidate = point.north();
                let candidate_connections = pipes.get(&candidate);
                if candidate_connections.is_some()
                    && candidate_connections.unwrap().contains(&Connection::South)
                {
                    Some(candidate)
                } else {
                    None
                }
            }
            Connection::East => {
                let candidate = point.east();
                let candidate_connections = pipes.get(&candidate);
                if candidate_connections.is_some()
                    && candidate_connections.unwrap().contains(&Connection::West)
                {
                    Some(candidate)
                } else {
                    None
                }
            }
            Connection::South => {
                let candidate = point.south();
                let candidate_connections = pipes.get(&candidate);
                if candidate_connections.is_some()
                    && candidate_connections.unwrap().contains(&Connection::North)
                {
                    Some(candidate)
                } else {
                    None
                }
            }
            Connection::West => {
                let candidate = point.west();
                let candidate_connections = pipes.get(&candidate);
                if candidate_connections.is_some()
                    && candidate_connections.unwrap().contains(&Connection::East)
                {
                    Some(candidate)
                } else {
                    None
                }
            }
        })
        .collect()
}

fn parse_input(input: &str) -> Input {
    let mut s_location = None;
    let mut pipes = HashMap::new();
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let point = Point {
                x: x as i16,
                y: y as i16,
            };
            match c {
                '|' => {
                    pipes.insert(
                        point,
                        hashset! {
                            Connection::North,
                            Connection::South,
                        },
                    );
                }
                '-' => {
                    pipes.insert(
                        point,
                        hashset! {
                            Connection::West,
                            Connection::East,
                        },
                    );
                }
                'L' => {
                    pipes.insert(
                        point,
                        hashset! {
                            Connection::North,
                            Connection::East,
                        },
                    );
                }
                'J' => {
                    pipes.insert(
                        point,
                        hashset! {
                            Connection::North,
                            Connection::West,
                        },
                    );
                }
                '7' => {
                    pipes.insert(
                        point,
                        hashset! {
                            Connection::South,
                            Connection::West,
                        },
                    );
                }
                'F' => {
                    pipes.insert(
                        point,
                        hashset! {
                            Connection::South,
                            Connection::East,
                        },
                    );
                }
                'S' => {
                    pipes.insert(point.clone(), hashset! {});
                    s_location = Some(point);
                }
                '.' => {}
                _ => panic!(),
            }
        }
    }
    Input {
        s_location: s_location.unwrap(),
        pipes,
    }
}

struct Input {
    s_location: Point,
    pipes: HashMap<Point, HashSet<Connection>>,
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
struct Point {
    x: i16,
    y: i16,
}

impl Point {
    fn north(&self) -> Point {
        Point {
            x: self.x,
            y: self.y - 1,
        }
    }

    fn east(&self) -> Point {
        Point {
            x: self.x + 1,
            y: self.y,
        }
    }

    fn south(&self) -> Point {
        Point {
            x: self.x,
            y: self.y + 1,
        }
    }

    fn west(&self) -> Point {
        Point {
            x: self.x - 1,
            y: self.y,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
enum Connection {
    North,
    East,
    South,
    West,
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day10/sample");
        assert_eq!(part1(input_path).unwrap(), 8);

        let input_path = Path::new("./src/day10/input");
        assert_eq!(part1(input_path).unwrap(), 6806);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day10/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day10/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
