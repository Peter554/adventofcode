use anyhow::Result;
use num::integer::lcm;
use std::{
    collections::{HashMap, HashSet},
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (directions, nodes) = parse_input(&input);

    let mut counter = 0;
    let mut current_node = nodes.get("AAA").unwrap();
    while current_node.id != "ZZZ" {
        let direction = &directions[counter % directions.len()];
        let next_node_id = match direction {
            Direction::Left => current_node.left_node_id.clone(),
            Direction::Right => current_node.right_node_id.clone(),
        };
        current_node = nodes.get(&next_node_id).unwrap();
        counter += 1;
    }
    Ok(counter as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (directions, nodes) = parse_input(&input);

    let node_ids_ending_in_a = nodes
        .keys()
        .filter(|id| id.ends_with('A'))
        .cloned()
        .collect::<HashSet<_>>();
    let node_ids_ending_in_z = nodes
        .keys()
        .filter(|id| id.ends_with('Z'))
        .cloned()
        .collect::<HashSet<_>>();

    // Collect a counter for each start node and take the lowest common multiple (LCM).
    // There is no guarantee that LCM is the correct solution here, but it seems to work.
    // https://www.reddit.com/r/adventofcode/comments/18dfpub/2023_day_8_part_2_why_is_spoiler_correct/
    let mut counters = vec![];
    for start_node_id in node_ids_ending_in_a {
        let mut counter = 0;
        let mut current_node = nodes.get(&start_node_id).unwrap();
        while !node_ids_ending_in_z.contains(&current_node.id) {
            let direction = &directions[counter % directions.len()];
            let next_node_id = match direction {
                Direction::Left => current_node.left_node_id.clone(),
                Direction::Right => current_node.right_node_id.clone(),
            };
            current_node = nodes.get(&next_node_id).unwrap();
            counter += 1;
        }
        counters.push(counter);
    }

    Ok(counters.into_iter().fold(1, lcm) as i64)
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
        let input_path = Path::new("./src/day08/sample2");
        assert_eq!(part2(input_path).unwrap(), 6);

        let input_path = Path::new("./src/day08/input");
        assert_eq!(part2(input_path).unwrap(), 12030780859469);
    }
}
