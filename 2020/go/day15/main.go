package main

import (
	"github.com/peter554/adventofcode/2020/go/lib"
)

var INPUT = []int{1, 0, 16, 5, 17, 4}

func main() {
	lib.Result{Part: 1, Value: Part1(INPUT)}.Print()
	lib.Result{Part: 2, Value: Part2(INPUT)}.Print()
}

func Part1(ints []int) int {
	return playGame(ints, 2020)
}

func Part2(ints []int) int {
	return playGame(ints, 30000000)
}

func playGame(ints []int, tmax int) int {
	t := 0
	var mostRecent int
	m := map[int][]int{}

	for _, i := range ints {
		t++

		mostRecent = i

		if _, exists := m[mostRecent]; exists {
			m[mostRecent][0] = m[mostRecent][1]
			m[mostRecent][1] = t
		} else {
			m[mostRecent] = []int{-1, t}
		}
	}

	for {
		t++

		var next int
		ts := m[mostRecent]
		if ts[0] == -1 {
			next = 0
		} else {
			next = ts[1] - ts[0]
		}

		mostRecent = next

		if _, exists := m[mostRecent]; exists {
			m[mostRecent][0] = m[mostRecent][1]
			m[mostRecent][1] = t
		} else {
			m[mostRecent] = []int{-1, t}
		}

		if t == tmax {
			return next
		}
	}
}
