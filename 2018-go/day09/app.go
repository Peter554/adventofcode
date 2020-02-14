package main

import (
	"fmt"
)

func main() {
	nPlayers := 446
	lastMarble := 71522
	topPlayer, highScore := runMarbleGame(nPlayers, lastMarble)
	fmt.Printf("Highscore: Player %v scored %v\n", topPlayer, highScore)
}

func runMarbleGame(nPlayers int, lastMarble int) (int, int) {
	scoreCounter := NewScoreCounter()
	marbles := []int{0}
	currentIdx := 0
	for marble := 1; marble <= lastMarble; marble++ {
		currentPlayer := (marble-1)%nPlayers + 1
		if marble%23 == 0 {
			removeIdx := (currentIdx - 7 + len(marbles)) % len(marbles)
			scoreCounter.IncrementScore(currentPlayer, marble)
			scoreCounter.IncrementScore(currentPlayer, marbles[removeIdx])
			marbles = append(marbles[:removeIdx], marbles[removeIdx+1:]...)
			currentIdx = removeIdx
		} else {
			insertIdx := (currentIdx + 2) % len(marbles)
			marbles = append(marbles[:insertIdx], append([]int{marble}, marbles[insertIdx:]...)...)
			currentIdx = insertIdx
		}
	}
	return scoreCounter.GetHighscore()
}
