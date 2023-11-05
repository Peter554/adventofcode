package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart1(t *testing.T) {
	lib.Expect(t, 5414549, Part1())
}

func Test_findLoopSize(t *testing.T) {
	lib.Expect(t, 8, findLoopSize(5764801))
	lib.Expect(t, 11, findLoopSize(17807724))
}
