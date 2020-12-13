package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("input")
	ints := lib.ReadInputAsInts()
	lib.Expect(t, 14360655, Part1(ints))
}

func TestPart2(t *testing.T) {
	lib.UseInput("input")
	ints := lib.ReadInputAsInts()
	lib.Expect(t, 1962331, Part2(ints))
}
