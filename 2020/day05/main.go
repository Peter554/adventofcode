package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()

	seats := map[seat]bool{}
	maxID := 0
	for _, line := range lines {
		seat := readBoardingPass(line)
		seats[seat] = true
		ID := seat.ID()
		if ID > maxID {
			maxID = ID
		}
	}
	fmt.Println("Max ID =", maxID)
	printSeats(seats)
}

type seat struct {
	Row int
	Col int
}

func readBoardingPass(s string) seat {
	rowS := strings.ReplaceAll(strings.ReplaceAll(s[:7], "F", "0"), "B", "1")
	row64, err := strconv.ParseInt(rowS, 2, 8)
	lib.Check(err)
	colS := strings.ReplaceAll(strings.ReplaceAll(s[7:], "L", "0"), "R", "1")
	col64, err := strconv.ParseInt(colS, 2, 8)
	lib.Check(err)
	return seat{int(row64), int(col64)}
}

func (s seat) ID() int {
	return s.Row*8 + s.Col
}

func printSeats(seats map[seat]bool) {
	s := ""
	for row := 0; row < 256; row++ {
		s += fmt.Sprintf("%d\t", row)
		for col := 0; col < 8; col++ {
			if _, exists := seats[seat{row, col}]; exists {
				s += "#"
			} else {
				s += "."
			}
		}
		s += "\n"
	}
	fmt.Println(s)
}
