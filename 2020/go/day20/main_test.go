package main

import (
	"strings"
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 20899048083289, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 17250897231301, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 273, Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 1576, Part2(lines))
}

func Test_buildPuzzle(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	cornerCheckSum, puzzle := buildPuzzle(lines)

	lib.Expect(t, 20899048083289, cornerCheckSum)

	puzzle = rotate(rotate(rotate(puzzle)))
	lib.UseInput("sample.built")
	if strings.Join(lib.ReadInput(), "\n") != strings.Join(puzzle, "\n") {
		t.Error("Puzzle did not match")
	}
}

func Test_countSeaMonsters(t *testing.T) {
	lib.UseInput("sample.built")
	puzzle := lib.ReadInput()
	lib.Expect(t, 2, countSeaMonsters(puzzle))
}
