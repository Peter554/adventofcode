package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 2, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 546, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 1, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 275, Part2(lines))
}
