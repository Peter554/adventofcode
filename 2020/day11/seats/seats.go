package seats

type point struct {
	x int
	y int
}

type Seats struct {
	occupation   map[point]bool
	xmax         int
	ymax         int
	visionDepth  int
	squashFactor int
	neighbours   map[point][]point
}

func New(lines []string, visionDepth int, squashFactor int) *Seats {
	occupation := map[point]bool{}
	xmax, ymax := 0, 0
	for y, line := range lines {
		ymax = y
		for x, char := range line {
			xmax = x
			if char == 'L' {
				occupation[point{x, y}] = false
			}
		}
	}

	if visionDepth == -1 {
		visionDepth = xmax * ymax
	}

	seats := &Seats{
		occupation:   occupation,
		xmax:         xmax,
		ymax:         ymax,
		visionDepth:  visionDepth,
		squashFactor: squashFactor,
	}

	seats.constructNeighbours()

	return seats
}

func (s *Seats) Evolve() *Seats {
	for {
		didChange := s.evolveOnce()
		if !didChange {
			return s
		}
	}
}

func (s *Seats) CountOccupied() int {
	o := 0
	for _, v := range s.occupation {
		if v {
			o++
		}
	}
	return o
}

func (s *Seats) evolveOnce() (didChange bool) {
	didChange = false
	nextOccupation := map[point]bool{}

	for seat, occupied := range s.occupation {
		visibleOccupation := s.visibleOccupation(seat)
		if !occupied && visibleOccupation == 0 {
			nextOccupation[seat] = true
			didChange = true
		} else if occupied && visibleOccupation >= s.squashFactor {
			nextOccupation[seat] = false
			didChange = true
		} else {
			nextOccupation[seat] = occupied
		}
	}

	s.occupation = nextOccupation
	return didChange
}

func (s *Seats) constructNeighbours() {
	s.neighbours = map[point][]point{}
	for seat := range s.occupation {
		for _, direction := range []point{
			point{1, 1},
			point{0, 1},
			point{1, 0},
			point{-1, -1},
			point{0, -1},
			point{-1, 0},
			point{-1, 1},
			point{1, -1},
		} {
			for depth := 1; depth <= s.visionDepth; depth++ {
				x := seat.x + direction.x*depth
				y := seat.y + direction.y*depth
				if x < 0 || x > s.xmax || y < 0 || y > s.ymax {
					break
				}
				if _, exists := s.occupation[point{x, y}]; exists {
					if _, exists := s.neighbours[seat]; exists {
						s.neighbours[seat] = append(s.neighbours[seat], point{x, y})
					} else {
						s.neighbours[seat] = []point{point{x, y}}
					}
					break
				}
			}
		}
	}
}

func (s *Seats) visibleOccupation(seat point) int {
	count := 0
	for _, neighbour := range s.neighbours[seat] {
		if occupied := s.occupation[neighbour]; occupied {
			count++
		}
	}
	return count

}
