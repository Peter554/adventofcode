package main

import (
	"github.com/peter554/adventofcode/2020/go/day08/compute"
	"github.com/peter554/adventofcode/2020/go/day08/parse"
	"github.com/peter554/adventofcode/2020/go/lib"
)

func main() {
	lines := lib.ReadInput()
	instructions := parse.Parse(lines)

	result := compute.Run(instructions)
	lib.Result{Part: 1, Value: result.Acc}.Print().Assert(1475)

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
			lib.Result{Part: 2, Value: result.Acc}.Print().Assert(1270)
			return
		}
	}
}

func Part1(lines []string) int {
	instructions := parse.Parse(lines)
	return compute.Run(instructions).Acc
}

func Part2(lines []string) int {
	instructions := parse.Parse(lines)

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
			return result.Acc
		}
	}
	panic("not found")
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
