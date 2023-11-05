package lib

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"testing"
)

var inputPath string

func init() {
	flag.StringVar(&inputPath, "input", "input", "The input file")
}

func CheckError(err error) {
	if err != nil {
		panic(err)
	}
}

func UseInput(input string) {
	CheckError(flag.Set("input", input))
}

func ReadInput() []string {
	flag.Parse()
	file, err := os.Open(inputPath)
	CheckError(err)
	defer file.Close()
	lines := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	CheckError(scanner.Err())
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
	CheckError(err)
	return i
}

func ParseInt(s string, base int) int {
	i, err := strconv.ParseInt(s, base, 64)
	CheckError(err)
	return int(i)
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

type Result struct {
	Part  int
	Value int
}

func (r Result) Print() Result {
	fmt.Printf("Part %d = %d\n", r.Part, r.Value)
	return r
}

func (r Result) Assert(value int) Result {
	if inputPath == "input" {
		Assert(value, r.Value)
	}
	return r
}

type regex struct {
	r *regexp.Regexp
}

func RE(pattern string) *regex {
	return &regex{regexp.MustCompile(pattern)}
}

func (r *regex) Test(s string) bool {
	return r.r.MatchString(s)
}

func (r *regex) Groups(s string) []string {
	match := r.r.FindStringSubmatch(s)
	if match == nil {
		panic(fmt.Sprintf("\"%s\" did not match pattern \"%v\"", s, r.r))
	}
	if len(match) == 0 {
		panic("No groups found.")
	}
	return match[1:]
}
