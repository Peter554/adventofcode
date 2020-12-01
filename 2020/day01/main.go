package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	file, err := os.Open("./input.txt")
	check(err)
	defer file.Close()

	ints := []int{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		i, err := strconv.Atoi(scanner.Text())
		check(err)
		ints = append(ints, i)
	}
	check(scanner.Err())

	for i := 0; i < len(ints); i++ {
		for j := 0; j < len(ints); j++ {
			for k := 0; k < len(ints); k++ {
				if i == j || i == k || j == k {
					continue
				}
				if (ints[i] + ints[j] + ints[k]) == 2020 {
					fmt.Println(ints[i], ints[j], ints[k], ints[i]*ints[j]*ints[k])
					return
				}
			}
		}
	}
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
