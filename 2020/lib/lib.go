package lib

import (
	"bufio"
	"os"
	"strings"
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

func TestLines(raw string) []string {
	lines := strings.Split(raw, "\n")
	return lines[1:]
}
