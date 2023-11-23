use anyhow::Result;
use std::{fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    _ = fs::read_to_string(input_path)?;
    Ok(42)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    _ = fs::read_to_string(input_path)?;
    Ok(42)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let input_path = Path::new("./src/day01/sample");
        assert_eq!(part1(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day01/input");
        assert_eq!(part1(input_path).unwrap(), 42);
    }

    #[test]
    fn test_part_2() {
        let input_path = Path::new("./src/day01/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day01/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
