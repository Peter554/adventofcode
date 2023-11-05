package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart1(t *testing.T) {
	sample := []int{0, 3, 6}
	lib.Expect(t, 436, Part1(sample))

	input := []int{1, 0, 16, 5, 17, 4}
	lib.Expect(t, 1294, Part1(input))
}

func TestPart2(t *testing.T) {
	sample := []int{0, 3, 6}
	lib.Expect(t, 175594, Part2(sample))

	input := []int{1, 0, 16, 5, 17, 4}
	lib.Expect(t, 573522, Part2(input))
}
