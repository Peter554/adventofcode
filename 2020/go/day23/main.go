package main

import (
	"fmt"
	"strings"
)

func main() {
	input := []int{7, 8, 4, 2, 3, 5, 9, 1, 6}
	fmt.Println("Part 1 =", Part1(input))
	fmt.Println("Part 2 =", Part2(input))
}

func Part1(input []int) string {
	cupLookup := playCups(input, 100)

	s := ""
	cup := cupLookup[1].Next
	for cup != cupLookup[1] {
		s += fmt.Sprint(cup.Number)
		cup = cup.Next
	}
	return s
}

func Part2(input []int) int {
	_, max := minMax(input)
	length := len(input)
	for i := 0; i < 1000000-length; i++ {
		input = append(input, max+1+i)
	}

	cupLookup := playCups(input, 10000000)

	return cupLookup[1].Next.Number * cupLookup[1].Next.Next.Number
}

func playCups(input []int, nTurns int) map[int]*Cup {
	min, max := minMax(input)

	cupLookup := map[int]*Cup{}
	for _, i := range input {
		cupLookup[i] = &Cup{Number: i}
	}
	for idx, i := range input {
		cupLookup[i].Next = cupLookup[input[(idx+1)%len(input)]]
	}

	currentCup := cupLookup[input[0]]
	for i := 0; i < nTurns; i++ {
		threeCupStart := currentCup.Next
		threeCupEnd := threeCupStart.Next.Next
		currentCup.Next = threeCupEnd.Next

		destinationCupNumber := currentCup.Number - 1
		for {
			if destinationCupNumber < min {
				destinationCupNumber = max
			}

			if (destinationCupNumber != threeCupStart.Number) &&
				(destinationCupNumber != threeCupStart.Next.Number) &&
				(destinationCupNumber != threeCupEnd.Number) {
				break
			}

			destinationCupNumber--
		}
		destinationCup := cupLookup[destinationCupNumber]

		t := destinationCup.Next
		destinationCup.Next = threeCupStart
		threeCupEnd.Next = t

		currentCup = currentCup.Next
	}

	return cupLookup
}

type Cup struct {
	Number int
	Next   *Cup
}

func (c *Cup) String() string {
	o := []string{fmt.Sprint(c.Number)}
	cup := c.Next
	for cup != nil && cup != c {
		o = append(o, fmt.Sprint(cup.Number))
		cup = cup.Next
	}
	s := strings.Join(o, " -> ")
	if cup == nil {
		s += " -> NIL"
	}
	return s
}

func minMax(is []int) (min, max int) {
	min, max = is[0], is[0]
	for _, i := range is {
		if i < min {
			min = i
		}
		if i > max {
			max = i
		}
	}
	return
}
