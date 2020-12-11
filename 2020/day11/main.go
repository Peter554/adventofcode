package main

import (
	"github.com/peter554/adventofcode/2020/day11/seats"
	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()

	lib.PrintResultAndAssert(
		1,
		seats.New(lines, 1, 4).Evolve().CountOccupied(),
		2359)

	lib.PrintResultAndAssert(
		2,
		seats.New(lines, -1, 5).Evolve().CountOccupied(),
		2131)
}
