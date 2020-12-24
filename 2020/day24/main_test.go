package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 10, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 254, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 2208, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 3697, Part2(lines))
}
