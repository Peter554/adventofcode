package main

import (
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	o := 0
	for _, line := range lines {
		o += Evaluate(line)
	}
	return o
}

func Part2(lines []string) int {
	o := 0
	for _, line := range lines {
		o += EvaluateAdvanced(line)
	}
	return o
}

func Evaluate(expression string) int {
	idxs := findBracketIdxs(expression)

	if len(idxs) == 0 {
		o := 0

		op := ""
		for _, s := range strings.Split(expression, " ") {
			if s == "+" || s == "*" {
				op = s
			} else {
				i := lib.AsInt(s)
				if op == "+" {
					o += i
				} else if op == "*" {
					o *= i
				} else {
					o = i
				}
				op = ""
			}
		}

		return o
	}

	subExpression := expression[idxs[0]+1 : idxs[1]]
	nextExpression := expression[:idxs[0]] + strconv.Itoa(Evaluate(subExpression)) + expression[idxs[1]+1:]
	return Evaluate(nextExpression)
}

func EvaluateAdvanced(expression string) int {
	idxs := findBracketIdxs(expression)

	if len(idxs) == 0 {
		idxs := findPlusIdxs(expression)

		if len(idxs) == 0 {
			o := 1
			for _, s := range strings.Split(expression, " ") {
				if s == "*" {
					continue
				}
				o *= lib.AsInt(s)
			}
			return o
		}

		subExpression := expression[idxs[0] : idxs[1]+1]
		nextExpression := expression[:idxs[0]] + strconv.Itoa(Evaluate(subExpression)) + expression[idxs[1]+1:]
		return EvaluateAdvanced(nextExpression)
	}

	subExpression := expression[idxs[0]+1 : idxs[1]]
	nextExpression := expression[:idxs[0]] + strconv.Itoa(EvaluateAdvanced(subExpression)) + expression[idxs[1]+1:]
	return EvaluateAdvanced(nextExpression)
}

func findBracketIdxs(expression string) []int {
	o := []int{}
	c := 0
	for idx, char := range expression {
		if char == '(' {
			c++
			if len(o) == 0 {
				o = append(o, idx)
			}
		} else if char == ')' {
			c--
			if c == 0 {
				o = append(o, idx)
				break
			}
		}
	}
	return o
}

func findPlusIdxs(expression string) []int {
	plusIdx := -1
	for idx, char := range expression {
		if char == '+' {
			plusIdx = idx
			break
		}
	}
	if plusIdx < 0 {
		return []int{}
	}
	lower, upper := plusIdx-2, plusIdx+2
	for {
		if lower == 0 {
			break
		} else if expression[lower] == ' ' {
			lower++
			break
		} else {
			lower--
		}
	}
	for {
		if upper == len(expression)-1 {
			break
		} else if expression[upper] == ' ' {
			upper--
			break
		} else {
			upper++
		}
	}
	return []int{lower, upper}
}
