package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func main() {
	bytes, err := ioutil.ReadFile("./input.txt")

	if err != nil {
		panic(err)
	}

	// Trim
	s := strings.TrimSpace(string(bytes))
	bytes = []byte(s)

	reacted := react(bytes)

	// Task 1
	fmt.Println(len(reacted))

	min := len(bytes)

	for code := 65; code <= 90; code++ {
		c := removeUnit(bytes, code)
		r := react(c)

		if l := len(r); l < min {
			min = l
		}
	}

	// Task 2
	fmt.Println(min)
}

func areSameType(a byte, b byte) bool {
	if a == b {
		return true
	}

	if a >= 65 && a <= 90 && b == a+32 {
		return true
	}

	if b >= 65 && b <= 90 && a == b+32 {
		return true
	}

	return false
}

func areOppositePolarity(a byte, b byte) bool {
	if a == b {
		return false
	}

	if a >= 65 && a <= 90 && b == a+32 {
		return true
	}

	if b >= 65 && b <= 90 && a == b+32 {
		return true
	}

	return false
}

func removePair(bytes []byte, at int) []byte {
	return append(bytes[:at], bytes[at+2:]...)
}

func react(bytes []byte) []byte {
	cpy := make([]byte, len(bytes))
	copy(cpy, bytes)

	done := false

	for !done {
		didReact := false

		for i, _ := range cpy {
			if i > 0 &&
				areSameType(cpy[i-1], cpy[i]) &&
				areOppositePolarity(cpy[i-1], cpy[i]) {
				cpy = removePair(cpy, i-1)
				didReact = true
				break
			}
		}

		if !didReact {
			done = true
		}
	}

	return cpy
}

func removeUnit(bytes []byte, unitCode int) []byte {
	out := make([]byte, 0)

	for _, b := range bytes {
		if unitCode != int(b) && unitCode+32 != int(b) && unitCode-32 != int(b) {
			out = append(out, b)
		}
	}

	return out
}
