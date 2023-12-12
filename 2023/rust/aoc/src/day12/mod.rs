use anyhow::Result;
use std::{collections::HashMap, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<u64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);
    Ok(input
        .into_iter()
        .map(|(states, constraints)| {
            combination_counter::CombinationCounter::new()
                .count_possible_combinations(&states, &constraints)
        })
        .sum())
}

pub fn part2(input_path: &Path) -> Result<u64> {
    let input = fs::read_to_string(input_path)?;
    let input = parse_input(&input);
    Ok(input
        .into_iter()
        .map(unfold_input)
        .map(|(states, constraints)| {
            combination_counter::CombinationCounter::new()
                .count_possible_combinations(&states, &constraints)
        })
        .sum())
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub enum State {
    On,
    Off,
    Unknown,
}

fn parse_input(input: &str) -> Vec<(Vec<State>, Vec<usize>)> {
    input
        .lines()
        .map(|line| {
            let mut it = line.split_ascii_whitespace();
            let states = parse_states(it.next().unwrap());
            let constraints = parse_constraints(it.next().unwrap());
            (states, constraints)
        })
        .collect()
}

fn parse_states(s: &str) -> Vec<State> {
    s.chars()
        .map(|c| match c {
            '#' => State::On,
            '.' => State::Off,
            '?' => State::Unknown,
            _ => panic!(),
        })
        .collect::<Vec<_>>()
}

fn parse_constraints(s: &str) -> Vec<usize> {
    s.split(',')
        .map(|s| s.parse::<usize>().unwrap())
        .collect::<Vec<_>>()
}

fn unfold_input(input: (Vec<State>, Vec<usize>)) -> (Vec<State>, Vec<usize>) {
    let mut states = vec![];
    let mut constaints = vec![];
    for i in 0..5 {
        states.extend(input.0.clone());
        constaints.extend(input.1.clone());
        if i < 4 {
            states.push(State::Unknown);
        }
    }
    (states, constaints)
}

mod combination_counter {
    use super::*;

    #[derive(Debug, PartialEq, Eq, Hash)]
    struct CacheKey<'a> {
        states: &'a [State],
        constraints: &'a [usize],
    }

    pub struct CombinationCounter<'a> {
        cache: HashMap<CacheKey<'a>, u64>,
    }

    impl<'a> CombinationCounter<'a> {
        pub fn new() -> Self {
            CombinationCounter {
                cache: HashMap::new(),
            }
        }

        pub fn count_possible_combinations(
            &mut self,
            states: &'a [State],
            constraints: &'a [usize],
        ) -> u64 {
            let cache_key = CacheKey {
                states,
                constraints,
            };
            if let Some(out) = self.cache.get(&cache_key) {
                return *out;
            }
            let out = self.count_possible_combinations_inner(states, constraints);
            self.cache.insert(cache_key, out);
            out
        }

        fn count_possible_combinations_inner(
            &mut self,
            states: &'a [State],
            constraints: &'a [usize],
        ) -> u64 {
            if states.is_empty() {
                if constraints.is_empty() {
                    return 1;
                } else {
                    return 0;
                }
            }
            if constraints.is_empty() {
                if states
                    .iter()
                    .all(|state| matches!(state, State::Off | State::Unknown))
                {
                    return 1;
                } else {
                    return 0;
                }
            }

            if matches!(states[0], State::Unknown | State::On) {
                let mut total_combinations = 0;

                // Check if we could consume a constraint, if so add this possibility.
                let could_consume_constraint = 'block: {
                    let constraint = constraints[0];
                    let middle_ok = constraint <= states.len()
                        && states[..constraint]
                            .iter()
                            .all(|state| matches!(state, State::On | State::Unknown));
                    if !middle_ok {
                        break 'block false;
                    }
                    let right_ok = constraint == states.len()
                        || matches!(states[constraint], State::Off | State::Unknown);
                    if !right_ok {
                        break 'block false;
                    }
                    true
                };
                if could_consume_constraint {
                    let constraint = constraints[0];
                    total_combinations += self.count_possible_combinations(
                        &states[std::cmp::min(constraint + 1, states.len())..],
                        &constraints[1..],
                    );
                }

                // Check if we could not consume a constraint, if so add this possibility.
                let must_consume_constraint = matches!(states[0], State::On);
                if !must_consume_constraint {
                    total_combinations +=
                        self.count_possible_combinations(&states[1..], constraints);
                }

                total_combinations
            } else {
                self.count_possible_combinations(&states[1..], constraints)
            }
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day12/sample");
        assert_eq!(part1(input_path).unwrap(), 21);

        let input_path = Path::new("./src/day12/input");
        assert_eq!(part1(input_path).unwrap(), 7633);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day12/sample");
        assert_eq!(part2(input_path).unwrap(), 525152);

        let input_path = Path::new("./src/day12/input");
        assert_eq!(part2(input_path).unwrap(), 23903579139437);
    }
}
