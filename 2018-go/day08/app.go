package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2018-go/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	ints := processLines(lines)
	tree, _ := readNode(ints, nil)
	fmt.Println(sumMeta(tree))
}

func processLines(lines []string) []int {
	o := make([]int, 0)
	firstLine := lines[0]
	fields := strings.Fields(firstLine)
	for _, v := range fields {
		i, _ := strconv.Atoi(v)
		o = append(o, i)
	}
	return o
}

type Node struct {
	Parent   *Node
	Children []*Node
	Metadata []int
}

func readNode(ints []int, parent *Node) (*Node, int) {
	node := Node{}
	if parent != nil {
		node.Parent = parent
	}
	nChildren := ints[0]
	nMeta := ints[1]
	nRead := 2
	nRead += readChildren(ints[2:], nChildren, &node)
	node.Metadata = ints[nRead : nRead+nMeta]
	nRead += nMeta
	return &node, nRead
}

func readChildren(ints []int, nChildren int, parent *Node) int {
	nReadTotal := 0
	children := make([]*Node, 0)
	for len(children) < nChildren {
		child, nRead := readNode(ints, parent)
		children = append(children, child)
		ints = ints[nRead:]
		nReadTotal += nRead
	}
	parent.Children = children
	return nReadTotal
}

func sumMeta(node *Node) int {
	o := 0
	for _, meta := range node.Metadata {
		o += meta
	}
	for _, child := range node.Children {
		o += sumMeta(child)
	}
	return o
}
