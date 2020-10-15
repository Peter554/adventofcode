package main

import (
	"fmt"

	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	data := parseLines(lines)

	for i := 1; i <= 1000; i++ {
		data = evolve(data)
		_, _, total := count(data)
		fmt.Printf("%d: %d\n", i, total)
	}
}

func parseLines(lines []string) [][]string {
	o := [][]string{}
	for _, line := range lines {
		a := []string{}
		for _, r := range line {
			a = append(a, string(r))
		}
		o = append(o, a)
	}
	return o
}

func clone(data [][]string) [][]string {
	o := [][]string{}
	for _, row := range data {
		a := []string{}
		for _, s := range row {
			a = append(a, s)
		}
		o = append(o, a)
	}
	return o
}

func evolve(data [][]string) [][]string {
	o := [][]string{}
	for y, row := range data {
		a := []string{}
		for x, s := range row {
			_, w, l := inspect(data, x, y)
			if s == "." {
				if w >= 3 {
					a = append(a, "|")
				} else {
					a = append(a, ".")
				}
			}
			if s == "|" {
				if l >= 3 {
					a = append(a, "#")
				} else {
					a = append(a, "|")
				}
			}
			if s == "#" {
				if w >= 1 && l >= 1 {
					a = append(a, "#")
				} else {
					a = append(a, ".")
				}
			}
		}
		o = append(o, a)
	}
	return o
}

func count(data [][]string) (int, int, int) {
	w := 0
	l := 0
	for _, row := range data {
		for _, s := range row {
			if s == "|" {
				w++
			}
			if s == "#" {
				l++
			}
		}
	}
	return w, l, w * l
}

func inspect(data [][]string, x int, y int) (int, int, int) {
	ymax := len(data) - 1
	xmax := len(data[0]) - 1
	e := 0
	w := 0
	l := 0
	for j := y - 1; j <= y+1; j++ {
		for i := x - 1; i <= x+1; i++ {
			if i == x && j == y {
				continue
			}
			if i < 0 || j < 0 || i > xmax || j > ymax {
				continue
			}
			s := data[j][i]
			if s == "." {
				e++
			}
			if s == "|" {
				w++
			}
			if s == "#" {
				l++
			}
		}
	}
	return e, w, l
}
