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

func getGridFuelLevel(x int, y int, gridSize int, offset int) int {
	t := 0
	for i := x; i < x+gridSize; i++ {
		for j := y; j < y+gridSize; j++ {
			t += getCellFuelLevel(i, j, offset)
		}
	}
	return t
}

func findMaxFuelGrid(gridSize int, offset int) (int, int, int) {
	maxFuel := getGridFuelLevel(1, 1, gridSize, offset)
	maxX := 1
	maxY := 1
	for x := 1; x <= 300-gridSize; x++ {
		for y := 1; y <= 300-gridSize; y++ {
			fuel := getGridFuelLevel(x, y, gridSize, offset)
			if fuel > maxFuel {
				maxX = x
				maxY = y
				maxFuel = fuel
			}
		}
	}
	return maxFuel, maxX, maxY
}

func main() {
	offset := 9221
	maxFuel := getGridFuelLevel(1, 1, 1, offset)
	maxSize := 1
	maxX := 1
	maxY := 1
	for size := 1; size <= 300; size++ {
		fuel, x, y := findMaxFuelGrid(size, offset)
		if fuel > maxFuel {
			maxFuel = fuel
			maxX = x
			maxY = y
			maxSize = size
		}
	}
	fmt.Printf("(%d, %d, %d)\n", maxX, maxY, maxSize)
}
