use anyhow::Result;
use std::{fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let patterns = parse_input(&input);
    Ok(patterns
        .into_iter()
        .map(find_symmetry)
        .map(|symmetry| match symmetry {
            Symmetry::Row(row_idx) => 100 * (row_idx + 1) as i64,
            Symmetry::Column(column_idx) => (column_idx + 1) as i64,
        })
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let _ = input;
    Ok(42)
}

fn parse_input(input: &str) -> Vec<Vec<Vec<bool>>> {
    input
        .split("\n\n")
        .map(|s| {
            s.lines()
                .map(|line| line.chars().map(|c| c == '#').collect())
                .collect()
        })
        .collect()
}

enum Symmetry {
    Row(usize),
    Column(usize),
}

fn find_symmetry(pattern: Vec<Vec<bool>>) -> Symmetry {
    for row_idx in 0..=pattern.len() - 2 {
        if is_symmetric_about_row(&pattern, row_idx) {
            return Symmetry::Row(row_idx);
        }
    }
    let transposed_pattern = transpose(&pattern);
    for row_idx in 0..=transposed_pattern.len() - 2 {
        if is_symmetric_about_row(&transposed_pattern, row_idx) {
            return Symmetry::Column(row_idx);
        }
    }
    panic!()
}

fn is_symmetric_about_row(pattern: &[Vec<bool>], row_idx: usize) -> bool {
    for idx in 0..=row_idx {
        let reflected_idx = (row_idx + 1) + (row_idx - idx);
        if reflected_idx > pattern.len() - 1 {
            continue;
        }
        if pattern[idx] != pattern[reflected_idx] {
            return false;
        }
    }
    true
}

fn transpose(pattern: &[Vec<bool>]) -> Vec<Vec<bool>> {
    let mut out = vec![vec![false; pattern.len()]; pattern[0].len()];
    for (row_idx, row) in pattern.iter().enumerate() {
        for (col_idx, value) in row.iter().enumerate() {
            out[col_idx][row_idx] = *value;
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day13/sample");
        assert_eq!(part1(input_path).unwrap(), 405);

        let input_path = Path::new("./src/day13/input");
        assert_eq!(part1(input_path).unwrap(), 35538);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day13/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day13/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
