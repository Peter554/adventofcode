package main

import "github.com/peter554/adventofcode/2020/go/lib"

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	return simulate(lines, 3)
}

func Part2(lines []string) int {
	return simulate(lines, 4)
}

func simulate(lines []string, d int) int {
	ps := NewPointSet()
	for y, line := range lines {
		for x, char := range line {
			if char == '#' {
				ps.Add(Point{x, y, 0, 0})
			}
		}
	}

	for i := 0; i < 6; i++ {
		nextPs := NewPointSet()

		pointsToConsider := ps.Copy()
		for _, p := range ps.ToSlice() {
			pointsToConsider.AddMany(p.Neighbors(d))
		}

		for _, p := range pointsToConsider.ToSlice() {
			currentlyActive := ps.Contains(p)

			count := 0
			for _, n := range p.Neighbors(d) {
				if ps.Contains(n) {
					count++
				}
			}

			if currentlyActive {
				if count == 2 || count == 3 {
					nextPs.Add(p)
				}
			} else {
				if count == 3 {
					nextPs.Add(p)
				}
			}
		}

		ps = nextPs
	}

	return ps.Size()
}

type Point struct {
	X, Y, Z, W int
}

func (p Point) Neighbors(d int) []Point {
	o := []Point{}
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			for dz := -1; dz <= 1; dz++ {
				for dw := -(d - 3); dw <= d-3; dw++ {
					if dx == 0 && dy == 0 && dz == 0 && dw == 0 {
						continue
					}
					o = append(o, Point{p.X + dx, p.Y + dy, p.Z + dz, p.W + dw})
				}
			}
		}
	}
	return o
}

type PointSet struct {
	m map[Point]bool
}

func NewPointSet() *PointSet {
	return &PointSet{map[Point]bool{}}
}

func (ps *PointSet) Add(p Point) {
	ps.m[p] = true
}

func (ps *PointSet) AddMany(p []Point) {
	for _, p1 := range p {
		ps.Add(p1)
	}
}

func (ps *PointSet) Remove(p Point) {
	delete(ps.m, p)
}

func (ps *PointSet) Contains(p Point) bool {
	_, exists := ps.m[p]
	return exists
}

func (ps *PointSet) Copy() *PointSet {
	m := map[Point]bool{}
	for p := range ps.m {
		m[p] = true
	}
	return &PointSet{m}
}

func (ps *PointSet) Size() int {
	return len(ps.m)
}

func (ps *PointSet) ToSlice() []Point {
	o := []Point{}
	for p := range ps.m {
		o = append(o, Point{p.X, p.Y, p.Z, p.W})
	}
	return o
}
