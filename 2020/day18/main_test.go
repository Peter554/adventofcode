package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("input")
	lines := lib.ReadInput()
	lib.Expect(t, 510009915468, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("input")
	lines := lib.ReadInput()
	lib.Expect(t, 321176691637769, Part2(lines))
}

func TestEvaluate(t *testing.T) {
	lib.Expect(t, 71, Evaluate("1 + 2 * 3 + 4 * 5 + 6"))
	lib.Expect(t, 26, Evaluate("2 * 3 + (4 * 5)"))
	lib.Expect(t, 51, Evaluate("1 + (2 * 3) + (4 * (5 + 6))"))
}

func TestEvaluateAdvanced(t *testing.T) {
	lib.Expect(t, 112, EvaluateAdvanced("7 * 8 * 2"))
	lib.Expect(t, 231, EvaluateAdvanced("1 + 2 * 3 + 4 * 5 + 6"))
	lib.Expect(t, 46, EvaluateAdvanced("2 * 3 + (4 * 5)"))
	lib.Expect(t, 51, EvaluateAdvanced("1 + (2 * 3) + (4 * (5 + 6))"))
}
