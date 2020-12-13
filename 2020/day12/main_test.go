package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/day12/vector"
	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
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

	lib.UseInput("input")
	lines = lib.ReadInput()
	instructions = ParseInstructions(lines)

	lib.Expect(
		t,
		508,
		(&Ship{
			Position: vector.New(0, 0),
			Engine:   SimpleEngine(),
		}).Execute(instructions).Position.Manhattan())
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	instructions := ParseInstructions(lines)

	lib.Expect(
		t,
		286,
		(&Ship{
			Position: vector.New(0, 0),
			Engine:   WaypointEngine(10, 1),
		}).Execute(instructions).Position.Manhattan())

	lib.UseInput("input")
	lines = lib.ReadInput()
	instructions = ParseInstructions(lines)

	lib.Expect(
		t,
		30761,
		(&Ship{
			Position: vector.New(0, 0),
			Engine:   WaypointEngine(10, 1),
		}).Execute(instructions).Position.Manhattan())
}
