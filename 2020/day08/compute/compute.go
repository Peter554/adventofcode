package compute

import (
	"github.com/peter554/adventofcode/2020/day08/parse"
)

type RunResult struct {
	Acc      int
	ExitCode int
}

func Run(instructions []parse.Instruction) RunResult {
	ip := 0
	previousIps := map[int]bool{}
	acc := 0
	exitCode := 1

	for {
		if _, exists := previousIps[ip]; exists {
			break
		}
		previousIps[ip] = true

		instruction := instructions[ip]

		if instruction.Op == "acc" {
			acc += instruction.Value
			ip++
		} else if instruction.Op == "jmp" {
			ip += instruction.Value
		} else if instruction.Op == "nop" {
			ip++
		} else {
			panic("Instruction not recognized")
		}

		if ip == len(instructions) {
			exitCode = 0
			break
		}
	}

	return RunResult{Acc: acc, ExitCode: exitCode}
}
