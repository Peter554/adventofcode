package main

import (
	"testing"
)

func Test_Lines_asInts(t *testing.T) {
	cases := []struct {
		lines   []string
		wantErr bool
		want    []int
	}{
		{[]string{}, false, []int{}},
		{[]string{"42"}, false, []int{42}},
		{[]string{"42", "-3"}, false, []int{42, -3}},
		{[]string{"42", "-3", "Baz"}, true, []int{}},
	}

	for _, c := range cases {
		got, err := asInts(c.lines)

		if c.wantErr {
			if err == nil {
				t.Errorf("%v .asInts() expected error", c.lines)
			}

			continue
		}

		if !c.wantErr && err != nil {
			t.Errorf("%v .asInts() did not expect error", c.lines)
			continue

		}

		if len(got) != len(c.want) {
			t.Errorf("%v .asInts() expected %v. Got %v.", c.lines, c.want, got)
			continue
		}

		for i, v := range got {
			if v != c.want[i] {
				t.Errorf("%v .asInts() expected %v. Got %v.", c.lines, c.want, got)
			}
		}
	}
}

func Test_sum(t *testing.T) {
	cases := []struct {
		input []int
		want  int
	}{
		{[]int{4, -1, 3}, 6},
		{[]int{-5, 8, -1}, 2},
		{[]int{0, 1, -1}, 0},
	}

	for _, c := range cases {
		got := sum(c.input)

		if got != c.want {
			t.Errorf("sum(%v) got %d, wanted %d", c.input, got, c.want)
		}
	}

}

func Test_contains(t *testing.T) {
	cases := []struct {
		arr   []int
		value int
		want  bool
	}{
		{[]int{1, 2, 3}, 2, true},
		{[]int{1, 2, 3}, -1, false},
		{[]int{3, 3, 3}, 3, true},
	}

	for _, c := range cases {
		got := contains(c.arr, c.value)

		if got != c.want {
			t.Errorf("contains(%v, %v) got %v, wanted %v", c.arr, c.value, got, c.want)
		}
	}
}

func Test_firstRepeatingSum(t *testing.T) {
	cases := []struct {
		arr     []int
		want    int
		wantErr bool
	}{
		{[]int{1, 1, -4, 5}, 1, false},
		{[]int{1, 1, 1, 1}, -1, true},
	}

	for _, c := range cases {
		got, err := firstRepeatingSum(c.arr)

		if c.wantErr {
			if err == nil {
				t.Errorf("firstRepeatingSum(%v) expected error", c.arr)
			}

			continue
		}

		if !c.wantErr && err != nil {
			t.Errorf("firstRepeatingSum(%v) did not expect error", c.arr)
			continue
		}

		if got != c.want {
			t.Errorf("firstRepeatingSum(%v) got %v, wanted %v", c.arr, got, c.want)
		}
	}
}
