use std::{fs, str::FromStr};

pub fn part1(input_path: &str) -> u32 {
    fs::read_to_string(input_path)
        .unwrap()
        .lines()
        .map(|line| line.parse::<Present>())
        .try_fold(0, |sum, present| {
            present.map(|p| sum + p.surface_area() + p.smallest_side_area())
        })
        .unwrap()
}

pub fn part2(input_path: &str) -> u32 {
    fs::read_to_string(input_path)
        .unwrap()
        .lines()
        .map(|line| line.parse::<Present>())
        .try_fold(0, |sum, present| {
            present.map(|p| sum + p.volume() + p.shortest_perimeter())
        })
        .unwrap()
}

struct Present(u32, u32, u32);

impl FromStr for Present {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let dimensions: Result<Vec<_>, _> = s.split('x').map(|s| s.parse::<u32>()).collect();
        match dimensions {
            Ok(mut dimensions) => {
                dimensions.sort();
                match dimensions.len() {
                    3 => Ok(Present(dimensions[0], dimensions[1], dimensions[2])),
                    _ => Err(String::from("Could not parse")),
                }
            }
            Err(_) => Err(String::from("Could not parse")),
        }
    }
}

impl Present {
    fn surface_area(&self) -> u32 {
        (2 * self.0 * self.1) + (2 * self.0 * self.2) + (2 * self.1 * self.2)
    }

    fn smallest_side_area(&self) -> u32 {
        self.0 * self.1
    }

    fn volume(&self) -> u32 {
        self.0 * self.1 * self.2
    }

    fn shortest_perimeter(&self) -> u32 {
        2 * (self.0 + self.1)
    }
}
