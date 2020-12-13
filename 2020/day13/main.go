package main

import (
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	myArrival := lib.AsInt(lines[0])

	busesAfterMyArrival := map[int]int{}
	for _, item := range strings.Split(lines[1], ",") {
		if item == "x" {
			continue
		}
		bus := lib.AsInt(item)
		busesAfterMyArrival[bus] = bus - myArrival%bus
	}

	nextBus, nextBusArrivesIn := -1, myArrival
	for bus, arrivesIn := range busesAfterMyArrival {
		if arrivesIn < nextBusArrivesIn {
			nextBusArrivesIn = arrivesIn
			nextBus = bus
		}
	}

	return nextBus * nextBusArrivesIn
}

func Part2(lines []string) int {
	buses := map[int]int{}
	for idx, item := range strings.Split(lines[1], ",") {
		if item == "x" {
			continue
		}
		buses[idx] = lib.AsInt(item)
	}

	t := buses[0]
	delta := buses[0]

	for dt, bus := range buses {
		for {
			if (t+dt)%bus == 0 {
				break
			}
			t += delta
		}
		delta = lcm(delta, bus)
	}

	return t
}

func lcm(a, b int) int {
	gcd := func(a, b int) int {
		for b != 0 {
			t := b
			b = a % b
			a = t
		}
		return a
	}
	return a * b / gcd(a, b)
}
