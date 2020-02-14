package main

import (
	"regexp"
	"strconv"
)

type Point interface {
	GetPosition() (int, int)
	Step()
}

func NewPoint(line string) Point {
	re := regexp.MustCompile(`position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>`)
	match := re.FindStringSubmatch(line)
	x, _ := strconv.Atoi(match[1])
	y, _ := strconv.Atoi(match[2])
	vx, _ := strconv.Atoi(match[3])
	vy, _ := strconv.Atoi(match[4])
	return &point{
		x:  x,
		y:  y,
		vx: vx,
		vy: vy,
	}
}

type point struct {
	x  int
	y  int
	vx int
	vy int
}

func (o *point) GetPosition() (int, int) {
	return o.x, o.y
}

func (o *point) Step() {
	o.x += o.vx
	o.y += o.vy
}
