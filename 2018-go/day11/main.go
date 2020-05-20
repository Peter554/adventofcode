package main

import (
	"fmt"
	"math"
)

func getHundreds(x int) int {
	f := float64(x)
	h := math.Floor(f/100) - math.Floor(f/1000)*10
	return int(h)
}

func getCellFuelLevel(x int, y int, offset int) int {
	o := x + 10
	o = o * y
	o += offset
	o *= x + 10
	o = getHundreds(o)
	o -= 5
	return o
}

func getGridFuelLevel(x int, y int, offset int) int {
	t := 0
	for i := x; i < x+3; i++ {
		for j := y; j < y+3; j++ {
			t += getCellFuelLevel(i, j, offset)
		}
	}
	return t
}

func main() {
	offset := 9221
	maxX := 1
	maxY := 1
	maxFuel := getGridFuelLevel(maxX, maxY, offset)

	for i := 1; i <= 300; i++ {
		for j := 1; j <= 300; j++ {
			fuel := getGridFuelLevel(i, j, offset)
			if fuel > maxFuel {
				maxX = i
				maxY = j
				maxFuel = fuel
			}
		}
	}

	fmt.Printf("(%d, %d)\n", maxX, maxY)
}
