use anyhow::Result;
use regex::Regex;
use std::{collections::HashMap, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (workflows, parts) = parse_input(&input);
    Ok(parts
        .into_iter()
        .filter(|part| is_accepted(&workflows, "in", part))
        .map(|part| part.iter().sum::<isize>())
        .sum::<isize>() as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (workflows, _) = parse_input(&input);
    let accepted_hypercubes = find_accepted_hypercubes(
        &workflows,
        "in",
        &PartHypercube([[1, 4000], [1, 4000], [1, 4000], [1, 4000]]),
    );
    Ok(accepted_hypercubes
        .into_iter()
        .map(|hc| hc.volume() as i64)
        .sum())
}

fn parse_input(input: &str) -> (HashMap<String, Workflow>, Vec<Part>) {
    let mut it = input.split("\n\n");

    let workflows = it
        .next()
        .unwrap()
        .lines()
        .map(|line| {
            let mut it = line.split('{');
            let id = it.next().unwrap().to_string();
            let s = it.next().unwrap().split(',');
            let if_rules = s
                .clone()
                .take(s.clone().count() - 1)
                .map(|s| {
                    let (split_char, operator) = if s.contains('<') {
                        ('<', Operator::LessThan)
                    } else {
                        ('>', Operator::GreaterThan)
                    };
                    let mut it = s.split(split_char);
                    let axis = match it.next().unwrap().chars().next().unwrap() {
                        'x' => 0,
                        'm' => 1,
                        'a' => 2,
                        's' => 3,
                        _ => panic!(),
                    };
                    let mut it = it.next().unwrap().split(':');
                    let value = it.next().unwrap().parse().unwrap();
                    let outcome = it.next().unwrap().to_string();
                    WorkflowIfRule {
                        axis,
                        operator,
                        value,
                        outcome,
                    }
                })
                .collect();
            let else_outcome = s
                .clone()
                .next_back()
                .unwrap()
                .strip_suffix('}')
                .unwrap()
                .to_string();
            let workflow = Workflow {
                id,
                if_rules,
                else_outcome,
            };
            (workflow.id.clone(), workflow)
        })
        .collect();

    let re = Regex::new(r"^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}$").unwrap();
    let parts = it
        .next()
        .unwrap()
        .lines()
        .map(|line| {
            let captures = re.captures(line).unwrap();
            [
                captures[1].parse().unwrap(),
                captures[2].parse().unwrap(),
                captures[3].parse().unwrap(),
                captures[4].parse().unwrap(),
            ]
        })
        .collect();

    (workflows, parts)
}

fn is_accepted(workflows: &HashMap<String, Workflow>, workflow: &str, part: &Part) -> bool {
    let workflow = workflows.get(workflow).unwrap();
    for if_rule in workflow.if_rules.iter() {
        let match_ = match (&if_rule.axis, &if_rule.operator) {
            (axis, Operator::LessThan) => part[*axis] < if_rule.value,
            (axis, Operator::GreaterThan) => part[*axis] > if_rule.value,
        };
        if match_ {
            if if_rule.outcome == "A" {
                return true;
            } else if if_rule.outcome == "R" {
                return false;
            } else {
                return is_accepted(workflows, &if_rule.outcome, part);
            }
        }
    }
    if workflow.else_outcome == "A" {
        true
    } else if workflow.else_outcome == "R" {
        false
    } else {
        is_accepted(workflows, &workflow.else_outcome, part)
    }
}

fn find_accepted_hypercubes(
    workflows: &HashMap<String, Workflow>,
    workflow: &str,
    hypercube: &PartHypercube,
) -> Vec<PartHypercube> {
    let workflow = workflows.get(workflow).unwrap();
    for if_rule in workflow.if_rules.iter() {
        let (matching_hypercube, remaining_hypercube) = {
            match (&if_rule.axis, &if_rule.operator) {
                (axis, Operator::LessThan) => hypercube.split_lt(*axis, if_rule.value),
                (axis, Operator::GreaterThan) => hypercube.split_gt(*axis, if_rule.value),
            }
        };
        if let Some(matching_hypercube) = matching_hypercube {
            let mut out = vec![];
            if if_rule.outcome == "A" {
                out.push(matching_hypercube)
            } else if if_rule.outcome == "R" {
                // Rejected!
            } else {
                out.extend(find_accepted_hypercubes(
                    workflows,
                    &if_rule.outcome,
                    &matching_hypercube,
                ));
            }
            if let Some(remaining_hypercube) = remaining_hypercube {
                out.extend(find_accepted_hypercubes(
                    workflows,
                    &workflow.id,
                    &remaining_hypercube,
                ));
            }
            return out;
        }
    }
    if workflow.else_outcome == "A" {
        vec![hypercube.clone()]
    } else if workflow.else_outcome == "R" {
        vec![]
    } else {
        find_accepted_hypercubes(workflows, &workflow.else_outcome, hypercube)
    }
}

#[derive(Debug)]
struct Workflow {
    id: String,
    if_rules: Vec<WorkflowIfRule>,
    else_outcome: String,
}

#[derive(Debug)]
struct WorkflowIfRule {
    axis: usize,
    operator: Operator,
    value: isize,
    outcome: String,
}

#[derive(Debug)]
enum Operator {
    LessThan,
    GreaterThan,
}

type Part = [isize; 4];

#[derive(Clone)]
struct PartHypercube([[isize; 2]; 4]);

impl PartHypercube {
    fn split_lt(&self, axis: usize, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.0[axis][0] >= v {
            (None, Some(self.clone()))
        } else if self.0[axis][1] < v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.0[axis][1] = v - 1;
            let mut remaining = self.clone();
            remaining.0[axis][0] = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_gt(&self, axis: usize, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.0[axis][1] <= v {
            (None, Some(self.clone()))
        } else if self.0[axis][0] > v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.0[axis][0] = v + 1;
            let mut remaining = self.clone();
            remaining.0[axis][1] = v;
            (Some(matching), Some(remaining))
        }
    }

    fn volume(&self) -> usize {
        self.0.iter().map(|r| (r[0]..=r[1]).count()).product()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day19/sample");
        assert_eq!(part1(input_path).unwrap(), 19114);

        let input_path = Path::new("./src/day19/input");
        assert_eq!(part1(input_path).unwrap(), 480738);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day19/sample");
        assert_eq!(part2(input_path).unwrap(), 167409079868000);

        let input_path = Path::new("./src/day19/input");
        assert_eq!(part2(input_path).unwrap(), 131550418841958);
    }
}
