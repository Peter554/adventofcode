use anyhow::{Error, Result};
use itertools::Itertools;
use std::{collections::HashMap, fs, path::Path, str::FromStr};

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(parse_input(&input)
        .into_iter()
        .sorted_by_key(|(hand, _)| hand.clone())
        .enumerate()
        .map(|(idx, (_, bid))| {
            let rank = (idx + 1) as u64;
            rank * bid
        })
        .sum::<u64>() as i64)
}

fn parse_input(input: &str) -> Vec<(Hand, u64)> {
    input
        .lines()
        .map(|line| {
            let mut it = line.split_ascii_whitespace();
            (
                it.next().unwrap().parse().unwrap(),
                it.next().unwrap().parse().unwrap(),
            )
        })
        .collect()
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone)]
struct Hand {
    type_: HandType,
    cards: [Card; 5],
}

impl FromStr for Hand {
    type Err = Error;

    fn from_str(s: &str) -> Result<Self> {
        let cards = s
            .chars()
            .map(|c| match c {
                'J' => Card::Joker,
                '2' => Card::Two,
                '3' => Card::Three,
                '4' => Card::Four,
                '5' => Card::Five,
                '6' => Card::Six,
                '7' => Card::Seven,
                '8' => Card::Eight,
                '9' => Card::Nine,
                'T' => Card::Ten,
                'Q' => Card::Queen,
                'K' => Card::King,
                'A' => Card::Ace,
                _ => unreachable!(),
            })
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();
        Ok(Hand::from_cards(cards))
    }
}

impl Hand {
    fn from_cards(cards: [Card; 5]) -> Hand {
        let type_ = {
            let mut card_counts = HashMap::new();
            for card in cards.iter() {
                *card_counts.entry(card.clone()).or_insert(0) += 1;
            }

            // Convert jokers into the most common card, for the purpose of determining the hand type.
            'block: {
                if !card_counts.contains_key(&Card::Joker) {
                    break 'block;
                }
                let most_common_non_joker_card = card_counts
                    .iter()
                    .filter(|&(card, _)| card != &Card::Joker)
                    .sorted_by_key(|&(_, count)| count)
                    .last()
                    .map(|(card, _)| card.clone());
                if most_common_non_joker_card.is_none() {
                    break 'block;
                }
                let most_common_non_joker_card = most_common_non_joker_card.unwrap();
                *card_counts.get_mut(&most_common_non_joker_card).unwrap() +=
                    *card_counts.get(&Card::Joker).unwrap();
                card_counts.remove(&Card::Joker);
            }

            let card_counts = card_counts.into_values().sorted().collect::<Vec<_>>();
            match card_counts.as_slice() {
                [5] => HandType::FiveOfAKind,
                [1, 4] => HandType::FourOfAKind,
                [2, 3] => HandType::FullHouse,
                [1, 1, 3] => HandType::ThreeOfAKind,
                [1, 2, 2] => HandType::TwoPair,
                [1, 1, 1, 2] => HandType::OnePair,
                _ => HandType::HighCard,
            }
        };
        Hand { type_, cards }
    }
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone, Hash)]
enum Card {
    Joker,
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    Queen,
    King,
    Ace,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone)]
enum HandType {
    HighCard,
    OnePair,
    TwoPair,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind,
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day07/sample");
        assert_eq!(part2(input_path).unwrap(), 5905);

        let input_path = Path::new("./src/day07/input");
        assert_eq!(part2(input_path).unwrap(), 253630098);
    }
}
