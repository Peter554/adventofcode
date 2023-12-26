use anyhow::Result;
use itertools::Itertools;
use slotmap::{DefaultKey, SecondaryMap, SlotMap};
use std::{cmp::Ordering, collections::HashSet, fs, path::Path, usize};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let tree = build_tree(&input);
    Ok(tree
        .bricks
        .keys()
        .filter(|k| can_disintegrate_safely(&tree, k))
        .count() as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let tree = build_tree(&input);

    let mut total = 0;
    for key in tree.bricks.keys() {
        total += number_of_bricks_falling(&tree, &key);
    }
    Ok(total as i64)
}

#[derive(Debug, Clone)]
struct Tree {
    bricks: SlotMap<DefaultKey, [[usize; 2]; 3]>,
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

    while let Some(brick_to_drop) = bricks_to_drop.pop() {
        let brick = [
            brick_to_drop[0],
            brick_to_drop[1],
            [0, 0], // Correct this later.
        ];
        let brick_key = bricks.insert(brick);

        let mut supported_by_keys = vec![];
        let mut supported_at_height = 0;
        for (other_brick_key, other_brick) in bricks.iter() {
            if other_brick_key == brick_key {
                continue;
            }
            let other_brick_height = other_brick[2][1];
            if overlaps(brick[0], other_brick[0]) && overlaps(brick[1], other_brick[1]) {
                match other_brick_height.cmp(&supported_at_height) {
                    Ordering::Greater => {
                        supported_by_keys = vec![other_brick_key];
                        supported_at_height = other_brick_height;
                    }
                    Ordering::Equal => {
                        supported_by_keys.push(other_brick_key);
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
        let brick = bricks.get_mut(brick_key).unwrap();
        brick[2] = [
            supported_at_height + 1,
            supported_at_height + 1 + brick_to_drop[2][1] - brick_to_drop[2][0],
        ];
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

fn can_disintegrate_safely(tree: &Tree, brick_key: &DefaultKey) -> bool {
    match tree.supports.get(*brick_key) {
        Some(supported) => supported.iter().all(|k| tree.supported_by[*k].len() > 1),
        None => true,
    }
}

fn number_of_bricks_falling(tree: &Tree, brick_to_disintegrate: &DefaultKey) -> usize {
    let mut removed_keys = HashSet::new();
    removed_keys.insert(*brick_to_disintegrate);
    for higher_brick_key in tree
        .bricks
        .iter()
        .filter(|(_, b)| b[2][0] > tree.bricks[*brick_to_disintegrate][2][1])
        // Topological order.
        .sorted_by_key(|(_, b)| b[2][0])
        .map(|(k, _)| k)
    {
        if tree
            .supported_by
            .get(higher_brick_key)
            .unwrap()
            .difference(&removed_keys)
            .count()
            == 0
        {
            // Brick is no longer supported.
            removed_keys.insert(higher_brick_key);
        }
    }
    removed_keys.len() - 1
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
        assert_eq!(part2(input_path).unwrap(), 7);

        let input_path = Path::new("./src/day22/input");
        assert_eq!(part2(input_path).unwrap(), 74594);
    }
}
