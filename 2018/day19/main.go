package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2018/common"
	"github.com/peter554/adventofcode/2018/day19/computer"
)

func main() {
	lines := common.Readlines("./input.txt")

	c := computer.New(parseInstructionPointer(lines[0]))
	instructions := [][]int{}
	for _, line := range lines[1:] {
		instructions = append(instructions, parseInstruction(line))
	}
	c.Run(instructions)
	fmt.Println(c)
}

func parseInstructionPointer(s string) int {
	match := regexp.MustCompile(`^#ip (\d)$`).FindStringSubmatch(s)
	if match == nil {
		panic("Instruction pointer did not match regex")
	}
	i, err := strconv.Atoi(match[1])
	common.CheckError(err)
	return i
}

func parseInstruction(s string) []int {
	opCodeMap := map[string]int{
		"eqir": 0,
		"bonr": 1,
		"addr": 2,
		"gtri": 3,
		"muli": 4,
		"gtir": 5,
		"mulr": 6,
		"banr": 7,
		"boni": 8,
		"eqri": 9,
		"eqrr": 10,
		"bani": 11,
		"setr": 12,
		"gtrr": 13,
		"addi": 14,
		"seti": 15,
	}

	instruction := []int{}
	split := strings.Split(s, " ")
	instruction = append(instruction, opCodeMap[split[0]])
	for _, part := range split[1:] {
		i, err := strconv.Atoi(part)
		common.CheckError(err)
		instruction = append(instruction, i)
	}
	return instruction
}
