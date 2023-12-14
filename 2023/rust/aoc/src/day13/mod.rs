use anyhow::Result;
use std::{collections::HashMap, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let patterns = parse_input(&input);
    Ok(patterns
        .into_iter()
        .map(get_reflection_error_counts)
        .map(|hm| hm.get(&0).unwrap()[0].clone())
        .map(|reflection_axis| match reflection_axis {
            ReflectionAxis::Row(row_idx) => 100 * (row_idx + 1) as i64,
            ReflectionAxis::Column(column_idx) => (column_idx + 1) as i64,
        })
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let patterns = parse_input(&input);
    Ok(patterns
        .into_iter()
        .map(get_reflection_error_counts)
        .map(|hm| hm.get(&1).unwrap()[0].clone())
        .map(|reflection_axis| match reflection_axis {
            ReflectionAxis::Row(row_idx) => 100 * (row_idx + 1) as i64,
            ReflectionAxis::Column(column_idx) => (column_idx + 1) as i64,
        })
        .sum())
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

#[derive(Debug, Clone)]
enum ReflectionAxis {
    Row(usize),
    Column(usize),
}

// For every reflection axis compute the reflection error count
// (number of errors we see when reflecting about that axis).
// Return a mapping of error count to reflection axes with that error count.
fn get_reflection_error_counts(pattern: Vec<Vec<bool>>) -> HashMap<i64, Vec<ReflectionAxis>> {
    let mut out: HashMap<i64, Vec<ReflectionAxis>> = HashMap::new();
    for row_idx in 0..=pattern.len() - 2 {
        let error_count = get_reflection_error_count_about_row(&pattern, row_idx);
        out.entry(error_count)
            .or_default()
            .push(ReflectionAxis::Row(row_idx));
    }
    let transposed_pattern = transpose(&pattern);
    for row_idx in 0..=transposed_pattern.len() - 2 {
        let error_count = get_reflection_error_count_about_row(&transposed_pattern, row_idx);
        out.entry(error_count)
            .or_default()
            .push(ReflectionAxis::Column(row_idx));
    }
    out
}

fn get_reflection_error_count_about_row(pattern: &[Vec<bool>], row_idx: usize) -> i64 {
    let mut out = 0;
    for idx in 0..=row_idx {
        let reflected_idx = (row_idx + 1) + (row_idx - idx);
        if reflected_idx > pattern.len() - 1 {
            continue;
        }
        out += pattern[idx]
            .iter()
            .zip(pattern[reflected_idx].iter())
            .map(|(a, b)| if a == b { 0 } else { 1 })
            .sum::<i64>()
    }
    out
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
        assert_eq!(part2(input_path).unwrap(), 400);

        let input_path = Path::new("./src/day13/input");
        assert_eq!(part2(input_path).unwrap(), 30442);
    }
}
