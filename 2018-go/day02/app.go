package main

import (
	"fmt"

	"github.com/peter554/adventofcode/2018-go/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	fmt.Println("Part 1")
	fmt.Printf("Checksum = %d\n", getchecksum(lines))
	fmt.Println("Part 2")
	fmt.Printf("Boxes = %s\n", findboxes(lines))
}

func getchecksum(lines []string) int {
	a := 0
	b := 0
	for _, v := range lines {
		runes := countrunes(v)
		if somevalueequals(runes, 2) {
			a++
		}
		if somevalueequals(runes, 3) {
			b++
		}
	}
	return a * b
}

func countrunes(s string) map[rune]int {
	countmap := make(map[rune]int)
	for _, r := range s {
		if _, found := countmap[r]; found {
			countmap[r]++
		} else {
			countmap[r] = 1
		}
	}
	return countmap
}

func somevalueequals(m map[rune]int, n int) bool {
	for _, v := range m {
		if v == n {
			return true
		}
	}
	return false
}

func findboxes(lines []string) string {
	for _, l1 := range lines {
		for _, l2 := range lines {
			if computedifference(l1, l2) == 1 {
				return fmt.Sprintf("%s %s", l1, l2)
			}
		}
	}
	return ""
}

func computedifference(s1 string, s2 string) int {
	out := 0
	for idx, r := range s1 {
		if r != []rune(s2)[idx] {
			out++
		}
	}
	return out
}
