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
	claims := make([]claim, 0)

	m := make(map[coordinate]int)

	for _, line := range lines {
		c, _ := getClaim(line)
		claims = append(claims, c)
	}

	for _, c := range claims {
		addClaimToMap(m, c)
	}

	// Task 1
	fmt.Println(getNumberOfCoordinatesInTwoOrMoreClaims(m))

	for _, c1 := range claims {
		overlaps := false

		for _, c2 := range claims {
			if c1 != c2 && c1.overlaps(c2) {
				overlaps = true
				break
			}
		}

		if !overlaps {
			// Task 2
			fmt.Println(c1.id)
			break
		}
	}
}
