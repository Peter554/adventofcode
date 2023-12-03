mod parser;

use anyhow::Result;
use std::{cmp, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let games = parser::parse(&input)?;
    Ok(games
        .iter()
        .filter(|g| {
            g.hands
                .iter()
                .all(|h| h.red <= 12 && h.green <= 13 && h.blue <= 14)
        })
        .map(|g| g.id as i64)
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let games = parser::parse(&input)?;
    Ok(games
        .iter()
        .map(|g| {
            g.hands
                .iter()
                .fold((0, 0, 0), |(mut red, mut green, mut blue), hand| {
                    red = cmp::max(red, hand.red);
                    green = cmp::max(green, hand.green);
                    blue = cmp::max(blue, hand.blue);
                    (red, green, blue)
                })
        })
        .map(|(red, green, blue)| (red as i64, green as i64, blue as i64))
        .map(|(red, green, blue)| red * green * blue)
        .sum())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input_path = Path::new("./src/day02/sample");
        assert_eq!(part1(input_path).unwrap(), 8);

        let input_path = Path::new("./src/day02/input");
        assert_eq!(part1(input_path).unwrap(), 2149);
    }

    #[test]
    fn test_part_2() {
        let input_path = Path::new("./src/day02/sample");
        assert_eq!(part2(input_path).unwrap(), 2286);

        let input_path = Path::new("./src/day02/input");
        assert_eq!(part2(input_path).unwrap(), 71274);
    }
}
