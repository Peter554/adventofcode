package main

import (
	"fmt"
	"io/ioutil"

	"github.com/peter554/hellogo/utils"
)

type doneType struct{}

func main() {
	bytes, err := ioutil.ReadFile("./input.txt")

	if err != nil {
		panic(err)
	}

	lines := utils.ReadLines(bytes)

	numberOfLinesWithLetterRepeatedExactlyTwoTimes := 0
	numberOfLinesWithLetterRepeatedExactlyThreeTimes := 0

	for _, line := range lines {
		if letterAppearsExactlyNTimes(line, 2) {
			numberOfLinesWithLetterRepeatedExactlyTwoTimes++
		}

		if letterAppearsExactlyNTimes(line, 3) {
			numberOfLinesWithLetterRepeatedExactlyThreeTimes++
		}
	}

	// Task 1
	fmt.Println(numberOfLinesWithLetterRepeatedExactlyTwoTimes * numberOfLinesWithLetterRepeatedExactlyThreeTimes)

	done := make(chan doneType)

	go func() {
		for _, line1 := range lines {
			for _, line2 := range lines {
				common, removed, err := lettersInCommon(line1, line2)

				if err != nil {
					panic(err)
				}

				if removed == 1 {
					// Task 2
					fmt.Println(common)
					done <- doneType{}
				}
			}
		}
	}()

	<-done
}
