package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart1(t *testing.T) {
	lines := lib.ReadInput()
	lib.Expect(t, 813, Part1(lines))
}

func TestPart2(t *testing.T) {
	lines := lib.ReadInput()
	lib.Expect(t, 612, Part2(lines))
}
