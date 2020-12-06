package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2018/common"
	"github.com/peter554/adventofcode/2018/day16/computer"
)

func main() {
	computer := computer.New()
	for _, line := range common.Readlines("./input2.txt") {
		instruction := parseInstruction(line)
		computer.Update(instruction)
	}
	fmt.Println(computer)
}

func parseInstruction(s string) []int {
	instruction := []int{}
	for _, v := range strings.Split(s, " ") {
		i, err := strconv.Atoi(v)
		common.Check(err)
		instruction = append(instruction, i)
	}
	return instruction
}
