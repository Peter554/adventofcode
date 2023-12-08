use anyhow::Result;
use std::{collections::HashMap, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (directions, nodes) = parse_input(&input);
    dbg!(&nodes);

    let mut counter = 0;
    let mut current_node = nodes.get("AAA").unwrap();
    while current_node.id != "ZZZ" {
        let current_node_id = match directions[counter % directions.len()] {
            Direction::Left => current_node.left_node_id.clone(),
            Direction::Right => current_node.right_node_id.clone(),
        };
        current_node = nodes.get(&current_node_id).unwrap();
        counter += 1;
    }
    Ok(counter as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let _ = input;
    Ok(42)
}

fn parse_input(s: &str) -> (Vec<Direction>, HashMap<String, Node>) {
    let mut it = s.split("\n\n");

    let directions = it
        .next()
        .unwrap()
        .chars()
        .map(|c| match c {
            'L' => Direction::Left,
            'R' => Direction::Right,
            _ => panic!(),
        })
        .collect();

    let mut nodes = HashMap::new();
    for line in it.next().unwrap().lines() {
        let mut it = line.split('=');
        let node_id = it.next().unwrap().trim().to_string();
        let mut it = it
            .next()
            .unwrap()
            .trim_matches(|c| c == ' ' || c == '(' || c == ')')
            .split(',');
        let left_node_id = it.next().unwrap().trim().to_string();
        let right_node_id = it.next().unwrap().trim().to_string();
        let node = nodes.entry(node_id.clone()).or_insert(Node {
            id: node_id,
            left_node_id: left_node_id.clone(),
            right_node_id: right_node_id.clone(),
        });
        node.left_node_id = left_node_id;
        node.right_node_id = right_node_id;
    }

    (directions, nodes)
}

#[derive(Debug)]
enum Direction {
    Left,
    Right,
}

#[derive(Debug)]
struct Node {
    id: String,
    left_node_id: String,
    right_node_id: String,
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day08/sample");
        assert_eq!(part1(input_path).unwrap(), 6);

        let input_path = Path::new("./src/day08/input");
        assert_eq!(part1(input_path).unwrap(), 12169);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day08/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day08/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
