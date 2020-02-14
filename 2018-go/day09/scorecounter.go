package main

type ScoreCounter interface {
	GetScore(player int) int
	GetHighscore() (int, int)
	IncrementScore(player int, points int)
}

func NewScoreCounter() ScoreCounter {
	return &marbleGameScores{
		playerScores: make(map[int]int),
	}
}

type marbleGameScores struct {
	playerScores map[int]int
}

func (o *marbleGameScores) GetScore(player int) int {
	if _, has := o.playerScores[player]; !has {
		return 0
	}
	return o.playerScores[player]
}

func (o *marbleGameScores) GetHighscore() (int, int) {
	leadingPlayer := -1
	maxScore := -1
	for k, v := range o.playerScores {
		if v > maxScore {
			leadingPlayer = k
			maxScore = v
		}
	}
	return leadingPlayer, maxScore
}

func (o *marbleGameScores) IncrementScore(player int, points int) {
	if _, has := o.playerScores[player]; !has {
		o.playerScores[player] = 0
	}
	o.playerScores[player] += points
}
