package main

import (
	"regexp"
	"strings"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	rules, messages := parseInput(lines)

	re := regexp.MustCompile(`\d+`)
	for {
		done := true

		for k := range rules {
			rules[k] = re.ReplaceAllStringFunc(rules[k], func(s string) string {
				done = false
				return rules[lib.AsInt(s)]
			})
		}

		if done {
			break
		}
	}

	regexRules := map[int]*regexp.Regexp{}

	for k := range rules {
		replacer := strings.NewReplacer("\"", "", " ", "")
		regexRules[k] = regexp.MustCompile("^" + replacer.Replace(rules[k]) + "$")
	}

	rule0 := regexRules[0]

	count := 0
	for _, message := range messages {
		if rule0.MatchString(message) {
			count++
		}
	}
	return count
}

func Part2(lines []string) int {
	rules, messages := parseInput(lines)

	rules[8] = "(42 | 42 8)"
	rules[11] = "(42 31 | 42 11 31)"

	count8 := map[int]int{}
	count11 := map[int]int{}
	maxRecurse := 10

	re := regexp.MustCompile(`\d+`)
	for {
		done := true

		for k := range rules {
			rules[k] = re.ReplaceAllStringFunc(rules[k], func(s string) string {
				done = false
				i := lib.AsInt(s)
				if i == 8 {
					if _, exists := count8[i]; !exists {
						count8[i] = 0
					}
					count8[i]++
					if count8[i] > maxRecurse {
						return "(42)"
					}
				}
				if i == 11 {
					if _, exists := count11[i]; !exists {
						count11[i] = 0
					}
					count11[i]++
					if count11[i] > maxRecurse {
						return "(42 31)"
					}
				}
				return rules[i]
			})
		}

		if done {
			break
		}
	}

	regexRules := map[int]*regexp.Regexp{}

	for k := range rules {
		replacer := strings.NewReplacer("\"", "", " ", "")
		regexRules[k] = regexp.MustCompile("^" + replacer.Replace(rules[k]) + "$")
	}

	rule0 := regexRules[0]

	count := 0
	for _, message := range messages {
		if rule0.MatchString(message) {
			count++
		}
	}
	return count
}

func parseInput(lines []string) (rules map[int]string, messages []string) {
	rules = map[int]string{}
	parts := strings.Split(strings.Join(lines, "\n"), "\n\n")
	for _, line := range strings.Split(parts[0], "\n") {
		k := lib.AsInt(strings.Split(line, ":")[0])
		v := "(" + strings.Split(line, ":")[1][1:] + ")"
		rules[k] = v
	}
	messages = strings.Split(parts[1], "\n")
	return
}
