package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 306, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 33772, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 291, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 35070, Part2(lines))
}
