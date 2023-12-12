use anyhow::Result;
use std::{
    collections::{HashMap, HashSet},
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(input
        .lines()
        .map(parse_card)
        .map(|card| {
            if card.number_of_winning_numbers == 0 {
                0
            } else {
                1 << (card.number_of_winning_numbers - 1)
            }
        })
        .sum())
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let cards = input.lines().map(parse_card).collect::<Vec<_>>();
    let mut card_counts = HashMap::new();
    for card in cards.iter() {
        let this_card_count = *card_counts.entry(card.clone()).or_insert(1);
        for other_card in
            cards[(card.id as usize)..(card.id + card.number_of_winning_numbers) as usize].iter()
        {
            let other_card_count = card_counts.entry(other_card.clone()).or_insert(1);
            *other_card_count += this_card_count;
        }
    }
    Ok(card_counts.values().sum())
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Card {
    id: u8,
    number_of_winning_numbers: u8,
}

impl Card {
    fn new(id: u8, winning_numbers: HashSet<u8>, my_numbers: HashSet<u8>) -> Self {
        let my_winning_numbers = winning_numbers
            .intersection(&my_numbers)
            .cloned()
            .collect::<HashSet<u8>>();
        Card {
            id,
            number_of_winning_numbers: my_winning_numbers.len() as u8,
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
    fn test_part2() {
        let input_path = Path::new("./src/day04/sample");
        assert_eq!(part2(input_path).unwrap(), 30);

        let input_path = Path::new("./src/day04/input");
        assert_eq!(part2(input_path).unwrap(), 12263631);
    }
}
