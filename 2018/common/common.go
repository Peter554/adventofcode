package common

import (
	"bufio"
	"os"
)

func Readlines(path string) []string {
	file, err := os.Open(path)
	Check(err)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	lines := []string{}
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	Check(scanner.Err())
	return lines
}

func Check(err error) {
	if err != nil {
		panic(err)
	}
}
