use std::{fs, iter};

use itertools::Itertools;

pub fn part1(input_path: &str) -> usize {
    get_route(fs::read_to_string(input_path).unwrap().chars())
        .unique()
        .count()
}

pub fn part2(input_path: &str) -> usize {
    get_route(fs::read_to_string(input_path).unwrap().chars().step_by(2))
        .chain(get_route(
            fs::read_to_string(input_path)
                .unwrap()
                .chars()
                .skip(1)
                .step_by(2),
        ))
        .unique()
        .count()
}

fn get_route(instructions: impl IntoIterator<Item = char>) -> impl Iterator<Item = (i32, i32)> {
    iter::once((0, 0)).chain(instructions.into_iter().scan((0, 0), |(x, y), c| {
        match c {
            '^' => *y += 1,
            '>' => *x += 1,
            'v' => *y -= 1,
            '<' => *x -= 1,
            _ => {}
        }
        Some((*x, *y))
    }))
}
