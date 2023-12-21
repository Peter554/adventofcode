use anyhow::Result;
use std::{
    collections::{HashMap, VecDeque},
    fmt::Debug,
    fs,
    path::Path,
};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let mut modules = parse_input(&input);
    let mut n_low = 0;
    let mut n_high = 0;
    let mut q = VecDeque::new();
    for _ in 0..1000 {
        q.push_back(Pulse {
            sender_id: "".to_string(),
            receiver_id: "broadcaster".to_string(),
            type_: PulseType::Low,
        });
        while let Some(pulse) = q.pop_front() {
            if matches!(pulse.type_, PulseType::Low) {
                n_low += 1;
            } else {
                n_high += 1;
            }
            let receiver = modules.get_mut(&pulse.receiver_id).unwrap();
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

fn parse_input(input: &str) -> HashMap<String, Box<dyn Module>> {
    let mut out: HashMap<String, Box<dyn Module>> = HashMap::new();
    for line in input.lines() {
        let mut it = line.split(" -> ");
        let id = it.next().unwrap();
        if id == "broadcaster" {
            out.insert(
                "broadcaster".to_string(),
                Box::new(BroadcasterModule::new()),
            );
        } else if id.starts_with('%') {
            let id: String = id.chars().skip(1).collect();
            out.insert(id.clone(), Box::new(FlipFlopModule::new(id)));
        } else if id.starts_with('&') {
            let id: String = id.chars().skip(1).collect();
            out.insert(id.clone(), Box::new(ConjunctionModule::new(id)));
        }
    }
    for line in input.lines() {
        let mut it = line.split(" -> ");
        let mut sender_id = it.next().unwrap().to_string();
        if sender_id.starts_with('%') || sender_id.starts_with('&') {
            sender_id = sender_id.chars().skip(1).collect();
        }
        for receiver_id in it.next().unwrap().split(", ") {
            let mut sender = out.remove(&sender_id).unwrap();
            let mut receiver = match out.remove(receiver_id) {
                Some(receiver) => receiver,
                None => Box::new(OutputModule::new(receiver_id.to_string())),
            };
            sender.connect_output(receiver.as_ref());
            receiver.connect_input(sender.as_ref());
            out.insert(sender.id().to_string(), sender);
            out.insert(receiver.id().to_string(), receiver);
        }
    }
    out
}

#[derive(Clone)]
struct Pulse {
    sender_id: String,
    receiver_id: String,
    type_: PulseType,
}

#[derive(Debug, Clone)]
enum PulseType {
    High,
    Low,
}

trait Module: Debug {
    fn id(&self) -> &str;

    fn connect_input(&mut self, input: &dyn Module);

    fn connect_output(&mut self, output: &dyn Module);

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse>;
}

#[derive(Debug)]
struct BroadcasterModule {
    output_ids: Vec<String>,
}

impl BroadcasterModule {
    fn new() -> BroadcasterModule {
        BroadcasterModule { output_ids: vec![] }
    }
}

impl Module for BroadcasterModule {
    fn id(&self) -> &str {
        "broadcaster"
    }

    fn connect_input(&mut self, _input: &dyn Module) {
        panic!()
    }

    fn connect_output(&mut self, output: &dyn Module) {
        self.output_ids.push(output.id().to_string())
    }

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse> {
        self.output_ids
            .iter()
            .map(|output_id| Pulse {
                sender_id: self.id().to_string(),
                receiver_id: output_id.to_string(),
                type_: pulse.type_.clone(),
            })
            .collect()
    }
}

#[derive(Debug)]
struct OutputModule {
    id: String,
}

impl OutputModule {
    fn new(id: String) -> OutputModule {
        OutputModule { id }
    }
}

impl Module for OutputModule {
    fn id(&self) -> &str {
        &self.id
    }

    fn connect_input(&mut self, _input: &dyn Module) {}

    fn connect_output(&mut self, _output: &dyn Module) {
        panic!()
    }

    fn handle_pulse(&mut self, _pulse: &Pulse) -> Vec<Pulse> {
        vec![]
    }
}

#[derive(Debug)]
struct FlipFlopModule {
    id: String,
    on: bool,
    output_ids: Vec<String>,
}

impl FlipFlopModule {
    fn new(id: String) -> FlipFlopModule {
        FlipFlopModule {
            id,
            on: false,
            output_ids: vec![],
        }
    }
}

impl Module for FlipFlopModule {
    fn id(&self) -> &str {
        &self.id
    }

    fn connect_input(&mut self, _input: &dyn Module) {}

    fn connect_output(&mut self, output: &dyn Module) {
        self.output_ids.push(output.id().to_string())
    }

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse> {
        match pulse.type_ {
            PulseType::High => {
                vec![]
            }
            PulseType::Low => {
                self.on = !self.on;
                self.output_ids
                    .iter()
                    .map(|output_id| Pulse {
                        sender_id: self.id().to_string(),
                        receiver_id: output_id.to_string(),
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
    id: String,
    memory: HashMap<String, PulseType>,
    output_ids: Vec<String>,
}

impl ConjunctionModule {
    fn new(id: String) -> ConjunctionModule {
        ConjunctionModule {
            id,
            memory: HashMap::new(),
            output_ids: vec![],
        }
    }
}

impl Module for ConjunctionModule {
    fn id(&self) -> &str {
        &self.id
    }

    fn connect_input(&mut self, input: &dyn Module) {
        self.memory
            .entry(input.id().to_string())
            .or_insert(PulseType::Low);
    }

    fn connect_output(&mut self, output: &dyn Module) {
        self.output_ids.push(output.id().to_string())
    }

    fn handle_pulse(&mut self, pulse: &Pulse) -> Vec<Pulse> {
        self.memory
            .insert(pulse.sender_id.clone(), pulse.type_.clone());
        self.output_ids
            .iter()
            .map(|output_id| Pulse {
                sender_id: self.id().to_string(),
                receiver_id: output_id.to_string(),
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
