package parse

import (
	"regexp"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func Parse(line string) (parent string, children map[string]int) {
	line = strings.ReplaceAll(line, ".", "")

	parent = strings.TrimSpace(strings.Split(line, "bags contain")[0])

	children = map[string]int{}
	if regexp.MustCompile(`no other bags`).FindStringSubmatch(line) != nil {
		return
	}
	re := regexp.MustCompile(`(\d)\s([a-z]+\s[a-z]+)`)
	for _, s := range strings.Split(strings.Split(line, "bags contain")[1], ",") {
		match := re.FindStringSubmatch(s)
		i, err := strconv.Atoi(match[1])
		lib.Check(err)
		children[strings.TrimSpace(match[2])] = i
	}
	return
}
