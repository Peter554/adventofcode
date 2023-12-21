use anyhow::Result;
use regex::Regex;
use std::{collections::HashMap, fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (workflows, parts) = parse_input(&input);
    Ok(parts
        .into_iter()
        .filter(|part| is_accepted(&workflows, "in", part))
        .map(|part| part.x + part.m + part.a + part.s)
        .sum::<isize>() as i64)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let (workflows, _) = parse_input(&input);
    let accepted_hypercubes = find_accepted_hypercubes(
        &workflows,
        "in",
        &PartHypercube {
            x_min: 1,
            x_max: 4000,
            m_min: 1,
            m_max: 4000,
            a_min: 1,
            a_max: 4000,
            s_min: 1,
            s_max: 4000,
        },
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
                    let dimension = it.next().unwrap().chars().next().unwrap();
                    let mut it = it.next().unwrap().split(':');
                    let value = it.next().unwrap().parse().unwrap();
                    let outcome = it.next().unwrap().to_string();
                    WorkflowIfRule {
                        dimension,
                        operator,
                        value,
                        outcome,
                    }
                })
                .collect();
            let else_outcome = s
                .clone()
                .last()
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
            Part {
                x: captures[1].parse().unwrap(),
                m: captures[2].parse().unwrap(),
                a: captures[3].parse().unwrap(),
                s: captures[4].parse().unwrap(),
            }
        })
        .collect();

    (workflows, parts)
}

fn is_accepted(workflows: &HashMap<String, Workflow>, workflow: &str, part: &Part) -> bool {
    let workflow = workflows.get(workflow).unwrap();
    for if_rule in workflow.if_rules.iter() {
        let match_ = match (&if_rule.dimension, &if_rule.operator) {
            ('x', Operator::LessThan) => part.x < if_rule.value,
            ('x', Operator::GreaterThan) => part.x > if_rule.value,
            ('m', Operator::LessThan) => part.m < if_rule.value,
            ('m', Operator::GreaterThan) => part.m > if_rule.value,
            ('a', Operator::LessThan) => part.a < if_rule.value,
            ('a', Operator::GreaterThan) => part.a > if_rule.value,
            ('s', Operator::LessThan) => part.s < if_rule.value,
            ('s', Operator::GreaterThan) => part.s > if_rule.value,
            _ => panic!(),
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
        return false;
    } else {
        return is_accepted(workflows, &workflow.else_outcome, part);
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
            match (&if_rule.dimension, &if_rule.operator) {
                ('x', Operator::LessThan) => hypercube.split_x_lt(if_rule.value),
                ('x', Operator::GreaterThan) => hypercube.split_x_gt(if_rule.value),
                ('m', Operator::LessThan) => hypercube.split_m_lt(if_rule.value),
                ('m', Operator::GreaterThan) => hypercube.split_m_gt(if_rule.value),
                ('a', Operator::LessThan) => hypercube.split_a_lt(if_rule.value),
                ('a', Operator::GreaterThan) => hypercube.split_a_gt(if_rule.value),
                ('s', Operator::LessThan) => hypercube.split_s_lt(if_rule.value),
                ('s', Operator::GreaterThan) => hypercube.split_s_gt(if_rule.value),
                _ => panic!(),
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
        return vec![];
    } else {
        return find_accepted_hypercubes(workflows, &workflow.else_outcome, hypercube);
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
    dimension: char,
    operator: Operator,
    value: isize,
    outcome: String,
}

#[derive(Debug)]
enum Operator {
    LessThan,
    GreaterThan,
}

#[derive(Debug)]
struct Part {
    x: isize,
    m: isize,
    a: isize,
    s: isize,
}

#[derive(Debug, Clone)]
struct PartHypercube {
    x_min: isize,
    x_max: isize,
    m_min: isize,
    m_max: isize,
    a_min: isize,
    a_max: isize,
    s_min: isize,
    s_max: isize,
}

impl PartHypercube {
    fn split_x_lt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.x_min >= v {
            (None, Some(self.clone()))
        } else if self.x_max < v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.x_max = v - 1;
            let mut remaining = self.clone();
            remaining.x_min = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_x_gt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.x_max <= v {
            (None, Some(self.clone()))
        } else if self.x_min > v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.x_min = v + 1;
            let mut remaining = self.clone();
            remaining.x_max = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_m_lt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.m_min >= v {
            (None, Some(self.clone()))
        } else if self.m_max < v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.m_max = v - 1;
            let mut remaining = self.clone();
            remaining.m_min = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_m_gt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.m_max <= v {
            (None, Some(self.clone()))
        } else if self.m_min > v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.m_min = v + 1;
            let mut remaining = self.clone();
            remaining.m_max = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_a_lt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.a_min >= v {
            (None, Some(self.clone()))
        } else if self.a_max < v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.a_max = v - 1;
            let mut remaining = self.clone();
            remaining.a_min = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_a_gt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.a_max <= v {
            (None, Some(self.clone()))
        } else if self.a_min > v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.a_min = v + 1;
            let mut remaining = self.clone();
            remaining.a_max = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_s_lt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.s_min >= v {
            (None, Some(self.clone()))
        } else if self.s_max < v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.s_max = v - 1;
            let mut remaining = self.clone();
            remaining.s_min = v;
            (Some(matching), Some(remaining))
        }
    }

    fn split_s_gt(&self, v: isize) -> (Option<PartHypercube>, Option<PartHypercube>) {
        if self.s_max <= v {
            (None, Some(self.clone()))
        } else if self.s_min > v {
            (Some(self.clone()), None)
        } else {
            let mut matching = self.clone();
            matching.s_min = v + 1;
            let mut remaining = self.clone();
            remaining.s_max = v;
            (Some(matching), Some(remaining))
        }
    }

    fn volume(&self) -> usize {
        (self.x_min..=self.x_max).count()
            * (self.m_min..=self.m_max).count()
            * (self.a_min..=self.a_max).count()
            * (self.s_min..=self.s_max).count()
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
