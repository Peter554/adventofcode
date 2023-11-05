package main

import (
	"sort"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	ids := []int{}
	for _, line := range lines {
		seat := readBoardingPass(line)
		ids = append(ids, seat.id())
	}

	sort.Slice(ids, func(i, j int) bool { return ids[i] < ids[j] })
	return ids[len(ids)-1]
}

func Part2(lines []string) int {
	ids := []int{}
	for _, line := range lines {
		seat := readBoardingPass(line)
		ids = append(ids, seat.id())
	}

	sort.Slice(ids, func(i, j int) bool { return ids[i] < ids[j] })

	for idx, id := range ids {
		if ids[idx+1] != id+1 {
			return id + 1
		}
	}

	panic("not found")
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
	lib.CheckError(err)
	col64, err := strconv.ParseInt(s[7:], 2, 8)
	lib.CheckError(err)
	return seat{int(row64), int(col64)}
}
