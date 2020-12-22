package main

import (
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	p1, p2 := parseInput(lines)

	for len(p1) > 0 && len(p2) > 0 {
		i1, i2 := p1[0], p2[0]
		p1, p2 = p1[1:], p2[1:]
		if i1 > i2 {
			p1 = append(p1, i1, i2)
		} else {
			p2 = append(p2, i2, i1)
		}
	}

	var winningP []int
	if len(p1) == 0 {
		winningP = p2
	} else {
		winningP = p1
	}

	count := 0
	for idx, i := range winningP {
		count += i * (len(winningP) - idx)
	}
	return count
}

func Part2(lines []string) int {
	p1, p2 := parseInput(lines)

	_, winningNumbers := playRecursiveCombat(p1, p2)

	count := 0
	for idx, i := range winningNumbers {
		count += i * (len(winningNumbers) - idx)
	}
	return count
}

func parseInput(lines []string) (p1, p2 []int) {
	p1, p2 = []int{}, []int{}
	for idx, line := range strings.Split(strings.Split(strings.Join(lines, "\n"), "\n\n")[0], "\n") {
		if idx == 0 {
			continue
		}
		p1 = append(p1, lib.AsInt(line))
	}
	for idx, line := range strings.Split(strings.Split(strings.Join(lines, "\n"), "\n\n")[1], "\n") {
		if idx == 0 {
			continue
		}
		p2 = append(p2, lib.AsInt(line))
	}
	return
}

func playRecursiveCombat(p1, p2 []int) (winner int, winningNumbers []int) {
	history := [][][]int{}

	for len(p1) > 0 && len(p2) > 0 {
		for _, state := range history {
			if equal(state[0], p1) && equal(state[1], p2) {
				winner = 1
				winningNumbers = p1
				return
			}
		}

		history = append(history, [][]int{
			copy(p1),
			copy(p2),
		})

		i1, i2 := p1[0], p2[0]
		p1, p2 = p1[1:], p2[1:]

		var roundWinner int
		if len(p1) >= i1 && len(p2) >= i2 {
			roundWinner, _ = playRecursiveCombat(copy(p1[:i1]), copy(p2[:i2]))
		} else {
			if i1 > i2 {
				roundWinner = 1
			} else {
				roundWinner = 2
			}
		}

		if roundWinner == 1 {
			p1 = append(p1, i1, i2)
		} else {
			p2 = append(p2, i2, i1)
		}
	}

	if len(p1) == 0 {
		winner = 2
		winningNumbers = p2
	} else {
		winner = 1
		winningNumbers = p1
	}

	return
}

func copy(is []int) []int {
	o := []int{}
	for _, i := range is {
		o = append(o, i)
	}
	return o
}

func equal(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for idx, v := range a {
		if v != b[idx] {
			return false
		}
	}
	return true
}
