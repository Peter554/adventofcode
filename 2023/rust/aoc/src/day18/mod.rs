use anyhow::Result;
use itertools::Itertools;
use std::{fs, isize, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let instructions = parse_input(&input);
    let vertices = get_vertices(&instructions);
    let n_boundary_coordinates = get_n_boundary_coordinates(&vertices);
    let n_interior_coordinates = get_n_interior_coordinates(&vertices);
    Ok((n_boundary_coordinates + n_interior_coordinates) as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let instructions = parse_input_corrected(&input);
    let vertices = get_vertices(&instructions);
    let n_boundary_coordinates = get_n_boundary_coordinates(&vertices);
    let n_interior_coordinates = get_n_interior_coordinates(&vertices);
    Ok((n_boundary_coordinates + n_interior_coordinates) as i64)
}

fn parse_input(s: &str) -> Vec<Instruction> {
    s.lines()
        .map(|line| {
            let mut it = line.split_ascii_whitespace();
            Instruction {
                direction: match it.next().unwrap() {
                    "U" => Direction::Up,
                    "D" => Direction::Down,
                    "L" => Direction::Left,
                    "R" => Direction::Right,
                    _ => panic!(),
                },
                distance: it.next().unwrap().parse().unwrap(),
            }
        })
        .collect()
}

fn parse_input_corrected(s: &str) -> Vec<Instruction> {
    s.lines()
        .map(|line| {
            let mut it = line.split_ascii_whitespace();
            it.next();
            it.next();
            let s = it
                .next()
                .unwrap()
                .strip_prefix("(#")
                .unwrap()
                .strip_suffix(')')
                .unwrap();
            let direction = match s.chars().last().unwrap() {
                '0' => Direction::Right,
                '1' => Direction::Down,
                '2' => Direction::Left,
                '3' => Direction::Up,
                _ => panic!(),
            };
            let distance =
                isize::from_str_radix(&s.chars().take(5).collect::<String>(), 16).unwrap();
            Instruction {
                direction,
                distance,
            }
        })
        .collect()
}

fn get_vertices(instructions: &[Instruction]) -> Vec<(isize, isize)> {
    let mut coordinates: Vec<(isize, isize)> = vec![(0, 0)];
    for instruction in instructions {
        let delta = match instruction.direction {
            Direction::Up => (0, -instruction.distance),
            Direction::Down => (0, instruction.distance),
            Direction::Left => (-instruction.distance, 0),
            Direction::Right => (instruction.distance, 0),
        };
        let current_coordinate = coordinates.last().unwrap();
        coordinates.push((
            current_coordinate.0 + delta.0,
            current_coordinate.1 + delta.1,
        ));
    }
    // Remove the duplicate element.
    coordinates.pop();
    coordinates
}

fn get_n_boundary_coordinates(vertices: &[(isize, isize)]) -> isize {
    vertices
        .iter()
        .circular_tuple_windows::<(_, _)>()
        .map(|window| (window.1 .0 - window.0 .0).abs() + (window.1 .1 - window.0 .1).abs())
        .sum::<isize>()
}

fn get_n_interior_coordinates(vertices: &[(isize, isize)]) -> isize {
    // Shoelace formula.
    let area = vertices
        .iter()
        .circular_tuple_windows::<(_, _)>()
        .map(|window| window.0 .0 * window.1 .1 - window.1 .0 * window.0 .1)
        .sum::<isize>()
        / 2;

    // Picks theorem.
    let n_boundary_coordinates = get_n_boundary_coordinates(vertices);
    area + 1 - n_boundary_coordinates / 2
}

#[derive(Debug)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug)]
struct Instruction {
    direction: Direction,
    distance: isize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day18/sample");
        assert_eq!(part1(input_path).unwrap(), 62);

        let input_path = Path::new("./src/day18/input");
        assert_eq!(part1(input_path).unwrap(), 35991);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day18/sample");
        assert_eq!(part2(input_path).unwrap(), 952408144115);

        let input_path = Path::new("./src/day18/input");
        assert_eq!(part2(input_path).unwrap(), 54058824661845);
    }
}
