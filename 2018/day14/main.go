package main

import (
	"fmt"
	"strconv"
	"strings"
)

func main() {
	fmt.Println(cook(640441))
	fmt.Println(cook2([]uint8{6, 4, 0, 4, 4, 1}))
}

func cook(n int) string {
	recipes := []int{3, 7}
	idx1 := 0
	idx2 := 1

	for {
		if len(recipes) >= n+10 {
			s := ""
			for idx := n; idx < n+10; idx++ {
				s += strconv.Itoa(recipes[idx])
			}
			return s
		}

		score1 := recipes[idx1]
		score2 := recipes[idx2]

		sum := score1 + score2
		for _, s := range strings.Split(strconv.Itoa(sum), "") {
			i, _ := strconv.Atoi(s)
			recipes = append(recipes, i)
		}

		idx1 = (idx1 + 1 + score1) % len(recipes)
		idx2 = (idx2 + 1 + score2) % len(recipes)
	}
}

func cook2(ns []uint8) int {
	recipes := map[int]uint8{
		0: 3,
		1: 7,
	}
	idx1 := 0
	idx2 := 1

	count := 2
	for {
		if endswith(count, recipes, ns) {
			return count - len(ns)
		}
		if endswith(count, recipes, append(ns, 0)) {
			return count - len(ns) - 1
		}

		score1 := recipes[idx1]
		score2 := recipes[idx2]

		sum := score1 + score2
		for _, s := range strings.Split(strconv.Itoa(int(sum)), "") {
			i, _ := strconv.Atoi(s)
			recipes[count] = uint8(i)
			count++
		}

		idx1 = (idx1 + 1 + int(score1)) % count
		idx2 = (idx2 + 1 + int(score2)) % count
	}
}

func endswith(count int, recipes map[int]uint8, ns []uint8) bool {
	if count < len(ns) {
		return false
	}

	j := 0
	for i := count - len(ns); i < count; i++ {
		if ns[j] != recipes[i] {
			return false
		}
		j++
	}
	return true
}
