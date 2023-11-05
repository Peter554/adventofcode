package main

import (
	"github.com/peter554/adventofcode/2020/go/lib"
)

func main() {
	ints := lib.ReadInputAsInts()

	lib.Result{Part: 1, Value: Part1(ints)}.Print()
	lib.Result{Part: 2, Value: Part2(ints)}.Print()
}

func Part1(ints []int) int {
	for i := 0; i < len(ints); i++ {
		for j := 0; j < len(ints); j++ {
			if i == j {
				continue
			}
			if (ints[i] + ints[j]) == 2020 {
				return ints[i] * ints[j]
			}
		}
	}
	panic("not found")
}

func Part2(ints []int) int {
	for i := 0; i < len(ints); i++ {
		for j := 0; j < len(ints); j++ {
			for k := 0; k < len(ints); k++ {
				if i == j || i == k || j == k {
					continue
				}
				if (ints[i] + ints[j] + ints[k]) == 2020 {
					return ints[i] * ints[j] * ints[k]
				}
			}
		}
	}
	panic("not found")
}
