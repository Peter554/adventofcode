package main

import (
	"strings"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	groups := strings.Split(strings.Join(lines, "\n"), "\n\n")
	sum := 0
	for _, group := range groups {
		sum += countQuestionsAny(group)
	}
	return sum
}

func Part2(lines []string) int {
	groups := strings.Split(strings.Join(lines, "\n"), "\n\n")
	sum := 0
	for _, group := range groups {
		sum += countQuestionsEvery(group)
	}
	return sum
}

func countQuestionsAny(group string) int {
	m := map[rune]bool{}
	for _, line := range strings.Split(group, "\n") {
		for _, question := range line {
			m[question] = true
		}
	}
	return len(m)
}

func countQuestionsEvery(group string) int {
	lines := strings.Split(group, "\n")
	m := map[rune]int{}
	for _, line := range lines {
		for _, question := range line {
			if _, exists := m[question]; exists {
				m[question]++
			} else {
				m[question] = 1
			}
		}
	}
	count := 0
	for _, v := range m {
		if v == len(lines) {
			count++
		}
	}
	return count
}
