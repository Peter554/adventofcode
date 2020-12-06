package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestPart1(t *testing.T) {
	lines := lib.TestLines(`
abc

a
b
c

ab
ac

a
a
a
a

b`)

	lib.Expect(t, 11, Part1(lines))
}

func TestPart2(t *testing.T) {
	lines := lib.TestLines(`
abc

a
b
c

ab
ac

a
a
a
a

b`)

	lib.Expect(t, 6, Part2(lines))
}
