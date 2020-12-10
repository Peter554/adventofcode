package main

import (
	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	ints := lib.ReadInputAsInts()
	for i := 0; i < len(ints); i++ {
		for j := 0; j < len(ints); j++ {
			for k := 0; k < len(ints); k++ {
				if i == j || i == k || j == k {
					continue
				}
				if (ints[i] + ints[j] + ints[k]) == 2020 {
					lib.PrintResultAndAssert(2, ints[i]*ints[j]*ints[k], 267520550)
					return
				}
			}
		}
	}
}
