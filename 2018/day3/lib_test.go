package main

import "testing"

func Test_getClaim(t *testing.T) {
	cases := []struct {
		input string
		want  claim
	}{
		{"#6 @ 466,619: 19x13", claim{6, coordinate{466, 619}, 19, 13}},
		{"#28 @ 662,127: 25x12", claim{28, coordinate{662, 127}, 25, 12}},
		{"#168 @ 196,236: 19x24", claim{168, coordinate{196, 236}, 19, 24}},
	}

	for _, c := range cases {
		get, err := getClaim(c.input)

		if err != nil {
			t.Errorf("Got unexpected error")
			continue
		}

		if get.id != c.want.id {
			t.Errorf("Got %v expected %v", get, c.want)
		}

		if get.topleft.x != c.want.topleft.x {
			t.Errorf("Got %v expected %v", get, c.want)
		}

		if get.topleft.y != c.want.topleft.y {
			t.Errorf("Got %v expected %v", get, c.want)
		}

		if get.width != c.want.width {
			t.Errorf("Got %v expected %v", get, c.want)
		}

		if get.height != c.want.height {
			t.Errorf("Got %v expected %v", get, c.want)
		}
	}
}

func Test_addClaimToMap(t *testing.T) {
	m := make(map[coordinate]int)
	c := claim{1, coordinate{2, 3}, 3, 2}

	addClaimToMap(m, c)

	for i := 0; i < 10; i++ {
		for j := 0; j < 10; j++ {
			switch {
			case (i >= 2) && (i <= 4) && (j >= 3) && (j <= 4):
				if m[coordinate{i, j}] != 1 {
					t.Errorf("Expected m(%v, %v) to be 1", i, j)
				}
			default:
				if m[coordinate{i, j}] != 0 {
					t.Errorf("Expected m(%v, %v) to be 0", i, j)
				}
			}
		}
	}
}

func Test_overlaps(t *testing.T) {
	cases := []struct {
		this  claim
		other claim
		want  bool
	}{
		{
			claim{1, coordinate{1, 1}, 3, 3},
			claim{2, coordinate{5, 3}, 2, 3},
			false,
		},
		{
			claim{1, coordinate{1, 1}, 3, 3},
			claim{2, coordinate{2, 3}, 2, 3},
			true,
		},
	}

	for _, c := range cases {
		get := c.this.overlaps(c.other)

		if get != c.want {
			t.Errorf("Expected %v got %v", c.want, get)
		}
	}
}
