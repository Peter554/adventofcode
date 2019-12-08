package main

import (
	"testing"
)

func Test_areSameType(t *testing.T) {
	cases := []struct {
		a    byte
		b    byte
		want bool
	}{
		{[]byte("a")[0], []byte("b")[0], false},
		{[]byte("a")[0], []byte("a")[0], true},
		{[]byte("A")[0], []byte("A")[0], true},
		{[]byte("a")[0], []byte("A")[0], true},
		{[]byte("w")[0], []byte("W")[0], true},
	}

	for _, c := range cases {
		get := areSameType(c.a, c.b)

		if get != c.want {
			t.Errorf("(%v, %v) Wanted %v got %v", c.a, c.b, c.want, get)
		}
	}
}

func Test_areOppositePolarity(t *testing.T) {
	cases := []struct {
		a    byte
		b    byte
		want bool
	}{
		{[]byte("a")[0], []byte("b")[0], false},
		{[]byte("a")[0], []byte("a")[0], false},
		{[]byte("a")[0], []byte("A")[0], true},
		{[]byte("W")[0], []byte("W")[0], false},
		{[]byte("V")[0], []byte("v")[0], true},
	}

	for _, c := range cases {
		get := areOppositePolarity(c.a, c.b)

		if get != c.want {
			t.Errorf("(%v, %v) Wanted %v got %v", c.a, c.b, c.want, get)
		}
	}
}

func Test_removePair(t *testing.T) {
	cases := []struct {
		b    []byte
		at   int
		want []byte
	}{
		{[]byte("abcdefg"), 0, []byte("cdefg")},
		{[]byte("abcdefg"), 3, []byte("abcfg")},
	}

	for _, c := range cases {
		get := removePair(c.b, c.at)

		if len(get) != len(c.want) {
			t.Errorf("(%v, %v) Wanted %v got %v", c.b, c.at, c.want, get)
		}

		for i, _ := range get {
			if get[i] != c.want[i] {
				t.Errorf("(%v, %v) Wanted %v got %v", c.b, c.at, c.want, get)
			}
		}
	}
}

func Test_removeUnit(t *testing.T) {
	cases := []struct {
		b    []byte
		unit int
		want []byte
	}{
		{[]byte("abcdeaafg"), 65, []byte("bcdefg")},
		{[]byte("AbcdeaAfg"), 65, []byte("bcdefg")},
		{[]byte("AbcdeaAfg"), 97, []byte("bcdefg")},
		{[]byte("AzbczdezazAzzfgZZ"), 90, []byte("AbcdeaAfg")},
	}

	for _, c := range cases {
		get := removeUnit(c.b, c.unit)

		if len(get) != len(c.want) {
			t.Errorf("(%v, %v) Wanted %v got %v", c.b, c.unit, c.want, get)
			continue
		}

		for i, _ := range get {
			if get[i] != c.want[i] {
				t.Errorf("(%v, %v) Wanted %v got %v", c.b, c.unit, c.want, get)
			}
		}
	}
}

func Test_react(t *testing.T) {
	want := []byte("dabCBAcaDA")

	get := react([]byte("dabAcCaCBAcCcaDA"))

	if len(get) != len(want) {
		t.Errorf("Wanted %v got %v", want, get)
	}

	for i, _ := range get {
		if get[i] != want[i] {
			t.Errorf("Wanted %v got %v", want, get)
		}
	}
}
