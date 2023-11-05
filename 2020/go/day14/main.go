package main

import (
	"sort"
	"strings"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	memory := map[int]int{}
	maskOne := 0
	maskNoChange := 0

	for _, line := range lines {
		if lib.RE(`^mask`).Test(line) {
			groups := lib.RE(`^mask = ([01X]+)$`).Groups(line)
			maskOne = lib.ParseInt(strings.NewReplacer("X", "0").Replace(groups[0]), 2)
			maskNoChange = lib.ParseInt(strings.NewReplacer("1", "0", "X", "1").Replace(groups[0]), 2)
		} else {
			groups := lib.RE(`^mem\[(\d+)\] = (\d+)$`).Groups(line)
			k, v := lib.AsInt(groups[0]), lib.AsInt(groups[1])
			v = maskOne | (maskNoChange & v)
			memory[k] = v
		}
	}

	o := 0
	for _, v := range memory {
		o += v
	}
	return o
}

func Part2(lines []string) int {
	memory := map[int]int{}
	maskOne := 0
	maskNoChange := 0
	masksFloating := []int{}

	for _, line := range lines {
		if lib.RE(`^mask`).Test(line) {
			groups := lib.RE(`^mask = ([01X]+)$`).Groups(line)
			maskOne = lib.ParseInt(strings.NewReplacer("X", "0").Replace(groups[0]), 2)
			maskNoChange = lib.ParseInt(strings.NewReplacer("X", "0", "1", "0", "0", "1").Replace(groups[0]), 2)
			masksFloating = getFloatMasks(groups[0])
		} else {
			groups := lib.RE(`^mem\[(\d+)\] = (\d+)$`).Groups(line)
			k, v := lib.AsInt(groups[0]), lib.AsInt(groups[1])
			for _, floatMask := range masksFloating {
				k = maskOne | (maskNoChange & k) | floatMask
				memory[k] = v
			}
		}
	}

	o := 0
	for _, v := range memory {
		o += v
	}
	return o
}

// 1X0X => [0000, 0001, 0100, 0101] => [0, 1, 4, 5]
func getFloatMasks(s string) []int {
	a := []int{}
	for idx, char := range s {
		if char == 'X' {
			a = append(a, 1<<(len(s)-idx-1))
		}
	}

	b := []int{0}
	for _, i := range a {
		for _, j := range b {
			b = append(b, i|j)
		}
	}

	sort.IntSlice(b).Sort()
	return b
}
