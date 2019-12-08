package main

import (
	"errors"
	"strconv"
)

func asInts(lines []string) ([]int, error) {
	values := make([]int, 0)

	for _, line := range lines {
		i, err := strconv.Atoi(line)

		if err != nil {
			return values, err
		}

		values = append(values, i)
	}

	return values, nil
}

// [Task 1] Sum the integers in an array
func sum(arr []int) int {
	s := 0
	for _, v := range arr {
		s += v
	}
	return s
}

// Does the array contain the specified value?
func contains(arr []int, value int) bool {
	for _, v := range arr {
		if v == value {
			return true
		}
	}

	return false
}

// [Task 2] Loop over an array finding the first repeating cumulative sum
func firstRepeatingSum(arr []int) (int, error) {
	maxLoops := 1000

	cumsum := make([]int, 1)

	for range make([]int, maxLoops) {
		for _, v := range arr {
			last := cumsum[len(cumsum)-1]
			next := last + v

			if contains(cumsum, next) {
				return next, nil
			}

			cumsum = append(cumsum, next)
		}
	}

	return -1, errors.New("Max loop depth reached.")
}
