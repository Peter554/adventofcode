package parse

import (
	"regexp"
	"strconv"

	"github.com/peter554/adventofcode/2020/lib"
)

type Instruction struct {
	Op    string
	Value int
}

func Parse(lines []string) []Instruction {
	instructions := []Instruction{}
	re := regexp.MustCompile(`^([a-z]+)\s([+-]\d+)$`)
	for _, line := range lines {
		match := re.FindStringSubmatch(line)
		if match == nil {
			panic("Line did not match regex")
		}
		op := match[1]
		value, err := strconv.Atoi(match[2])
		lib.Check(err)
		instructions = append(instructions, Instruction{Op: op, Value: value})
	}
	return instructions
}
