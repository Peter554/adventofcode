use anyhow::Result;
use std::{cmp, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);
    let seed_to_location = |seed| input.maps.iter().fold(seed, |value, map| map.apply(value));
    Ok(input.seeds.into_iter().map(seed_to_location).min().unwrap())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);

    let mut ranges = input
        .seeds
        .as_slice()
        .windows(2)
        .step_by(2)
        .map(|window| (window[0], (window[0] + window[1] - 1)))
        .collect::<Vec<_>>();

    for map in input.maps.iter() {
        ranges = apply_map(ranges, map);
    }

    Ok(ranges.iter().map(|(start, _)| *start).min().unwrap())
}

fn apply_map(ranges: Vec<(i64, i64)>, map: &Map) -> Vec<(i64, i64)> {
    let mut out_ranges = vec![];
    for range in ranges {
        out_ranges.extend(apply_map_to_single_range(range, map));
    }
    out_ranges
}

fn apply_map_to_single_range(range: (i64, i64), map: &Map) -> Vec<(i64, i64)> {
    let mut out_ranges = vec![];
    let mut unmapped_ranges = vec![range];
    for rule in map.rules.iter() {
        let mut next_unmapped_ranges = vec![];
        while let Some((range_start, range_end)) = unmapped_ranges.pop() {
            if range_start > rule.range_end || range_end < rule.range_start {
                // No overlap.
                next_unmapped_ranges.push((range_start, range_end));
            } else {
                // Overlap.
                out_ranges.push((
                    cmp::max(range_start, rule.range_start) + rule.delta,
                    cmp::min(range_end, rule.range_end) + rule.delta,
                ));
                if range_start < rule.range_start {
                    next_unmapped_ranges.push((range_start, rule.range_start - 1));
                }
                if range_end > rule.range_end {
                    next_unmapped_ranges.push((rule.range_end + 1, range_end));
                }
            }
        }
        unmapped_ranges = next_unmapped_ranges;
    }
    out_ranges.extend(unmapped_ranges);
    out_ranges
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
                        .collect::<Vec<i64>>();
                    MapRule {
                        range_start: line[1],
                        range_end: line[1] + line[2] - 1,
                        delta: line[0] - line[1],
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
    seeds: Vec<i64>,
    maps: Vec<Map>,
}

#[derive(Debug)]
struct Map {
    rules: Vec<MapRule>,
}

#[derive(Debug)]
struct MapRule {
    range_start: i64,
    range_end: i64,
    delta: i64,
}

impl Map {
    fn apply(&self, value: i64) -> i64 {
        for rule in self.rules.iter() {
            if value >= rule.range_start && value <= rule.range_end {
                return value + rule.delta;
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
    fn test_part1() {
        let input_path = Path::new("./src/day05/sample");
        assert_eq!(part1(input_path).unwrap(), 35);

        let input_path = Path::new("./src/day05/input");
        assert_eq!(part1(input_path).unwrap(), 535088217);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day05/sample");
        assert_eq!(part2(input_path).unwrap(), 46);
        let input_path = Path::new("./src/day05/input");
        assert_eq!(part2(input_path).unwrap(), 51399228);
    }
}
