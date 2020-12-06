package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func Test_Part1(t *testing.T) {
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

func Test_Part2(t *testing.T) {
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
