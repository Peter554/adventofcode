package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	validPassportsCount := countValidPassports(lines, func(p *passport) bool { return p.isValidSimple() })
	lib.PrintResultAndAssert(1, validPassportsCount, 250)
	validPassportsCount = countValidPassports(lines, func(p *passport) bool { return p.isValid() })
	lib.PrintResultAndAssert(2, validPassportsCount, 158)
}

func countValidPassports(lines []string, validator func(p *passport) bool) int {
	lines = strings.Split(strings.Join(lines, "\n"), "\n\n")
	passports := []*passport{}
	for _, line := range lines {
		passports = append(passports, readPassport(line))
	}
	validPassportsCount := 0
	for _, passport := range passports {
		if validator(passport) {
			validPassportsCount++
		}
	}
	return validPassportsCount
}

type passport struct {
	m map[string]string
}

func readPassport(rawData string) *passport {
	re := regexp.MustCompile(`([a-z]+):([a-z0-9#]+)`)
	m := map[string]string{}
	for _, field := range strings.Fields(rawData) {
		match := re.FindStringSubmatch(field)
		if match == nil {
			panic(fmt.Sprintf("field %v did not match regex", field))
		}
		m[match[1]] = match[2]
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
