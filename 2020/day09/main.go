package main

import (
	"fmt"
	"strconv"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	ints := asInts(lines)

	invalidNumber := firstInvalidNumber(ints)
	fmt.Println("Part 1 =", invalidNumber)

	block := findContiguousBlock(ints, invalidNumber)
	min, max := minMaxInts(block)
	fmt.Println("Part 2 =", min+max)
}

func asInts(lines []string) []int {
	ints := []int{}
	for _, line := range lines {
		i, err := strconv.Atoi(line)
		lib.Check(err)
		ints = append(ints, i)
	}
	return ints
}

func firstInvalidNumber(ints []int) int {
	for idx := 25; idx < len(ints); idx++ {
		i := ints[idx]
		valid := false

		m := map[int]int{}
		for _, j := range ints[idx-25 : idx] {
			if _, exists := m[j]; exists {
				m[j]++
			} else {
				m[j] = 1
			}
		}

		for k, v := range m {
			if k*2 == i && v >= 2 {
				valid = true
			}
			if _, exists := m[i-k]; exists {
				valid = true
			}
		}

		if !valid {
			return i
		}
	}
	panic("Invalid number not found")
}

func findContiguousBlock(ints []int, sum int) []int {
	i, j := 0, 1
	for {
		block := ints[i:j]
		blockSum := sumInts(block)
		if blockSum == sum {
			return block
		} else if blockSum < sum {
			j++
		} else {
			i++
		}
		if j == i {
			j++
		}
		if j >= len(ints) {
			panic("Contiguous block not found")
		}
	}
}

func sumInts(ints []int) int {
	o := 0
	for _, i := range ints {
		o += i
	}
	return o
}

func minMaxInts(ints []int) (min, max int) {
	min, max = ints[0], ints[0]
	for _, i := range ints {
		if i < min {
			min = i
		}
		if i > max {
			max = i
		}
	}
	return
}
