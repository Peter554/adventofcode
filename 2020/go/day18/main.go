package main

import (
	"regexp"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2020/go/lib"
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
	re := regexp.MustCompile(`\([^\(\)]+\)`)
	for re.MatchString(expression) {
		expression = re.ReplaceAllStringFunc(expression, func(s string) string {
			return strconv.Itoa(Evaluate(s[1 : len(s)-1]))
		})
	}
	return l2r(expression)
}

func EvaluateAdvanced(expression string) int {
	re := regexp.MustCompile(`\([^\(\)]+\)`)
	for re.MatchString(expression) {
		expression = re.ReplaceAllStringFunc(expression, func(s string) string {
			return strconv.Itoa(EvaluateAdvanced(s[1 : len(s)-1]))
		})
	}
	re = regexp.MustCompile(`\d+ \+ \d+`)
	for re.MatchString(expression) {
		expression = re.ReplaceAllStringFunc(expression, func(s string) string {
			return strconv.Itoa(l2r(s))
		})
	}
	return l2r(expression)
}

func l2r(expression string) int {
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
