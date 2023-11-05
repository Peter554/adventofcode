package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample1")
	lines := lib.ReadInput()
	lib.Expect(t, 71, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 25916, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample2")
	lines := lib.ReadInput()
	lib.Expect(t, 156, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 2564529489989, Part2(lines))
}
