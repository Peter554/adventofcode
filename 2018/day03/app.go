package main

import (
	"fmt"
	"regexp"
	"strconv"

	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	claims := buildclaims(lines)
	mp := buildmap(claims)
	fmt.Println("Part 1")
	fmt.Printf("Count = %d\n", countvalueswhere(mp, func(i int) bool { return i >= 2 }))
	fmt.Println("Part 2")
	fmt.Printf("Id = %d\n", findlonelyclaim(claims).id)
}

type coordinate struct {
	x int
	y int
}

type claim struct {
	id      int
	topleft coordinate
	width   int
	height  int
}

func buildclaims(lines []string) []claim {
	out := make([]claim, 0)
	for _, l := range lines {
		out = append(out, getclaim(l))
	}
	return out
}

func getclaim(line string) claim {
	r, _ := regexp.Compile(`#(\d+) @ (\d+),(\d+): (\d+)x(\d+)`)
	matches := r.FindStringSubmatch(line)
	id, _ := strconv.Atoi(matches[1])
	left, _ := strconv.Atoi(matches[2])
	top, _ := strconv.Atoi(matches[3])
	width, _ := strconv.Atoi(matches[4])
	height, _ := strconv.Atoi(matches[5])
	return claim{id, coordinate{left, top}, width, height}
}

func buildmap(claims []claim) map[coordinate]int {
	m := make(map[coordinate]int)
	for _, c := range claims {
		c.addtomap(m)
	}
	return m
}

func (c claim) addtomap(m map[coordinate]int) {
	x := c.topleft.x
	y := c.topleft.y
	for i := 0; i < c.width; i++ {
		for j := 0; j < c.height; j++ {
			if _, found := m[coordinate{x + i, y + j}]; found {
				m[coordinate{x + i, y + j}]++
			} else {
				m[coordinate{x + i, y + j}] = 1
			}
		}
	}
}

type intcondition func(int) bool

func countvalueswhere(m map[coordinate]int, condition intcondition) int {
	out := 0
	for _, v := range m {
		if condition(v) {
			out++
		}
	}
	return out
}

func findlonelyclaim(claims []claim) claim {
	for _, c1 := range claims {
		overlaps := 0
		for _, c2 := range claims {
			if c1 == c2 {
				continue
			}
			if c1.overlaps(c2) {
				overlaps++
				break
			}
		}
		if overlaps == 0 {
			return c1
		}
	}
	return claim{}
}

func (c claim) overlaps(other claim) bool {
	claims := []claim{c, other}
	mp := buildmap(claims)
	return countvalueswhere(mp, func(i int) bool { return i >= 2 }) > 0
}
