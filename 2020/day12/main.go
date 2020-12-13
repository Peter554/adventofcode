package main

import (
	"fmt"
	"regexp"
	"strconv"

	"github.com/peter554/adventofcode/2020/day12/vector"
	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	instructions := ParseInstructions(lines)

	ship := &Ship{
		Position: vector.New(0, 0),
		Engine:   SimpleEngine(),
	}
	ship.Execute(instructions)

	lib.Result{
		Part:  1,
		Value: ship.Position.Manhattan(),
	}.Print()

	ship = &Ship{
		Position: vector.New(0, 0),
		Engine:   WaypointEngine(10, 1),
	}
	ship.Execute(instructions)

	lib.Result{
		Part:  2,
		Value: ship.Position.Manhattan(),
	}.Print()
}

func ParseInstructions(lines []string) []Instruction {
	o := []Instruction{}
	re := regexp.MustCompile(`^([NSEWLRF])(\d+)$`)
	for _, line := range lines {
		match := re.FindStringSubmatch(line)
		if match == nil {
			panic("Line did not match regex")
		}
		i, err := strconv.Atoi(match[2])
		lib.CheckError(err)
		o = append(o, Instruction{match[1], i})
	}
	return o
}

type Instruction struct {
	Name  string
	Value int
}

type Ship struct {
	Position *vector.Vector
	Engine   map[string]func(s *Ship, value int)
}

func (s *Ship) Execute(instructions []Instruction) *Ship {
	for _, instruction := range instructions {
		s.Engine[instruction.Name](s, instruction.Value)
	}
	return s
}

func SimpleEngine() map[string]func(s *Ship, value int) {
	r := 0
	return map[string]func(s *Ship, value int){
		"N": func(s *Ship, value int) {
			s.Position.Add(0, value)
		},
		"S": func(s *Ship, value int) {
			s.Position.Add(0, -value)
		},
		"E": func(s *Ship, value int) {
			s.Position.Add(value, 0)
		},
		"W": func(s *Ship, value int) {
			s.Position.Add(-value, 0)
		},
		"L": func(s *Ship, value int) {
			if value%90 != 0 {
				panic(fmt.Sprintf("Cannot rotate %d degrees", value))
			}
			r = (r - value/90 + 4) % 4
		},
		"R": func(s *Ship, value int) {
			if value%90 != 0 {
				panic(fmt.Sprintf("Cannot rotate %d degrees", value))
			}
			r = (r + value/90) % 4
		},
		"F": func(s *Ship, value int) {
			v := map[int]*vector.Vector{
				0: vector.New(value, 0),
				1: vector.New(0, -value),
				2: vector.New(-value, 0),
				3: vector.New(0, value),
			}[r]
			s.Position.Add(v.X, v.Y)
		},
	}
}

func WaypointEngine(x, y int) map[string]func(s *Ship, value int) {
	w := vector.New(x, y)
	return map[string]func(s *Ship, value int){
		"N": func(s *Ship, value int) {
			w.Add(0, value)
		},
		"S": func(s *Ship, value int) {
			w.Add(0, -value)
		},
		"E": func(s *Ship, value int) {
			w.Add(value, 0)
		},
		"W": func(s *Ship, value int) {
			w.Add(-value, 0)
		},
		"L": func(s *Ship, value int) {
			if value%90 != 0 {
				panic(fmt.Sprintf("Cannot rotate %d degrees", value))
			}
			for i := 0; i < value/90; i++ {
				w.RotateBy90()
			}
		},
		"R": func(s *Ship, value int) {
			if value%90 != 0 {
				panic(fmt.Sprintf("Cannot rotate %d degrees", value))
			}
			for i := 0; i < (4 - value/90); i++ {
				w.RotateBy90()
			}
		},
		"F": func(s *Ship, value int) {
			v := w.Copy().Multiply(value)
			s.Position.Add(v.X, v.Y)
		},
	}
}
