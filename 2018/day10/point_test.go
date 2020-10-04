package main

import "testing"

func TestPoint(t *testing.T) {
	line := "position=< 51730, -30721> velocity=<-5,  3>"
	point := NewPoint(line)

	x, y := point.GetPosition()
	if x != 51730 {
		t.Error()
	}
	if y != -30721 {
		t.Error()
	}

	point.Step()
	x, y = point.GetPosition()
	if x != 51725 {
		t.Error()
	}
	if y != -30718 {
		t.Error()
	}
}
