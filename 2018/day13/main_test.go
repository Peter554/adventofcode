package main

import "testing"

func Test_findcrash(t *testing.T) {
	input := []string{
		"/->-\\        ",
		"|   |  /----\\",
		"| /-+--+-\\  |",
		"| | |  | v  |",
		"\\-+-/  \\-+--/",
		"  \\------/   ",
	}
	crash := findcrash(parseinput(input))
	if (crash != point{7, 3}) {
		t.Errorf("Expected crash at (7, 3), found crash at (%d, %d)", crash.x, crash.y)
	}
}

func Test_findlastcart(t *testing.T) {
	input := []string{
		"/>-<\\  ",
		"|   |  ",
		"| /<+-\\",
		"| | | v",
		"\\>+</ |",
		"  |   ^",
		"  \\<->/",
	}
	_, p := findlastcart(parseinput(input))
	if (p != point{6, 4}) {
		t.Errorf("Expected last cart at (6, 4), found last cart at (%d, %d)", p.x, p.y)
	}
}
