use anyhow::Result;
use pest::Parser;
use pest_derive::Parser;

pub struct Game {
    pub id: u8,
    pub hands: Vec<Hand>,
}

pub struct Hand {
    pub red: u8,
    pub green: u8,
    pub blue: u8,
}

#[derive(Parser)]
#[grammar = "day02/grammar.pest"]
struct InputParser;

pub fn parse(input: &str) -> Result<Vec<Game>> {
    let mut games = vec![];
    let file = InputParser::parse(Rule::file, input)?.next().unwrap();
    for file_inner in file.into_inner() {
        match file_inner.as_rule() {
            Rule::game => {
                let game = file_inner;
                let mut game_inners = game.into_inner();
                let game_id = game_inners.next().unwrap().as_str().parse::<u8>()?;
                let mut out_game = Game {
                    id: game_id,
                    hands: vec![],
                };
                let hands = game_inners.next().unwrap();
                for hand in hands.into_inner() {
                    let mut out_hand = Hand {
                        red: 0,
                        green: 0,
                        blue: 0,
                    };
                    for hand_part in hand.into_inner() {
                        let mut hand_part_inners = hand_part.into_inner();
                        let n = hand_part_inners.next().unwrap().as_str().parse::<u8>()?;
                        match hand_part_inners.next().unwrap().as_str() {
                            "red" => {
                                out_hand.red = n;
                            }
                            "green" => {
                                out_hand.green = n;
                            }
                            "blue" => {
                                out_hand.blue = n;
                            }
                            _ => unreachable!(),
                        }
                    }
                    out_game.hands.push(out_hand);
                }
                games.push(out_game);
            }
            Rule::EOI => {}
            _ => unreachable!(),
        }
    }
    Ok(games)
}
