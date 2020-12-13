package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("input")
	lines := lib.ReadInput()
	lib.Expect(t, 1475, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("input")
	lines := lib.ReadInput()
	lib.Expect(t, 1270, Part2(lines))
}
