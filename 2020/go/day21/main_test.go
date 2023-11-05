package main

import (
	"testing"

	"github.com/peter554/adventofcode/2020/go/lib"
)

func TestPart1(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, 5, Part1(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, 2517, Part1(lines))
}

func TestPart2(t *testing.T) {
	lib.UseInput("sample")
	lines := lib.ReadInput()
	lib.Expect(t, "mxmxvkd,sqjhc,fvjkl", Part2(lines))

	lib.UseInput("input")
	lines = lib.ReadInput()
	lib.Expect(t, "rhvbn,mmcpg,kjf,fvk,lbmt,jgtb,hcbdb,zrb", Part2(lines))
}
