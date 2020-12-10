package main

import (
	"regexp"
	"strconv"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()

	records := []record{}
	for _, line := range lines {
		records = append(records, parseLine(line))
	}

	validPasswordsCount := 0
	for _, r := range records {
		letterCount := 0
		for _, letter := range r.Password {
			if letter == r.Letter {
				letterCount++
			}
		}
		if letterCount >= r.X && letterCount <= r.Y {
			validPasswordsCount++
		}
	}
	lib.PrintResultAndAssert(1, validPasswordsCount, 546)

	validPasswordsCount = 0
	for _, r := range records {
		isValid := false
		for idx, letter := range r.Password {
			if (idx+1 == r.X || idx+1 == r.Y) && letter == r.Letter {
				isValid = !isValid
			}
		}
		if isValid {
			validPasswordsCount++
		}
	}
	lib.PrintResultAndAssert(2, validPasswordsCount, 275)
}

type record struct {
	X        int
	Y        int
	Letter   rune
	Password string
}

func parseLine(line string) record {
	re := regexp.MustCompile(`(\d+)-(\d+)\s([a-z]):\s([a-z]+)`)
	match := re.FindStringSubmatch(line)
	if match == nil {
		panic("Line did not match regex")
	}
	x, _ := strconv.Atoi(match[1])
	y, _ := strconv.Atoi(match[2])
	return record{
		X:        x,
		Y:        y,
		Letter:   rune(match[3][0]),
		Password: match[4],
	}
}
