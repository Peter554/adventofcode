package main

import "testing"

func TestExample1(t *testing.T) {
	ints := []int{2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2}
	tree, _ := readNode(ints, nil)
	get := sumMeta(tree)
	want := 138
	if get != want {
		t.Errorf("got %v want %v", get, want)
	}
}

func TestExample2(t *testing.T) {
	ints := []int{2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2}
	tree, _ := readNode(ints, nil)
	get := getValue(tree)
	want := 66
	if get != want {
		t.Errorf("got %v want %v", get, want)
	}
}
