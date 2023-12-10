use anyhow::Result;
use maplit::hashset;
use std::{
    collections::{HashMap, HashSet, VecDeque},
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);
    let (loop_path, _) = find_loop(&input.s_location, &input.pipes);
    Ok(loop_path.len() as i64 / 2)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);
    let (loop_path, pipes) = find_loop(&input.s_location, &input.pipes);
    Ok(count_interior_points(loop_path, pipes))
}

fn find_loop(
    start_point: &Point,
    pipes: &HashMap<Point, HashSet<Connection>>,
) -> (Vec<Point>, HashMap<Point, HashSet<Connection>>) {
    let original_pipes = pipes;
    for start_connections in [
        hashset! {Connection::North, Connection::East},
        hashset! {Connection::North, Connection::West},
        hashset! {Connection::South, Connection::West},
        hashset! {Connection::South, Connection::East},
    ] {
        let mut pipes = original_pipes.clone();
        *pipes.get_mut(start_point).unwrap() = start_connections;

        let mut current_point = start_point.clone();
        let mut path = vec![];
        let mut visited = HashSet::new();
        loop {
            path.push(current_point.clone());
            visited.insert(current_point.clone());
            let neighbors = get_neighbors(&current_point, &pipes);
            if neighbors.len() != 2 {
                break;
            }
            let unvisited_neighbors = neighbors.difference(&visited).cloned().collect::<Vec<_>>();
            if unvisited_neighbors.is_empty() {
                return (path, pipes);
            } else {
                current_point = unvisited_neighbors[0].clone();
            }
        }
    }
    panic!()
}

fn get_neighbors(point: &Point, pipes: &HashMap<Point, HashSet<Connection>>) -> HashSet<Point> {
    pipes
        .get(point)
        .unwrap()
        .iter()
        .filter_map(|connection| match connection {
            Connection::North => {
                let candidate = Point::new(point.x, point.y - 1);
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
                let candidate = Point::new(point.x + 1, point.y);
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
                let candidate = Point::new(point.x, point.y + 1);
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
                let candidate = Point::new(point.x - 1, point.y);
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

fn count_interior_points(loop_path: Vec<Point>, pipes: HashMap<Point, HashSet<Connection>>) -> i64 {
    // Approach:
    // * create a set of all points in the space.
    // * blow up the space by a factor of 2, including the loop.
    // * find all the exterior points.
    // * count all interior points where x and y are even.
    let bounding_box = get_bounding_box(&loop_path);
    let mut grid = HashSet::new();
    for x in 2 * bounding_box.x_min - 1..=2 * bounding_box.x_max + 1 {
        for y in 2 * bounding_box.y_min - 1..=2 * bounding_box.y_max + 1 {
            grid.insert(Point::new(x, y));
        }
    }
    let mut loop_ = HashSet::new();
    for loop_point in loop_path {
        loop_.insert(Point::new(2 * loop_point.x, 2 * loop_point.y));
        let connections = pipes.get(&loop_point).unwrap();
        if connections.contains(&Connection::North) {
            loop_.insert(Point::new(2 * loop_point.x, 2 * loop_point.y - 1));
        }
        if connections.contains(&Connection::East) {
            loop_.insert(Point::new(2 * loop_point.x + 1, 2 * loop_point.y));
        }
        if connections.contains(&Connection::South) {
            loop_.insert(Point::new(2 * loop_point.x, 2 * loop_point.y + 1));
        }
        if connections.contains(&Connection::West) {
            loop_.insert(Point::new(2 * loop_point.x - 1, 2 * loop_point.y));
        }
    }

    let mut exterior_points = HashSet::new();
    let mut q = VecDeque::new();
    // We can be sure that top_left is exterior.
    let top_left = Point::new(2 * bounding_box.x_min - 1, 2 * bounding_box.y_min - 1);
    q.push_back(top_left);
    while let Some(p) = q.pop_front() {
        if exterior_points.contains(&p) {
            continue;
        } else {
            exterior_points.insert(p.clone());
        }
        for neighbor in [
            Point::new(p.x - 1, p.y),
            Point::new(p.x + 1, p.y),
            Point::new(p.x, p.y - 1),
            Point::new(p.x, p.y + 1),
            Point::new(p.x - 1, p.y - 1),
            Point::new(p.x + 1, p.y - 1),
            Point::new(p.x - 1, p.y + 1),
            Point::new(p.x + 1, p.y + 1),
        ] {
            if !grid.contains(&neighbor) {
                continue;
            }
            if loop_.contains(&neighbor) {
                continue;
            }
            q.push_back(neighbor);
        }
    }

    grid.into_iter()
        .filter(|p| !loop_.contains(p))
        .filter(|p| !exterior_points.contains(p))
        .filter(|p| p.x % 2 == 0 && p.y % 2 == 0)
        .count() as i64
}

struct BoundingBox {
    x_min: i16,
    x_max: i16,
    y_min: i16,
    y_max: i16,
}

fn get_bounding_box(points: &[Point]) -> BoundingBox {
    BoundingBox {
        x_min: points.iter().map(|p| p.x).min().unwrap(),
        x_max: points.iter().map(|p| p.x).max().unwrap(),
        y_min: points.iter().map(|p| p.y).min().unwrap(),
        y_max: points.iter().map(|p| p.y).max().unwrap(),
    }
}

fn parse_input(input: &str) -> Input {
    let mut s_location = None;
    let mut pipes = HashMap::new();
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let point = Point::new(x as i16, y as i16);
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
    fn new(x: i16, y: i16) -> Point {
        Point { x, y }
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
        let input_path = Path::new("./src/day10/sample2");
        assert_eq!(part2(input_path).unwrap(), 10);

        let input_path = Path::new("./src/day10/input");
        assert_eq!(part2(input_path).unwrap(), 449);
    }
}
