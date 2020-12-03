package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	lines := readInput()
	env := asRunes(lines)

	slopes := []slope{
		slope{1, 1},
		slope{3, 1},
		slope{5, 1},
		slope{7, 1},
		slope{1, 2},
	}

	results := []int{}
	for _, slope := range slopes {
		x, y, treeCount := 0, 0, 0
		for y < len(env) {
			if env[y][x] == '#' {
				treeCount++
			}
			x = (x + slope.Dx) % len(env[0])
			y = y + slope.Dy
		}
		fmt.Println("# of trees met =", treeCount, fmt.Sprintf("(slope %v)", slope))
		results = append(results, treeCount)
	}

	fmt.Println("Product of results =", reduce(results, func(acc, next int) int { return acc * next }))
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func readInput() []string {
	file, err := os.Open("./input.txt")
	check(err)
	defer file.Close()
	lines := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	check(scanner.Err())
	return lines
}

func asRunes(lines []string) [][]rune {
	a := [][]rune{}
	for _, line := range lines {
		b := []rune{}
		for _, letter := range line {
			b = append(b, letter)
		}
		a = append(a, b)
	}
	return a
}

type slope struct {
	Dx int
	Dy int
}

func reduce(ints []int, f func(acc, next int) int) int {
	o := ints[0]
	for _, i := range ints[1:] {
		o = f(o, i)
	}
	return o
}
