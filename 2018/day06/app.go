package main

import (
	"math"
	"regexp"
	"sort"
	"strconv"

	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	lines := common.Readlines("./input.txt")

	points := getPoints(lines)
	box := getBox(points)

	areaCounts := getZeroedDict(points)
	for i := box.bottomLeft.x; i <= box.bottomLeft.x+box.width; i++ {
		for j := box.bottomLeft.y; j <= box.bottomLeft.y+box.height; j++ {
			t := Point{x: i, y: j}
			closestPoint := points[0]
			minDistance := box.width + box.height
			distances := make([]int, 0)
			for _, p := range points {
				distance := getDistance(t, p)
				if distance < minDistance {
					closestPoint = p
					minDistance = distance
				}
				distances = append(distances, distance)
			}
			if count(distances, minDistance) == 1 {
				areaCounts[closestPoint]++
			}
		}
	}
	println(getMaxValue(areaCounts))

	d := make(map[Point]int)
	for i := box.bottomLeft.x; i <= box.bottomLeft.x+box.width; i++ {
		for j := box.bottomLeft.y; j <= box.bottomLeft.y+box.height; j++ {
			t := Point{x: i, y: j}
			d[t] = 0
			for _, p := range points {
				d[t] += getDistance(t, p)
			}
		}
	}
	ds := getValues(d)
	sort.Ints(ds)
	cs := cumSum(ds)
	println(len(filter(cs, func(i int) bool {
		return i < 10000
	})))
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

func contains(a []Point, b Point) bool {
	for i := 0; i < len(a); i++ {
		if a[i] == b {
			return true
		}
	}
	return false
}

func getZeroedDict(points []Point) map[Point]int {
	m := make(map[Point]int)
	for _, p := range points {
		m[p] = 0
	}
	return m
}

func count(a []int, b int) int {
	o := 0
	for i := 0; i < len(a); i++ {
		if a[i] == b {
			o++
		}
	}
	return o
}

func getMaxValue(d map[Point]int) int {
	o := -1
	for _, v := range d {
		if v > o {
			o = v
		}
	}
	return o
}

func getValues(d map[Point]int) []int {
	o := make([]int, 0)
	for _, v := range d {
		o = append(o, v)
	}
	return o
}

func cumSum(a []int) []int {
	o := make([]int, 0)
	sum := 0
	for _, v := range a {
		sum += v
		o = append(o, v)
	}
	return o
}

func filter(a []int, f func(int) bool) []int {
	o := make([]int, 0)
	for _, v := range a {
		if f(v) {
			o = append(o, v)
		}
	}
	return o
}
