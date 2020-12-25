package main

import "fmt"

func main() {
	fmt.Println("Part 1 =", Part1())

}

func Part1() int {
	pk1, pk2 := 1614360, 7734663
	ls1 := findLoopSize(pk1)
	return transform(pk2, ls1)
}

type transformMemoKey struct {
	subjectNumber int
	loopSize      int
}

var transformMemo map[transformMemoKey]int = map[transformMemoKey]int{}

func transform(subjectNumber int, loopSize int) int {
	if loopSize == 0 {
		return 1
	}

	if value, exists := transformMemo[transformMemoKey{subjectNumber, loopSize}]; exists {
		return value
	}

	value := (transform(subjectNumber, loopSize-1) * subjectNumber) % 20201227
	transformMemo[transformMemoKey{subjectNumber, loopSize}] = value
	return value
}

func findLoopSize(pk int) (loopSize int) {
	loopSize = 1
	for {
		if transform(7, loopSize) == pk {
			return
		}
		loopSize++
	}
}
