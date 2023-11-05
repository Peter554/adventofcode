package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 336, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 2122848000, Part2(lines))
}
