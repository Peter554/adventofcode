package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 11, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 6683, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 6, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 3122, Part2(lines))
}
