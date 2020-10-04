package main

import (
	"fmt"
)

func main() {
	nPlayers := 446
	lastMarbleValue := 71522

	topPlayer, highScore := runMarbleGame(nPlayers, lastMarbleValue)
	fmt.Printf("Highscore: Player %v scored %v\n", topPlayer, highScore)

	topPlayer, highScore = runMarbleGame(nPlayers, lastMarbleValue*100)
	fmt.Printf("Highscore: Player %v scored %v\n", topPlayer, highScore)
}

func runMarbleGame(nPlayers int, lastMarbleValue int) (int, int) {
	scoreCounter := NewScoreCounter()
	currentMarble := &node{value: 0}
	currentMarble.previous = currentMarble
	currentMarble.next = currentMarble
	for marbleValue := 1; marbleValue <= lastMarbleValue; marbleValue++ {
		currentPlayer := (marbleValue-1)%nPlayers + 1
		if marbleValue%23 == 0 {
			removeMarble := currentMarble.previous.previous.previous.previous.previous.previous.previous
			scoreCounter.IncrementScore(currentPlayer, marbleValue)
			scoreCounter.IncrementScore(currentPlayer, removeMarble.value)
			connectNodes(removeMarble.previous, removeMarble.next)
			currentMarble = removeMarble.next
		} else {
			addMarble := &node{value: marbleValue}
			connectNodes(addMarble, currentMarble.next.next)
			connectNodes(currentMarble.next, addMarble)
			currentMarble = addMarble
		}
	}
	return scoreCounter.GetHighscore()
}

type node struct {
	previous *node
	next     *node
	value    int
}

func connectNodes(from *node, to *node) {
	from.next = to
	to.previous = from
}
