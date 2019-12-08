package main

import (
	"fmt"
	"strings"

	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	rawdata := common.Readlines("./input.txt")[0]
	units := strings.Split(rawdata, "")
	fmt.Println("Part 1")
	fmt.Printf("Lenght = %d\n", getlenghtafterreaction(units))
	fmt.Println("Part 2")
	fmt.Printf("Minimum lenght = %d\n", getlenghtafterreaction2(units))
}

func getlenghtafterreaction(units []string) int {
	return len(react(units))
}

func getlenghtafterreaction2(units []string) int {
	min := -1
	alphabet := getalphabet()
	for _, letter := range alphabet {
		reacted := react(removeunit(units, letter))
		if min == -1 || len(reacted) < min {
			min = len(reacted)
		}
	}
	return min
}

func react(units []string) []string {
	cpy := copyunits(units)
	for {
		didreact := false
		for idx, _ := range cpy {
			if idx == 0 {
				continue
			}
			sametype := aresametype(cpy[idx-1], cpy[idx])
			oppositepolarity := areoppositepolarity(cpy[idx-1], cpy[idx])
			if sametype && oppositepolarity {
				cpy = removepair(cpy, idx-1)
				didreact = true
				break
			}
		}
		if !didreact {
			return cpy
		}
	}
}

func aresametype(a string, b string) bool {
	return strings.ToLower(a) == strings.ToLower(b)
}

func islower(s string) bool {
	return s == strings.ToLower(s)
}

func isupper(s string) bool {
	return s == strings.ToUpper(s)
}

func areoppositepolarity(a string, b string) bool {
	return (islower(a) && isupper(b)) || (isupper(a) && islower(b))
}

func removepair(units []string, at int) []string {
	return append(units[:at], units[at+2:]...)
}

func removeunit(units []string, unit string) []string {
	out := make([]string, 0)
	for _, v := range units {
		if strings.ToLower(v) == strings.ToLower(unit) {
			continue
		}
		out = append(out, v)
	}
	return out
}

func getalphabet() []string {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	return strings.Split(alphabet, "")
}

// Why is this required?
func copyunits(units []string) []string {
	out := make([]string, len(units))
	copy(out, units)
	return out
}
