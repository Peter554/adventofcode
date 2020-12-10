package lib

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

func Check(err error) {
	if err != nil {
		panic(err)
	}
}

func ReadInput() []string {
	file, err := os.Open("input")
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
		i, err := strconv.Atoi(line)
		Check(err)
		ints = append(ints, i)
	}
	return ints
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

func PrintResult(part int, result int) {
	fmt.Printf("Part %d = %d\n", part, result)
}

func PrintResultAndAssert(part int, result int, expectedResult int) {
	PrintResult(part, result)
	Assert(expectedResult, result)
}
