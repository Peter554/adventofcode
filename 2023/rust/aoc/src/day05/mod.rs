use anyhow::Result;
use std::{fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);
    Ok(input
        .seeds
        .into_iter()
        .map(|seed| input.maps.iter().fold(seed, |value, map| map.apply(value)))
        .min()
        .unwrap() as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let input = {
        let mut input = parse_input(&input);
        input.seeds = input
            .seeds
            .as_slice()
            .windows(2)
            .step_by(2)
            .flat_map(|window| (window[0]..window[0] + window[1]))
            .collect();
        input
    };
    Ok(input
        .seeds
        .into_iter()
        .map(|seed| input.maps.iter().fold(seed, |value, map| map.apply(value)))
        .min()
        .unwrap() as i64)
}

fn parse_input(input: &str) -> Input {
    let mut it = input.split("\n\n");
    let seeds = it
        .next()
        .unwrap()
        .strip_prefix("seeds: ")
        .unwrap()
        .split_ascii_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();
    let maps = it
        .map(|s| {
            let rules = s
                .lines()
                .skip(1)
                .map(|line| {
                    let line = line
                        .split_ascii_whitespace()
                        .map(|s| s.parse().unwrap())
                        .collect::<Vec<u64>>();
                    MapRule {
                        source_range_start: line[1],
                        destination_range_start: line[0],
                        range_size: line[2],
                    }
                })
                .collect::<Vec<_>>();
            Map { rules }
        })
        .collect();
    Input { seeds, maps }
}

#[derive(Debug)]
struct Input {
    seeds: Vec<u64>,
    maps: Vec<Map>,
}

#[derive(Debug)]
struct Map {
    rules: Vec<MapRule>,
}

#[derive(Debug)]
struct MapRule {
    source_range_start: u64,
    destination_range_start: u64,
    range_size: u64,
}

impl Map {
    fn apply(&self, value: u64) -> u64 {
        for rule in self.rules.iter() {
            if value >= rule.source_range_start && value < rule.source_range_start + rule.range_size
            {
                return rule.destination_range_start + (value - rule.source_range_start);
            }
        }
        value
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part_1() {
        let input_path = Path::new("./src/day05/sample");
        assert_eq!(part1(input_path).unwrap(), 35);

        let input_path = Path::new("./src/day05/input");
        assert_eq!(part1(input_path).unwrap(), 535088217);
    }

    #[test]
    fn test_part_2_sample() {
        let input_path = Path::new("./src/day05/sample");
        assert_eq!(part2(input_path).unwrap(), 46);
    }

    #[test]
    #[cfg_attr(not(feature = "slow"), ignore = "slow")]
    fn test_part_2_real() {
        let input_path = Path::new("./src/day05/input");
        assert_eq!(part2(input_path).unwrap(), 51399228);
    }
}
