package main

import (
	"math"
	"regexp"
	"strconv"

	"github.com/peter554/adventofcode/2018-go/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	points := getPoints(lines)
	box := getBox(points)
	dict := getInitialDict(points)
	for i := box.bottomLeft.x; i <= box.bottomLeft.x+box.width; i++ {
		for j := box.bottomLeft.y; j <= box.bottomLeft.y+box.height; j++ {
			t := Point{x: i, y: j}
			for _, p := range points {
				d := getDistance(t, p)
			}
		}
	}
}

type Point struct {
	x int
	y int
}

type Box struct {
	bottomLeft Point
	width      int
	height     int
}

func getPoints(lines []string) []Point {
	o := make([]Point, 0)
	re := regexp.MustCompile(`(\d+),\s?(\d+)`)
	for _, line := range lines {
		match := re.FindStringSubmatch(line)
		x, _ := strconv.Atoi(match[1])
		y, _ := strconv.Atoi(match[2])
		o = append(o, Point{x: x, y: y})
	}
	return o
}

func getBox(points []Point) Box {
	minX := points[0].x
	maxX := points[0].x
	minY := points[0].y
	maxY := points[0].y

	for _, p := range points {
		if p.x < minX {
			minX = p.x
		}
		if p.x > maxX {
			maxX = p.x
		}
		if p.y < minY {
			minY = p.y
		}
		if p.y > maxY {
			maxY = p.y
		}
	}

	return Box{
		bottomLeft: Point{
			x: minX,
			y: minY,
		},
		width:  maxX - minX,
		height: maxY - minY,
	}
}

func getDistance(a Point, b Point) int {
	return abs(a.x-b.x) + abs(a.y-b.y)
}

func abs(i int) int {
	return int(math.Abs(float64(i)))
}

func getInitialDict(points []Point) map[Point]int {
	m := make(map[Point]int)
	for _, p := range points {
		m[p] = 0
	}
	return m
}
