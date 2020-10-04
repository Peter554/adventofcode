package main

import "testing"

func Test_cook(t *testing.T) {
	cases := []struct {
		n    int
		want string
	}{
		{9, "5158916779"},
		{5, "0124515891"},
		{18, "9251071085"},
		{2018, "5941429882"},
	}

	for _, c := range cases {
		got := cook(c.n)
		if got != c.want {
			t.Errorf("Expected cook(%d) to be %s, got %s", c.n, c.want, got)
		}
	}
}

func Test_cook2(t *testing.T) {
	cases := []struct {
		ns   []uint8
		want int
	}{
		{[]uint8{5, 1, 5, 8, 9}, 9},
		{[]uint8{0, 1, 2, 4, 5}, 5},
		{[]uint8{9, 2, 5, 1, 0}, 18},
		{[]uint8{5, 9, 4, 1, 4}, 2018},
	}

	for _, c := range cases {
		got := cook2(c.ns)
		if got != c.want {
			t.Errorf("Expected cook2(%d) to be %d, got %d", c.ns, c.want, got)
		}
	}
}
