package main

import (
	"fmt"

	"github.com/peter554/adventofcode/2020/day08/compute"
	"github.com/peter554/adventofcode/2020/day08/parse"
	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	instructions := parse.Parse(lines)

	result := compute.Run(instructions)
	fmt.Println(result)

	idxs := findIdxs(instructions, func(instruction parse.Instruction) bool {
		return instruction.Op == "jmp" || instruction.Op == "nop"
	})

	for _, idx := range idxs {
		copiedInstructions := copy(instructions)

		if copiedInstructions[idx].Op == "jmp" {
			copiedInstructions[idx].Op = "nop"
		} else {
			copiedInstructions[idx].Op = "jmp"
		}

		result := compute.Run(copiedInstructions)
		if result.ExitCode == 0 {
			fmt.Println(result)
			return
		}
	}
}

func findIdxs(instructions []parse.Instruction, filter func(instruction parse.Instruction) bool) []int {
	idxs := []int{}
	for idx, instruction := range instructions {
		if filter(instruction) {
			idxs = append(idxs, idx)
		}
	}
	return idxs
}

func copy(instructions []parse.Instruction) []parse.Instruction {
	o := []parse.Instruction{}
	for _, instruction := range instructions {
		o = append(o, parse.Instruction{Op: instruction.Op, Value: instruction.Value})
	}
	return o
}
