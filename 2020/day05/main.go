package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()

	ids := []int{}
	for _, line := range lines {
		seat := readBoardingPass(line)
		ids = append(ids, seat.id())
	}

	sort.Slice(ids, func(i, j int) bool { return ids[i] < ids[j] })
	fmt.Println("Max ID =", ids[len(ids)-1])

	for idx, id := range ids {
		if ids[idx+1] != id+1 {
			fmt.Println("My ID =", id+1)
			return
		}
	}
}

type seat struct {
	row int
	col int
}

func (s seat) id() int {
	return s.row*8 + s.col
}

func readBoardingPass(s string) seat {
	s = strings.NewReplacer("F", "0", "B", "1", "L", "0", "R", "1").Replace(s)
	row64, err := strconv.ParseInt(s[:7], 2, 8)
	lib.Check(err)
	col64, err := strconv.ParseInt(s[7:], 2, 8)
	lib.Check(err)
	return seat{int(row64), int(col64)}
}
