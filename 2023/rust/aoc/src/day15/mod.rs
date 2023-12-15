use anyhow::Result;
use indexmap::IndexMap;
use std::{fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let mut total_hash = 0i64;
    for s in input.split(',') {
        total_hash += hash(s) as i64;
    }
    Ok(total_hash)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;

    let lens_ops = parse_lens_ops(&input);
    let mut boxes = IndexMap::new();
    for lens_op in lens_ops {
        match lens_op {
            LensOp::Add {
                label,
                focal_length,
            } => {
                let lenses = boxes.entry(hash(&label)).or_insert(IndexMap::new());
                *lenses.entry(label).or_insert(focal_length) = focal_length;
            }
            LensOp::Remove { label } => {
                let lenses = boxes.entry(hash(&label)).or_insert(IndexMap::new());
                lenses.shift_remove(&label);
            }
        }
    }

    Ok(boxes
        .into_iter()
        .map(|(box_idx, lenses)| {
            (box_idx as i64 + 1)
                * lenses
                    .into_values()
                    .enumerate()
                    .map(|(slot_idx, focal_length)| (slot_idx as i64 + 1) * focal_length as i64)
                    .sum::<i64>()
        })
        .sum())
}

fn hash(s: &str) -> u8 {
    let mut hash = 0i64;
    for c in s.chars() {
        hash += c as i64;
        hash *= 17;
        hash %= 256;
    }
    hash as u8
}

#[derive(Debug)]
enum LensOp {
    Add { label: String, focal_length: u8 },
    Remove { label: String },
}

fn parse_lens_ops(input: &str) -> Vec<LensOp> {
    let mut out = vec![];
    for s in input.split(',') {
        if s.contains('=') {
            let mut it = s.split('=');
            out.push(LensOp::Add {
                label: it.next().unwrap().to_string(),
                focal_length: it.next().unwrap().parse().unwrap(),
            });
        } else {
            out.push(LensOp::Remove {
                label: s.strip_suffix('-').unwrap().to_string(),
            })
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
        let input_path = Path::new("./src/day15/sample");
        assert_eq!(part1(input_path).unwrap(), 1320);

        let input_path = Path::new("./src/day15/input");
        assert_eq!(part1(input_path).unwrap(), 516469);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day15/sample");
        assert_eq!(part2(input_path).unwrap(), 145);

        let input_path = Path::new("./src/day15/input");
        assert_eq!(part2(input_path).unwrap(), 221627);
    }
}
