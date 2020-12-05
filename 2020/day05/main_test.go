package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func Test_readBoardingPass(t *testing.T) {
	cases := []struct {
		s   string
		row int
		col int
	}{
		{"FBFBBFFRLR", 44, 5},
		{"BFFFBBFRRR", 70, 7},
		{"FFFBBBFRRR", 14, 7},
		{"BBFFBBFRLL", 102, 4},
	}

	for _, c := range cases {
		seat := readBoardingPass(c.s)
		lib.Expect(t, c.row, seat.Row)
		lib.Expect(t, c.col, seat.Col)
	}
}
