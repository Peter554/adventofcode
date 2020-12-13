package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 295, Part1(lines))
	lib.Expect(t, 1068781, Part2(lines))
}
