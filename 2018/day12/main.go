package main

import (
	"fmt"

	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	lines := common.Readlines("./input.txt")

	stateString := lines[0][15:]
	state := newIntSet()
	for i, r := range stateString {
		if string(r) == "#" {
			state.Add(i)
		}
	}

	rules := make(map[string]bool)
	for _, line := range lines[2:] {
		pattern := line[:5]
		produces := string(line[9])
		if produces == "#" {
			rules[pattern] = true
		} else {
			rules[pattern] = false
		}
	}

	gMax := 1000000
	logAt := 10000
	for g := 0; g < gMax; g++ {
		if g%logAt == 0 {
			percentDone := (float64(g) / float64(gMax) * 100)
			fmt.Printf("g = %d\n", g)
			fmt.Printf("%f percent done\n", percentDone)
			fmt.Printf("sum is %d\n\n", state.Sum())
		}
		nextState := newIntSet()
		for _, v := range state.Values() {
			for i := v - 2; i <= v+2; i++ {
				pattern := ""
				for j := i - 2; j <= i+2; j++ {
					if state.Contains(j) {
						pattern += "#"
					} else {
						pattern += "."
					}
				}
				if rules[pattern] {
					nextState.Add(i)
				}
			}
		}
		state = nextState
	}

	fmt.Println(state.Sum())
}

type IntSet interface {
	Add(i int)
	Contains(i int) bool
	Min() int
	Max() int
	Sum() int
	Values() []int
}

func newIntSet() IntSet {
	return &intSet{data: make(map[int]bool)}
}

type intSet struct {
	data map[int]bool
}

func (s *intSet) Add(i int) {
	s.data[i] = true
}

func (s *intSet) Contains(i int) bool {
	exists := s.data[i]
	return exists
}

func (s *intSet) Min() int {
	o := 0
	first := true
	for k, _ := range s.data {
		if first || k < o {
			o = k
			first = false
		}
	}
	return o
}

func (s *intSet) Max() int {
	o := 0
	first := true
	for k, _ := range s.data {
		if first || k > o {
			o = k
			first = false
		}
	}
	return o
}

func (s *intSet) Sum() int {
	o := 0
	for k, _ := range s.data {
		o += k
	}
	return o
}

func (s *intSet) Values() []int {
	o := make([]int, 0)
	for k, _ := range s.data {
		o = append(o, k)
	}
	return o
}
