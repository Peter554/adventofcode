package parse

import (
	"testing"
)

func Test_Parse(t *testing.T) {
	cases := []struct {
		line     string
		parent   string
		children map[string]int
	}{
		{
			line:   "muted white bags contain 4 dark orange bags, 3 bright white bags.",
			parent: "muted white",
			children: map[string]int{
				"dark orange":  4,
				"bright white": 3,
			},
		},
		{
			line:   "bright salmon bags contain 5 light indigo bags.",
			parent: "bright salmon",
			children: map[string]int{
				"light indigo": 5,
			},
		},
		{
			line:     "dim salmon bags contain no other bags.",
			parent:   "dim salmon",
			children: map[string]int{},
		},
		{
			line:   "plaid green bags contain 5 drab indigo bags, 4 vibrant gray bags, 1 vibrant chartreuse bag, 5 mirrored lavender bags.",
			parent: "plaid green",
			children: map[string]int{
				"drab indigo":        5,
				"vibrant gray":       4,
				"vibrant chartreuse": 1,
				"mirrored lavender":  5,
			},
		},
	}

	for _, c := range cases {
		t.Run(c.line, func(t *testing.T) {
			parent, children := Parse(c.line)
			if c.parent != parent {
				t.Errorf("Expected \"%v\", got \"%v\"", c.parent, parent)
				return
			}
			for wantK, wantV := range c.children {
				gotV, exists := children[wantK]
				if !exists {
					t.Errorf("\"%v\" not found in %v", wantK, children)
					return
				}
				if wantV != gotV {
					t.Errorf("Expected \"%v\" to have value %v in %v", wantK, wantV, children)
				}
			}
		})
	}
}
