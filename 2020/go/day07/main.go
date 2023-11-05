package main

import (
	"github.com/peter554/adventofcode/2020/go/day07/parse"
	"github.com/peter554/adventofcode/2020/go/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	parent2Children := map[string]map[string]int{}
	for _, line := range lines {
		parent, children := parse.Parse(line)
		parent2Children[parent] = children
	}
	return len(uniqueParents(parent2Children, "shiny gold"))
}

func Part2(lines []string) int {
	parent2Children := map[string]map[string]int{}
	for _, line := range lines {
		parent, children := parse.Parse(line)
		parent2Children[parent] = children
	}
	return countChildren(parent2Children, "shiny gold")
}

func uniqueParents(parent2Children map[string]map[string]int, child string) map[string]bool {
	parents := map[string]bool{}
	for parent, children := range parent2Children {
		for c := range children {
			if c == child {
				parents[parent] = true
				for parentsParent := range uniqueParents(parent2Children, parent) {
					parents[parentsParent] = true
				}
			}
		}
	}
	return parents
}

func countChildren(parent2Children map[string]map[string]int, parent string) int {
	children := parent2Children[parent]
	total := 0
	for child, count := range children {
		total += count * (1 + countChildren(parent2Children, child))
	}
	return total
}
