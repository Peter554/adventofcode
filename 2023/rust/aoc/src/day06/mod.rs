use anyhow::Result;
use std::collections::HashMap;

pub fn part1(input: HashMap<u64, u64>) -> Result<i64> {
    Ok(input
        .into_iter()
        .map(|(time, record)| {
            (0..=time)
                .filter(|wait_time| (time - wait_time) * wait_time > record)
                .count() as i64
        })
        .product())
}

pub fn part2(input: HashMap<u64, u64>) -> Result<i64> {
    // Too lazy, it works.
    part1(input)
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use super::*;
    use maplit::hashmap;
    use pretty_assertions::assert_eq;

    fn sample() -> HashMap<u64, u64> {
        hashmap! {
            7 => 9,
            15 => 40,
            30 => 200
        }
    }

    fn input() -> HashMap<u64, u64> {
        hashmap! {
            54 => 239,
            70 => 1142,
            82 => 1295,
            75 => 1253,
        }
    }

    fn sample2() -> HashMap<u64, u64> {
        hashmap! {
            71530 => 940200,
        }
    }

    fn input2() -> HashMap<u64, u64> {
        hashmap! {
            54708275 => 239114212951253,
        }
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(sample()).unwrap(), 288);
        assert_eq!(part1(input()).unwrap(), 800280);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(sample2()).unwrap(), 71503);
        assert_eq!(part2(input2()).unwrap(), 45128024);
    }
}
