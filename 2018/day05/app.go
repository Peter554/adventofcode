package main

import (
	"fmt"
	"strings"
	"sync"

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
	return len(react(units, ""))
}

func getlenghtafterreaction2(units []string) int {
	min := -1
	wg := sync.WaitGroup{}
	alphabet := getalphabet()
	for _, letter := range alphabet {
		wg.Add(1)
		go func(letter string) {
			reacted := react(units, letter)
			if min == -1 || len(reacted) < min {
				min = len(reacted)
			}
			wg.Done()
		}(letter)
	}
	wg.Wait()
	return min
}

func react(units []string, remove string) []string {
	units = removeunit(units, remove)
	for {
		reactat := -1
		for idx := range units {
			if idx == 0 {
				continue
			}
			sametype := aresametype(units[idx-1], units[idx])
			oppositepolarity := areoppositepolarity(units[idx-1], units[idx])
			if sametype && oppositepolarity {
				reactat = idx - 1
				break
			}
		}
		if reactat == -1 {
			return units
		}
		units = removepair(units, reactat)
	}
}

func getalphabet() []string {
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	return strings.Split(alphabet, "")
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

// See gotcha at https://gist.github.com/Peter554/711c1035c5168289d1542e9458cc2823
func removepair(units []string, at int) []string {
	units = copyunits(units)
	return append(units[:at], units[at+2:]...)
}

func copyunits(units []string) []string {
	out := make([]string, len(units))
	copy(out, units)
	return out
}
