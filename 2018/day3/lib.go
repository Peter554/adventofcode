package main

import (
	"errors"
	"regexp"
	"strconv"
)

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

func getClaim(line string) (claim, error) {
	r, _ := regexp.Compile("#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)")

	matches := r.FindStringSubmatch(line)

	if matches == nil {
		return claim{}, errors.New("Claim not found")
	}

	id, _ := strconv.Atoi(matches[1])
	left, _ := strconv.Atoi(matches[2])
	top, _ := strconv.Atoi(matches[3])
	width, _ := strconv.Atoi(matches[4])
	height, _ := strconv.Atoi(matches[5])

	c := claim{id, coordinate{left, top}, width, height}

	return c, nil
}

func addClaimToMap(m map[coordinate]int, c claim) {
	x := c.topleft.x
	y := c.topleft.y

	for i := 0; i < c.width; i++ {
		for j := 0; j < c.height; j++ {
			m[coordinate{x + i, y + j}]++
		}
	}
}

func getNumberOfCoordinatesInTwoOrMoreClaims(m map[coordinate]int) int {
	count := 0

	for _, v := range m {
		if v >= 2 {
			count++
		}
	}

	return count
}

func (this claim) overlaps(other claim) bool {
	m := make(map[coordinate]int)

	addClaimToMap(m, this)
	addClaimToMap(m, other)

	if getNumberOfCoordinatesInTwoOrMoreClaims(m) > 0 {
		return true
	}

	return false
}
