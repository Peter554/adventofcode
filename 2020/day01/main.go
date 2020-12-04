package main

import (
	"fmt"
	"strconv"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()

	ints := []int{}
	for _, line := range lines {
		i, err := strconv.Atoi(line)
		lib.Check(err)
		ints = append(ints, i)
	}

	for i := 0; i < len(ints); i++ {
		for j := 0; j < len(ints); j++ {
			for k := 0; k < len(ints); k++ {
				if i == j || i == k || j == k {
					continue
				}
				if (ints[i] + ints[j] + ints[k]) == 2020 {
					fmt.Println(ints[i], ints[j], ints[k], ints[i]*ints[j]*ints[k])
					return
				}
			}
		}
	}
}
