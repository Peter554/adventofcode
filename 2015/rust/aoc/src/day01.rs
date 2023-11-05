use std::fs;

pub fn part1(input_path: &str) -> i32 {
    fs::read_to_string(input_path)
        .unwrap()
        .chars()
        .fold(0, |floor, c| match c {
            '(' => floor + 1,
            ')' => floor - 1,
            _ => floor,
        })
}

pub fn part2(input_path: &str) -> u32 {
    fs::read_to_string(input_path)
        .unwrap()
        .chars()
        .scan(State::new(), |state, c| {
            match c {
                '(' => state.up(),
                ')' => state.down(),
                _ => {}
            }
            Some(*state)
        })
        .find(|state| state.floor < 0)
        .unwrap()
        .position
}

#[derive(Clone, Copy)]
struct State {
    position: u32,
    floor: i32,
}

impl State {
    fn new() -> Self {
        State {
            position: 0,
            floor: 0,
        }
    }

    fn up(&mut self) {
        self.position += 1;
        self.floor += 1;
    }

    fn down(&mut self) {
        self.position += 1;
        self.floor -= 1;
    }
}
