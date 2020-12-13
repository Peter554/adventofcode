package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	ints := lib.ReadInputAsInts()
	lib.Expect(t, 514579, Part1(ints))

	lib.UseInput("input")
	ints = lib.ReadInputAsInts()
	lib.Expect(t, 494475, Part1(ints))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	ints := lib.ReadInputAsInts()
	lib.Expect(t, 241861950, Part2(ints))

	lib.UseInput("input")
	ints = lib.ReadInputAsInts()
	lib.Expect(t, 267520550, Part2(ints))
}
