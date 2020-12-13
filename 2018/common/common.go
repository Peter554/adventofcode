package common

import (
	"bufio"
	"os"
)

func Readlines(path string) []string {
	file, err := os.Open(path)
	CheckError(err)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	lines := []string{}
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	CheckError(scanner.Err())
	return lines
}

func CheckError(err error) {
	if err != nil {
		panic(err)
	}
}
