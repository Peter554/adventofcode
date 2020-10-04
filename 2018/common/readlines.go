package common

import (
	"bufio"
	"log"
	"os"
)

func Readlines(path string) []string {
	file, err := os.Open(path)
	if err != nil {
		log.Fatalln(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	out := make([]string, 0)
	for scanner.Scan() {
		line := scanner.Text()
		out = append(out, line)
	}
	err = scanner.Err()
	if err != nil {
		log.Fatalln(err)
	}
	return out
}
