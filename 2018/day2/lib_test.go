package main

import "testing"

func Test_letterAppearsExactlyNTimes(t *testing.T) {
	cases := []struct {
		s    string
		n    int
		want bool
	}{
		{"", 2, false},
		{"abc", 2, false},
		{"abcb", 2, true},
		{"abbb", 2, false},
		{"abbb", 3, true},
		{"abaca", 3, true},
		{"bbbb", 3, false},
	}

	for _, c := range cases {
		get := letterAppearsExactlyNTimes(c.s, c.n)

		if get != c.want {
			t.Errorf("Expected %v got %v", c.want, get)
		}
	}
}

func Test_lettersInCommon(t *testing.T) {
	cases := []struct {
		input1      string
		input2      string
		wantCommon  string
		wantRemoved int
		wantError   bool
	}{
		{"foo", "foo", "foo", 0, false},
		{"foo", "fooo", "", 0, true},
		{"foo", "fao", "fo", 1, false},
		{"brtyzg", "batylg", "btyg", 2, false},
	}

	for _, c := range cases {
		getCommon, getRemoved, getError := lettersInCommon(c.input1, c.input2)

		if c.wantError {
			if getError == nil {
				t.Errorf("Expected error")
			}

			continue
		}

		if getCommon != c.wantCommon {
			t.Errorf("Expected %v got %v", c.wantCommon, getCommon)
		}

		if getRemoved != c.wantRemoved {
			t.Errorf("Expected %v got %v", c.wantRemoved, getRemoved)
		}
	}
}
