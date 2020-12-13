package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lines := lib.ReadInput()
	lib.Expect(t, 242, Part1(lines))
}

func TestPart2(t *testing.T) {
	lines := lib.ReadInput()
	lib.Expect(t, 176035, Part2(lines))
}
