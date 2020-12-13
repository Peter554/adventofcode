package main

import (
	"github.com/peter554/adventofcode/2020/day11/seats"
	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()

	lib.Result{
		Part:  1,
		Value: Part1(lines),
	}.Print()

	lib.Result{
		Part:  2,
		Value: Part2(lines),
	}.Print()

}

func Part1(lines []string) int {
	return seats.New(lines, 1, 4).Evolve().CountOccupied()
}
func Part2(lines []string) int {
	return seats.New(lines, -1, 5).Evolve().CountOccupied()
}
