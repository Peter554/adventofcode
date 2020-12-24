package main

import (
	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	m := initialize(lines)
	return len(m)
}

func Part2(lines []string) int {
	m := initialize(lines)

	for i := 0; i < 100; i++ {
		nextM := map[Point]bool{}

		possibilities := []Point{}
		for p := range m {
			possibilities = append(possibilities, p.Neighbours()...)
		}

		for _, p := range possibilities {
			count := 0
			for _, neighbour := range p.Neighbours() {
				if _, exists := m[neighbour]; exists {
					count++
				}
			}

			if _, exists := m[p]; exists {
				if count == 1 || count == 2 {
					nextM[p] = true
				}
			} else {
				if count == 2 {
					nextM[p] = true
				}
			}
		}

		m = nextM
	}

	return len(m)
}

type Point struct {
	X, Y int
}

func (p Point) Neighbours() []Point {
	return []Point{
		Point{p.X + 2, p.Y},
		Point{p.X - 2, p.Y},
		Point{p.X + 1, p.Y + 1},
		Point{p.X + 1, p.Y - 1},
		Point{p.X - 1, p.Y + 1},
		Point{p.X - 1, p.Y - 1},
	}
}

func initialize(lines []string) map[Point]bool {
	m := map[Point]bool{}

	for _, line := range lines {
		var X, Y int
		var buffer rune = 0
		for _, char := range line {
			switch char {
			case 'n':
				buffer = 'n'
			case 's':
				buffer = 's'
			case 'e':
				if buffer == 0 {
					X += 2
				} else if buffer == 'n' {
					X++
					Y++
				} else {
					X++
					Y--
				}
				buffer = 0

			case 'w':
				if buffer == 0 {
					X -= 2
				} else if buffer == 'n' {
					X--
					Y++
				} else {
					X--
					Y--
				}
				buffer = 0
			}

		}
		p := Point{X, Y}
		if _, exists := m[p]; exists {
			delete(m, p)
		} else {
			m[p] = true
		}
	}

	return m
}
