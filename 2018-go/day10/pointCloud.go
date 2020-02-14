package main

import "fmt"

type PointCloud interface {
	GetExtent() Extent
	HasPoint(x int, y int) bool
	Print()
	Step()
}

type Extent struct {
	xmin int
	xmax int
	ymin int
	ymax int
}

func NewPointCloud(lines []string) PointCloud {
	points := make([]Point, 0)
	for _, v := range lines {
		points = append(points, NewPoint(v))
	}
	return &pointCloud{
		points: points,
	}
}

type pointCloud struct {
	points []Point
	time   int
}

func (o *pointCloud) GetExtent() Extent {
	if len(o.points) == 0 {
		return Extent{0, 0, 0, 0}
	}
	xmin, ymin := o.points[0].GetPosition()
	xmax, ymax := xmin, ymin
	for _, v := range o.points {
		x, y := v.GetPosition()
		if x < xmin {
			xmin = x
		}
		if x > xmax {
			xmax = x
		}
		if y < ymin {
			ymin = y
		}
		if y > ymax {
			ymax = y
		}
	}
	return Extent{
		xmin: xmin,
		xmax: xmax,
		ymin: ymin,
		ymax: ymax,
	}
}

func (o *pointCloud) HasPoint(x int, y int) bool {
	for _, v := range o.points {
		px, py := v.GetPosition()
		if px == x && py == y {
			return true
		}
	}
	return false
}

func (o *pointCloud) Print() {
	fmt.Println()
	extent := o.GetExtent()
	for y := extent.ymin; y <= extent.ymax; y++ {
		s := ""
		for x := extent.xmin; x <= extent.xmax; x++ {
			if o.HasPoint(x, y) {
				s += "#"
			} else {
				s += "."
			}
		}
		fmt.Println(s)
	}
	fmt.Println("Time: ", o.time)
	fmt.Println()
}

func (o *pointCloud) Step() {
	for _, v := range o.points {
		v.Step()
	}
	o.time++
}
