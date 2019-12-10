package main

import (
	"fmt"
	"strconv"

	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	frequencies := toInts(lines)
	fmt.Println("Part 1")
	fmt.Printf("Sum = %d\n", sum(frequencies))
	fmt.Println("Part 2")
	fmt.Printf("First repeating sum = %d\n", firstRepeatingSum(frequencies))

}

func toInts(lines []string) []int {
	out := make([]int, 0)
	for _, line := range lines {
		i, _ := strconv.Atoi(line)
		out = append(out, i)
	}
	return out
}

func sum(ints []int) int {
	total := 0
	for _, v := range ints {
		total += v
	}
	return total
}

func contains(ints []int, i int) bool {
	for _, v := range ints {
		if v == i {
			return true
		}
	}
	return false
}

func firstRepeatingSum(ints []int) int {
	sums := make([]int, 1)
	for {
		for _, v := range ints {
			next := sums[len(sums)-1] + v
			if contains(sums, next) {
				return next
			}
			sums = append(sums, next)
		}
	}
}
