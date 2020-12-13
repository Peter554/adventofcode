package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/day12/vector"
	"github.com/peter554/adventofcode/2020/lib"
)

func TestExample(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	instructions := ParseInstructions(lines)

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
