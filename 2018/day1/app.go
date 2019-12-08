package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	data := readFile("./input.txt")
	frequencies := data.toInts()
	fmt.Println("Part 1")
	fmt.Printf("Sum = %d\n", frequencies.sum())
	fmt.Println("Part 2")
	fmt.Printf("First repeating sum = %d\n", frequencies.firstRepeatingSum())

}

type lines []string
type ints []int

func readFile(location string) lines {
	file, _ := os.Open(location)
	scanner := bufio.NewScanner(file)
	out := make(lines, 0)
	for scanner.Scan() {
		out = append(out, scanner.Text())
	}
	return out
}

func (o lines) toInts() ints {
	out := make(ints, 0)
	for _, line := range o {
		i, _ := strconv.Atoi(line)
		out = append(out, i)
	}
	return out
}

func (o ints) sum() int {
	total := 0
	for _, v := range o {
		total += v
	}
	return total
}

func (o ints) contains(i int) bool {
	for _, v := range o {
		if v == i {
			return true
		}
	}
	return false
}

func (o ints) firstRepeatingSum() int {
	sums := make(ints, 1)
	for {
		for _, v := range o {
			next := sums[len(sums)-1] + v
			if sums.contains(next) {
				return next
			}
			sums = append(sums, next)
		}
	}
}
