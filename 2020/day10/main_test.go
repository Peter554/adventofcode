package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	ints := lib.ReadInputAsInts()
	lib.Expect(t, 220, Part1(ints))

	lib.UseInput("input")
	ints = lib.ReadInputAsInts()
	lib.Expect(t, 2040, Part1(ints))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	ints := lib.ReadInputAsInts()
	lib.Expect(t, 19208, Part2(ints))

	lib.UseInput("input")
	ints = lib.ReadInputAsInts()
	lib.Expect(t, 28346956187648, Part2(ints))
}
