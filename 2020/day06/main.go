package main

import (
	"fmt"
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	fmt.Println("Sum across groups (any) =", Part1(lines))
	fmt.Println("Sum across groups (every) =", Part2(lines))
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
