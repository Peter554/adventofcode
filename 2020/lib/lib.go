package lib

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

var inputPath string

func init() {
	flag.StringVar(&inputPath, "input", "input", "The input file")
}

func Check(err error) {
	if err != nil {
		panic(err)
	}
}

func UseInput(input string) {
	Check(flag.Set("input", input))
}

func ReadInput() []string {
	flag.Parse()
	file, err := os.Open(inputPath)
	Check(err)
	defer file.Close()
	lines := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	Check(scanner.Err())
	return lines
}

func ReadInputAsInts() []int {
	lines := ReadInput()
	ints := []int{}
	for _, line := range lines {
		ints = append(ints, AsInt(line))
	}
	return ints
}

func AsInt(s string) int {
	i, err := strconv.Atoi(s)
	Check(err)
	return i
}

func TestLines(raw string) []string {
	lines := strings.Split(raw, "\n")
	return lines[1:]
}

func Expect(t *testing.T, want, got interface{}) {
	if want != got {
		t.Errorf("Expected %v, got %v", want, got)
	}
}

func Assert(want, got interface{}) {
	if want != got {
		panic(fmt.Sprintf("Expected %v, got %v", want, got))
	}
}

func PrintResultAndAssert(part int, result int, expectedResult int) {
	fmt.Printf("Part %d = %d\n", part, result)
	if inputPath == "input" {
		Assert(expectedResult, result)
	}
}

type Result struct {
	Part          int
	Value         int
	ExpectedValue int
}

func (r Result) Execute() {
	fmt.Printf("Part %d = %d\n", r.Part, r.Value)
	if inputPath == "input" {
		Assert(r.ExpectedValue, r.Value)
	}
}
