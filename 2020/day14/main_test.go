package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample1")
	lines := lib.ReadInput()
	lib.Expect(t, 165, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 14862056079561, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample2")
	lines := lib.ReadInput()
	lib.Expect(t, 208, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 3296185383161, Part2(lines))
}

func Test_getFloatMasks(t *testing.T) {
	masks := getFloatMasks("1X0X")
	lib.Expect(t, masks[0], 0)
	lib.Expect(t, masks[1], 1)
	lib.Expect(t, masks[2], 4)
	lib.Expect(t, masks[3], 5)
}
