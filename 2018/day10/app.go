package main

import (
	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	cloud := NewPointCloud(lines)

	collided := false
	for {
		cloud.Step()
		extent := cloud.GetExtent()
		xrange := extent.xmax - extent.xmin
		yrange := extent.ymax - extent.ymin
		if xrange < 100 && yrange < 15 {
			collided = true
			cloud.Print()
			continue
		}
		if collided {
			break
		}
	}
}
