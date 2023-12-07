use anyhow::Result;
use std::{collections::HashMap, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let mut input = parse_input(&input);
    input.sort_by_key(|(hand, _)| hand.clone());
    Ok(input
        .iter()
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
                parse_hand(it.next().unwrap()),
                it.next().unwrap().parse().unwrap(),
            )
        })
        .collect()
}

fn parse_hand(s: &str) -> Hand {
    let cards = s
        .chars()
        .map(|c| match c {
            '2' => Card::Two,
            '3' => Card::Three,
            '4' => Card::Four,
            '5' => Card::Five,
            '6' => Card::Six,
            '7' => Card::Seven,
            '8' => Card::Eight,
            '9' => Card::Nine,
            'T' => Card::Ten,
            'J' => Card::Jack,
            'Q' => Card::Queen,
            'K' => Card::King,
            'A' => Card::Ace,
            _ => unreachable!(),
        })
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
    Hand::from_cards(cards)
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone)]
struct Hand {
    type_: HandType,
    cards: [Card; 5],
}

impl Hand {
    fn from_cards(cards: [Card; 5]) -> Hand {
        let type_ = {
            let mut m = HashMap::new();
            for card in cards.iter() {
                *m.entry(card.clone()).or_insert(0) += 1;
            }
            let mut counts = m.into_values().collect::<Vec<_>>();
            counts.sort();
            if counts == vec![5] {
                HandType::FiveOfAKind
            } else if counts == vec![1, 4] {
                HandType::FourOfAKind
            } else if counts == vec![2, 3] {
                HandType::FullHouse
            } else if counts == vec![1, 1, 3] {
                HandType::ThreeOfAKind
            } else if counts == vec![1, 2, 2] {
                HandType::TwoPair
            } else if counts == vec![1, 1, 1, 2] {
                HandType::OnePair
            } else {
                HandType::HighCard
            }
        };
        Hand { type_, cards }
    }
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone, Hash)]
enum Card {
    Two,
    Three,
    Four,
    Five,
    Six,
    Seven,
    Eight,
    Nine,
    Ten,
    Jack,
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
    fn test_part1() {
        let input_path = Path::new("./src/day07/sample");
        assert_eq!(part1(input_path).unwrap(), 6440);

        let input_path = Path::new("./src/day07/input");
        assert_eq!(part1(input_path).unwrap(), 253603890);
    }
}
