package main

import "fmt"

func getHundreds(x int) int {
	return 9
}

func getFuelLevel(x int, y int, offset int) int {
	o := x + 10
	o = o * y
	o += offset
	o *= x + 10
	o = getHundreds(o)
	o -= 5
	return o
}

func main() {
	fuelLevel := getFuelLevel(3, 5, 8)
	fmt.Println(fuelLevel)
}
