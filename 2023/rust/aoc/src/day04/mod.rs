use anyhow::Result;
use std::{
    collections::{HashMap, HashSet, VecDeque},
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(input
        .lines()
        .map(parse_card)
        .map(|card| {
            if card.len_my_winning_numbers == 0 {
                0
            } else {
                1 << (card.len_my_winning_numbers - 1)
            }
        })
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let cards = input
        .lines()
        .map(parse_card)
        .map(|card| (card.id, card))
        .collect::<HashMap<_, _>>();
    let mut total_cards = 0;
    let mut q = cards.values().collect::<VecDeque<_>>();
    while !q.is_empty() {
        total_cards += 1;
        let card = q.pop_front().unwrap();
        if card.len_my_winning_numbers == 0 {
            continue;
        } else {
            for id in card.id + 1..=card.id + card.len_my_winning_numbers {
                q.push_back(cards.get(&id).unwrap());
            }
        }
    }
    Ok(total_cards)
}

struct Card {
    id: u8,
    len_my_winning_numbers: u8,
}

impl Card {
    fn new(id: u8, winning_numbers: HashSet<u8>, my_numbers: HashSet<u8>) -> Self {
        let my_winning_numbers = winning_numbers
            .intersection(&my_numbers)
            .cloned()
            .collect::<HashSet<u8>>();
        Card {
            id,
            len_my_winning_numbers: my_winning_numbers.len() as u8,
        }
    }
}

fn parse_card(raw_card: &str) -> Card {
    let mut it = raw_card.split(':');
    let id = it
        .next()
        .unwrap()
        .strip_prefix("Card ")
        .unwrap()
        .trim()
        .parse::<u8>()
        .unwrap();
    let mut it = it.next().unwrap().split('|');
    let winning_numbers = it
        .next()
        .unwrap()
        .split_ascii_whitespace()
        .map(|s| s.trim().parse::<u8>().unwrap())
        .collect();
    let my_numbers = it
        .next()
        .unwrap()
        .split_ascii_whitespace()
        .map(|s| s.trim().parse::<u8>().unwrap())
        .collect();
    Card::new(id, winning_numbers, my_numbers)
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day04/sample");
        assert_eq!(part1(input_path).unwrap(), 13);

        let input_path = Path::new("./src/day04/input");
        assert_eq!(part1(input_path).unwrap(), 23673);
    }

    #[test]
    fn test_part2_sample() {
        let input_path = Path::new("./src/day04/sample");
        assert_eq!(part2(input_path).unwrap(), 30);
    }

    #[test]
    #[cfg_attr(not(feature = "slow"), ignore = "slow")]
    fn test_part2_real() {
        let input_path = Path::new("./src/day04/input");
        assert_eq!(part2(input_path).unwrap(), 12263631);
    }
}
