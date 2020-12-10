package main

import (
	"sort"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	ints := lib.ReadInputAsInts()
	ints = append(ints, 0, maxInt(ints)+3)
	sort.Slice(ints, func(i, j int) bool { return ints[i] < ints[j] })
	lib.PrintResultAndAssert(1, part1(ints), 2040)
	lib.PrintResultAndAssert(2, part2(ints), 28346956187648)
}

func part1(ints []int) int {
	m := map[int]int{}
	for idx := 1; idx < len(ints); idx++ {
		diff := ints[idx] - ints[idx-1]
		if _, exists := m[diff]; exists {
			m[diff]++
		} else {
			m[diff] = 1
		}
	}
	return m[1] * m[3]
}

func part2(ints []int) int {
	memo := map[int]int{}

	var f func(startFrom int) int
	f = func(startFrom int) int {
		if value, exists := memo[startFrom]; exists {
			return value
		}

		subInts := ints[startFrom:]

		if len(subInts) <= 1 {
			return 1
		}

		first := subInts[0]
		withinThree := findIdxs(subInts, func(i int) bool {
			return i > first && i <= first+3
		})

		count := 0
		for _, idx := range withinThree {
			count += f(startFrom + idx)
		}
		memo[startFrom] = count
		return count
	}

	return f(0)
}

func maxInt(ints []int) (max int) {
	max = ints[0]
	for _, i := range ints[1:] {
		if i > max {
			max = i
		}
	}
	return
}

func findIdxs(ints []int, match func(i int) bool) []int {
	idxs := []int{}
	for idx, i := range ints {
		if match(i) {
			idxs = append(idxs, idx)
		}
	}
	return idxs
}
