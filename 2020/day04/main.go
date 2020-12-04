package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	lines := readInput()
	batches := batchBy(lines, func(line string) bool { return len(line) == 0 })

	passports := []*passport{}
	for _, batch := range batches {
		passports = append(passports, readPassport(batch))
	}

	validPassportsCount := 0
	for _, passport := range passports {
		if passport.isValidSimple() {
			validPassportsCount++
		}
	}
	fmt.Println("# of valid passports =", validPassportsCount, "(simple)")

	validPassportsCount = 0
	for _, passport := range passports {
		if passport.isValid() {
			validPassportsCount++
		}
	}
	fmt.Println("# of valid passports =", validPassportsCount)
}

func readInput() []string {
	file, err := os.Open("./input.txt")
	check(err)
	defer file.Close()
	lines := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	check(scanner.Err())
	return lines
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func batchBy(lines []string, f func(line string) bool) [][]string {
	batches := [][]string{}
	batch := []string{}
	for _, line := range lines {
		batch = append(batch, line)
		if f(line) {
			batches = append(batches, batch)
			batch = []string{}
		}
	}
	if len(batch) > 0 {
		batches = append(batches, batch)
	}
	return batches
}

type passport struct {
	m map[string]string
}

func readPassport(batch []string) *passport {
	re := regexp.MustCompile(`([a-z]+):([a-z0-9#]+)`)
	m := map[string]string{}
	for _, line := range batch {
		for _, field := range strings.Fields(line) {
			match := re.FindStringSubmatch(field)
			if match == nil {
				panic(fmt.Sprintf("field %v did not match regex", field))
			}
			m[match[1]] = match[2]
		}
	}
	return &passport{m}
}

func (p *passport) isValidSimple() bool {
	requiredFields := []string{
		"byr",
		"iyr",
		"eyr",
		"hgt",
		"hcl",
		"ecl",
		"pid",
	}
	for _, field := range requiredFields {
		if _, exists := p.m[field]; !exists {
			return false
		}
	}
	return true
}

func isNumber(min, max int) func(s string) bool {
	return func(s string) bool {
		i, err := strconv.Atoi(s)
		if err != nil {
			return false
		}
		return i >= min && i <= max
	}
}

func (p *passport) isValid() bool {
	requiredFields := map[string]func(value string) bool{
		"byr": isNumber(1920, 2002),
		"iyr": isNumber(2010, 2020),
		"eyr": isNumber(2020, 2030),
		"hgt": func(value string) bool {
			match := regexp.MustCompile(`^(\d+)cm$`).FindStringSubmatch(value)
			if match != nil {
				return isNumber(150, 193)(match[1])
			}
			match = regexp.MustCompile(`^(\d+)in$`).FindStringSubmatch(value)
			if match != nil {
				return isNumber(59, 76)(match[1])
			}
			return false
		},
		"hcl": func(value string) bool {
			return regexp.MustCompile(`^#[0-9a-f]{6}$`).FindStringSubmatch(value) != nil
		},
		"ecl": func(value string) bool {
			return regexp.MustCompile(`^(amb|blu|brn|gry|grn|hzl|oth)$`).FindStringSubmatch(value) != nil
		},
		"pid": func(value string) bool {
			return regexp.MustCompile(`^[0-9]{9}$`).FindStringSubmatch(value) != nil
		},
	}
	for field, validator := range requiredFields {
		value, exists := p.m[field]
		if !exists || !validator(value) {
			return false
		}
	}
	return true
}
