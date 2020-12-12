package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/day12/vector"
	"github.com/peter554/adventofcode/2020/lib"
)

func TestExample(t *testing.T) {
	lines := lib.TestLines(`
F10
N3
F7
R90
F11`)

	instructions := parseInstructions(lines)

	lib.Expect(
		t,
		25,
		(&Ship{
			Position: vector.New(0, 0),
			Engine:   SimpleEngine(),
		}).Execute(instructions).Position.Manhattan())

	lib.Expect(
		t,
		286,
		(&Ship{
			Position: vector.New(0, 0),
			Engine:   WaypointEngine(10, 1),
		}).Execute(instructions).Position.Manhattan())
}
