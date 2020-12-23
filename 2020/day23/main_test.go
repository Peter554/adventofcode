package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	sample := []int{3, 8, 9, 1, 2, 5, 4, 6, 7}
	lib.Expect(t, "67384529", Part1(sample))

	input := []int{7, 8, 4, 2, 3, 5, 9, 1, 6}
	lib.Expect(t, "53248976", Part1(input))
}

func TestPart2(t *testing.T) {
	sample := []int{3, 8, 9, 1, 2, 5, 4, 6, 7}
	lib.Expect(t, 149245887792, Part2(sample))

	input := []int{7, 8, 4, 2, 3, 5, 9, 1, 6}
	lib.Expect(t, 418819514477, Part2(input))
}
