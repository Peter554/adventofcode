package main

import (
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	lib.Result{Part: 2, Value: Part2(lines)}.Print()
}

func Part1(lines []string) int {
	checksum, _ := buildPuzzle(lines)
	return checksum
}

func Part2(lines []string) int {
	return 42
}

type Tile struct {
	ID     int
	data   []string
	Top    *Tile
	Bottom *Tile
	Left   *Tile
	Right  *Tile
}

func (t *Tile) Rotate() *Tile {
	t.data = rotate(t.data)
	return t
}

func (t *Tile) Flip() *Tile {
	t.data = flip(t.data)
	return t
}

func (t *Tile) Trim() {
	data := []string{}
	for i := 1; i < len(t.data)-1; i++ {
		line := t.data[i]
		data = append(data, line[1:len(line)-1])
	}
	t.data = data
}

func (t *Tile) Data() []string {
	return t.data
}

func (t *Tile) Matches(other *Tile, direction string) bool {
	if direction == "top" {
		return t.data[0] == other.data[len(other.data)-1]
	}
	if direction == "bottom" {
		return t.data[len(t.data)-1] == other.data[0]
	}
	if direction == "left" {
		return col(t.data, 0) == col(other.data, len(other.data[0])-1)
	}
	if direction == "right" {
		return col(t.data, len(t.data[0])-1) == col(other.data, 0)
	}
	return false
}

func parseTile(lines []string) *Tile {
	id := lib.AsInt(lib.RE(`Tile (\d+):`).Groups(lines[0])[0])
	return &Tile{
		ID:   id,
		data: lines[1:],
	}
}

func buildPuzzle(lines []string) (cornerCheckSum int, puzzle []string) {
	unconnected := map[*Tile]bool{}
	connected := map[*Tile]bool{}
	visited := map[*Tile]bool{}

	for idx, tileString := range strings.Split(strings.Join(lines, "\n"), "\n\n") {
		tile := parseTile(strings.Split(tileString, "\n"))
		if idx == 0 {
			connected[tile] = true
			visited[tile] = false
		} else {
			unconnected[tile] = true
		}
	}

	connect := func(t *Tile) {
		for tile := range connected {
			if t.Matches(tile, "top") {
				t.Top = tile
				tile.Bottom = t
			}
			if t.Matches(tile, "bottom") {
				t.Bottom = tile
				tile.Top = t
			}
			if t.Matches(tile, "left") {
				t.Left = tile
				tile.Right = t
			}
			if t.Matches(tile, "right") {
				t.Right = tile
				tile.Left = t
			}
		}
		connected[t] = true
		visited[t] = false
		delete(unconnected, t)
	}

	transforms := []func(t *Tile){
		func(t *Tile) {},
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate().Flip() },
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate().Flip().Rotate().Flip() },
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate() },
		func(t *Tile) { t.Rotate() },
	}

	for {
		var visiting *Tile

		for tile, visited := range visited {
			if !visited {
				visiting = tile
				break
			}
		}

		if visiting == nil {
			break
		}

		if visiting.Top == nil {
		outerTop:
			for otherTile := range unconnected {
				for _, transform := range transforms {
					transform(otherTile)
					if visiting.Matches(otherTile, "top") {
						connect(otherTile)
						break outerTop
					}
				}
			}
		}

		if visiting.Bottom == nil {
		outerBottom:
			for otherTile := range unconnected {
				for _, transform := range transforms {
					transform(otherTile)
					if visiting.Matches(otherTile, "bottom") {
						connect(otherTile)
						break outerBottom
					}
				}
			}
		}

		if visiting.Left == nil {
		outerLeft:
			for otherTile := range unconnected {
				for _, transform := range transforms {
					transform(otherTile)
					if visiting.Matches(otherTile, "left") {
						connect(otherTile)
						break outerLeft
					}
				}
			}
		}

		if visiting.Right == nil {
		outerRight:
			for otherTile := range unconnected {
				for _, transform := range transforms {
					transform(otherTile)
					if visiting.Matches(otherTile, "right") {
						connect(otherTile)
						break outerRight
					}
				}
			}
		}

		visited[visiting] = true
	}

	cornerCheckSum = 1
	var topLeft *Tile
	for tile := range connected {
		count := 0
		if tile.Top != nil {
			count++
		}
		if tile.Bottom != nil {
			count++
		}
		if tile.Left != nil {
			count++
		}
		if tile.Right != nil {
			count++
		}
		if count == 2 {
			cornerCheckSum *= tile.ID
			if tile.Top == nil && tile.Left == nil {
				topLeft = tile
			}
		}
	}

	for tile := range connected {
		tile.Trim()
	}

	puzzle = []string{}

	left := topLeft
	current := topLeft
	for left != nil {
		part := []string{}
		for i := 0; i < len(current.Data()); i++ {
			part = append(part, "")
		}
		for current != nil {
			for idx, line := range current.Data() {
				part[idx] += line
			}
			current = current.Right
		}
		left = left.Bottom
		current = left
		puzzle = append(puzzle, part...)
	}

	return
}

func col(a []string, i int) string {
	o := ""
	for _, row := range a {
		o += string(row[i])
	}
	return o
}

func reverse(s string) string {
	o := ""
	for i := len(s) - 1; i >= 0; i-- {
		o += string(s[i])
	}
	return o
}

func flip(s []string) []string {
	data := []string{}
	for i := 0; i < len(s); i++ {
		data = append(data, s[len(s)-1-i])
	}
	return data
}

func rotate(s []string) []string {
	data := []string{}
	for i := 0; i < len(s[0]); i++ {
		data = append(data, col(s, len(s[0])-1-i))
	}
	return data
}
