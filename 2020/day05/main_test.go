package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func Test_readBoardingPass(t *testing.T) {
	cases := []struct {
		s  string
		id int
	}{
		{"FBFBBFFRLR", 357},
		{"BFFFBBFRRR", 567},
		{"FFFBBBFRRR", 119},
		{"BBFFBBFRLL", 820},
	}

	for _, c := range cases {
		seat := readBoardingPass(c.s)
		lib.Expect(t, c.id, seat.id())
	}
}
