use anyhow::Result;
use itertools::Itertools;
use slotmap::{DefaultKey, SecondaryMap, SlotMap};
use std::{
    cmp::Ordering,
    collections::{HashMap, HashSet},
    fs,
    path::Path,
    usize,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let tree = build_tree(&input);
    Ok(tree
        .bricks
        .keys()
        .filter(|k| can_disintegrate(&tree, k))
        .count() as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let _ = input;
    Ok(42)
}

#[derive(Debug)]
struct Tree {
    bricks: SlotMap<DefaultKey, ([usize; 2], [usize; 2], usize)>,
    supports: SecondaryMap<DefaultKey, HashSet<DefaultKey>>,
    supported_by: SecondaryMap<DefaultKey, HashSet<DefaultKey>>,
}

fn build_tree(input: &str) -> Tree {
    let mut bricks_to_drop = input
        .lines()
        .map(|line| {
            let mut it = line.split('~');
            let start = it
                .next()
                .unwrap()
                .split(',')
                .map(|s| s.parse::<usize>().unwrap())
                .collect::<Vec<_>>();
            let end = it
                .next()
                .unwrap()
                .split(',')
                .map(|s| s.parse::<usize>().unwrap())
                .collect::<Vec<_>>();
            [[start[0], end[0]], [start[1], end[1]], [start[2], end[2]]]
        })
        .sorted_by_key(|b| b[2][0])
        .rev()
        .collect::<Vec<_>>();

    let mut bricks = SlotMap::new();
    let mut supports = SecondaryMap::new();
    let mut supported_by = SecondaryMap::new();

    let mut heights: HashMap<DefaultKey, usize> = HashMap::new();
    while let Some(brick_to_drop) = bricks_to_drop.pop() {
        let brick = (
            brick_to_drop[0],
            brick_to_drop[1],
            brick_to_drop[2][1] - brick_to_drop[2][0] + 1,
        );
        let brick_key = bricks.insert(brick);

        let mut supported_by_keys = vec![];
        let mut supported_at_height = 0usize;
        for (other_brick_key, other_brick_height) in heights.iter() {
            let other_brick = bricks.get(*other_brick_key).unwrap();
            if overlaps(brick.0, other_brick.0) && overlaps(brick.1, other_brick.1) {
                match other_brick_height.cmp(&supported_at_height) {
                    Ordering::Greater => {
                        supported_by_keys = vec![*other_brick_key];
                        supported_at_height = *other_brick_height;
                    }
                    Ordering::Equal => {
                        supported_by_keys.push(*other_brick_key);
                    }
                    Ordering::Less => continue,
                }
            }
        }

        for key in supported_by_keys.iter() {
            supports
                .entry(*key)
                .unwrap()
                .or_insert(HashSet::new())
                .insert(brick_key);
        }
        supported_by.insert(
            brick_key,
            supported_by_keys.into_iter().collect::<HashSet<_>>(),
        );
        heights.insert(brick_key, supported_at_height + brick.2);
    }

    Tree {
        bricks,
        supports,
        supported_by,
    }
}

fn overlaps(a: [usize; 2], b: [usize; 2]) -> bool {
    a[0] <= b[1] && b[0] <= a[1]
}

fn can_disintegrate(tree: &Tree, brick_key: &DefaultKey) -> bool {
    match &tree.supports.get(*brick_key) {
        Some(supported) => supported.iter().all(|k| tree.supported_by[*k].len() > 1),
        None => true,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day22/sample");
        assert_eq!(part1(input_path).unwrap(), 5);

        let input_path = Path::new("./src/day22/input");
        assert_eq!(part1(input_path).unwrap(), 485);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day22/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day22/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
