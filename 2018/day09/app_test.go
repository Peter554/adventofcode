package main

import "testing"

func TestRunMarbleGame(t *testing.T) {
	cases := []struct {
		nPlayers   int
		lastMarble int
		wantPlayer int
		wantScore  int
	}{
		{9, 25, 5, 32},
		{10, 1618, -1, 8317},
		{13, 7999, -1, 146373},
		{17, 1104, -1, 2764},
		{21, 6111, -1, 54718},
		{30, 5807, -1, 37305},
	}

	for _, c := range cases {
		getPlayer, getScore := runMarbleGame(c.nPlayers, c.lastMarble)

		if c.wantPlayer >= 0 && getPlayer != c.wantPlayer {
			t.Errorf("Expected player %v, got player %v", c.wantPlayer, getPlayer)
		}

		if getScore != c.wantScore {
			t.Errorf("Expected score %v, got score %v", c.wantScore, getScore)
		}
	}
}
