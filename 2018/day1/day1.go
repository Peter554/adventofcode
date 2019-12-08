package main

import (
	"fmt"
	"io/ioutil"

	"github.com/peter554/hellogo/utils"
)

func main() {
	bytes, err := ioutil.ReadFile("./input.txt")

	if err != nil {
		panic(err)
	}

	lines := utils.ReadLines(bytes)
	data, err := asInts(lines)

	if err != nil {
		panic(err)
	}

	// Task 1
	fmt.Println(sum(data))

	repeating, err := firstRepeatingSum(data)

	if err != nil {
		panic(err)
	}

	// Task 2
	fmt.Println(repeating)
}
