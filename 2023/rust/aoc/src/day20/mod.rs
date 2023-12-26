use anyhow::Result;
use slotmap::{DefaultKey, Key, SlotMap};
use std::{
    collections::{HashMap, VecDeque},
    fmt::Debug,
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (mut modules, index) = parse_input(&input);
    let mut n_low = 0;
    let mut n_high = 0;
    let mut q = VecDeque::new();
    for _ in 0..1000 {
        q.push_back(Pulse {
            sender: DefaultKey::null(),
            receiver: *index.get("broadcaster").unwrap(),
            type_: PulseType::Low,
        });
        while let Some(pulse) = q.pop_front() {
            if matches!(pulse.type_, PulseType::Low) {
                n_low += 1;
            } else {
                n_high += 1;
            }
            let receiver = modules.get_mut(pulse.receiver).unwrap();
            for output_pulse in receiver.handle_pulse(&pulse) {
                q.push_back(output_pulse);
            }
        }
    }
    Ok(n_low * n_high)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let _input = fs::read_to_string(input_path)?;
    Ok(42)
}

fn parse_input(
    input: &str,
) -> (
    SlotMap<DefaultKey, Box<dyn Module>>,
    HashMap<String, DefaultKey>,
) {
    let mut modules: SlotMap<DefaultKey, Box<dyn Module>> = SlotMap::with_key();
    let mut index: HashMap<String, DefaultKey> = HashMap::new();
    for line in input.lines() {
        let mut it = line.split(" -> ");
        let id = it.next().unwrap();
        if id == "broadcaster" {
            let key = modules.insert(Box::new(BroadcasterModule::new()));
            index.insert("broadcaster".to_string(), key);
        } else if id.starts_with('%') {
            let id: String = id.chars().skip(1).collect();
            let key = modules.insert(Box::new(FlipFlopModule::new()));
            index.insert(id, key);
        } else if id.starts_with('&') {
            let id: String = id.chars().skip(1).collect();
            let key = modules.insert(Box::new(ConjunctionModule::new()));
            index.insert(id, key);
        }
    }
    for line in input.lines() {
        let mut it = line.split(" -> ");
        let mut sender_id = it.next().unwrap().to_string();
        if sender_id.starts_with('%') || sender_id.starts_with('&') {
            sender_id = sender_id.chars().skip(1).collect();
        }
        let sender_key = *index.get(&sender_id).unwrap();
        for receiver_id in it.next().unwrap().split(", ") {
            let receiver_key = match index.get(receiver_id) {
                Some(receiver_key) => *receiver_key,
                None => {
                    let key = modules.insert(Box::new(OutputModule::new()));
                    index.insert(receiver_id.to_string(), key);
                    key
                }
            };
            let [sender, receiver] = modules
                .get_disjoint_mut([sender_key, receiver_key])
                .unwrap();
            sender.connect_output(&receiver_key);
            receiver.connect_input(&sender_key);
        }
    }
    (modules, index)
}

#[derive(Clone)]
struct Pulse {
    sender: DefaultKey,
    receiver: DefaultKey,
    type_: PulseType,
}

#[derive(Debug, Clone)]
enum PulseType {
    High,
    Low,
}

trait Module: Debug {
    fn connect_input(&mut self, input: &DefaultKey);

    fn connect_output(&mut self, output: &DefaultKey);

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse>;
}

#[derive(Debug)]
struct BroadcasterModule {
    outputs: Vec<DefaultKey>,
}

impl BroadcasterModule {
    fn new() -> BroadcasterModule {
        BroadcasterModule { outputs: vec![] }
    }
}

impl Module for BroadcasterModule {
    fn connect_input(&mut self, _input: &DefaultKey) {
        panic!()
    }

    fn connect_output(&mut self, output: &DefaultKey) {
        self.outputs.push(*output)
    }

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse> {
        self.outputs
            .iter()
            .cloned()
            .map(|output| Pulse {
                sender: pulse.receiver,
                receiver: output,
                type_: pulse.type_.clone(),
            })
            .collect()
    }
}

#[derive(Debug)]
struct OutputModule;

impl OutputModule {
    fn new() -> OutputModule {
        OutputModule
    }
}

impl Module for OutputModule {
    fn connect_input(&mut self, _input: &DefaultKey) {}

    fn connect_output(&mut self, _output: &DefaultKey) {
        panic!()
    }

    fn handle_pulse(&mut self, _pulse: &Pulse) -> Vec<Pulse> {
        vec![]
    }
}

#[derive(Debug)]
struct FlipFlopModule {
    on: bool,
    outputs: Vec<DefaultKey>,
}

impl FlipFlopModule {
    fn new() -> FlipFlopModule {
        FlipFlopModule {
            on: false,
            outputs: vec![],
        }
    }
}

impl Module for FlipFlopModule {
    fn connect_input(&mut self, _input: &DefaultKey) {}

    fn connect_output(&mut self, output: &DefaultKey) {
        self.outputs.push(*output)
    }

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse> {
        match pulse.type_ {
            PulseType::High => {
                vec![]
            }
            PulseType::Low => {
                self.on = !self.on;
                self.outputs
                    .iter()
                    .cloned()
                    .map(|output| Pulse {
                        sender: pulse.receiver,
                        receiver: output,
                        type_: match self.on {
                            true => PulseType::High,
                            false => PulseType::Low,
                        },
                    })
                    .collect()
            }
        }
    }
}

#[derive(Debug)]
struct ConjunctionModule {
    memory: HashMap<DefaultKey, PulseType>,
    outputs: Vec<DefaultKey>,
}

impl ConjunctionModule {
    fn new() -> ConjunctionModule {
        ConjunctionModule {
            memory: HashMap::new(),
            outputs: vec![],
        }
    }
}

impl Module for ConjunctionModule {
    fn connect_input(&mut self, input: &DefaultKey) {
        self.memory.entry(*input).or_insert(PulseType::Low);
    }

    fn connect_output(&mut self, output: &DefaultKey) {
        self.outputs.push(*output)
    }

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse> {
        self.memory.insert(pulse.sender, pulse.type_.clone());
        self.outputs
            .iter()
            .cloned()
            .map(|output| Pulse {
                sender: pulse.receiver,
                receiver: output,
                type_: if self.memory.values().all(|v| matches!(v, PulseType::High)) {
                    PulseType::Low
                } else {
                    PulseType::High
                },
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day20/sample");
        assert_eq!(part1(input_path).unwrap(), 32000000);

        let input_path = Path::new("./src/day20/sample2");
        assert_eq!(part1(input_path).unwrap(), 11687500);

        let input_path = Path::new("./src/day20/input");
        assert_eq!(part1(input_path).unwrap(), 680278040);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day20/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day20/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
