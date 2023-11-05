package main

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/peter554/adventofcode/2020/go/lib"
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
	transforms := []func(s []string) []string{
		func(s []string) []string { return s },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return flip(rotate(s)) },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return flip(rotate(flip(rotate(s)))) },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return rotate(s) },
		func(s []string) []string { return rotate(s) },
	}

	_, puzzle := buildPuzzle(lines)

	hashCount := 0
	for _, line := range puzzle {
		for _, char := range line {
			if char == '#' {
				hashCount++
			}
		}
	}

	seaMonsterCount := 0
	for _, transform := range transforms {
		puzzle = transform(puzzle)
		seaMonsterCount = countSeaMonsters(puzzle)
		if seaMonsterCount > 0 {
			break
		}
	}

	return hashCount - seaMonsterCount*15
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

	for idx, tileString := range strings.Split(strings.Join(lines, "\n"), "\n\n") {
		tile := parseTile(strings.Split(tileString, "\n"))
		if idx == 0 {
			connected[tile] = true
		} else {
			unconnected[tile] = true
		}
	}

	tryConnect := func(t *Tile) bool {
		didConnect := false
		for tile := range connected {
			if t.Matches(tile, "top") {
				t.Top = tile
				tile.Bottom = t
				didConnect = true
			}
			if t.Matches(tile, "bottom") {
				t.Bottom = tile
				tile.Top = t
				didConnect = true
			}
			if t.Matches(tile, "left") {
				t.Left = tile
				tile.Right = t
				didConnect = true
			}
			if t.Matches(tile, "right") {
				t.Right = tile
				tile.Left = t
				didConnect = true
			}
		}
		if didConnect {
			connected[t] = true
			delete(unconnected, t)
		}
		return didConnect
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

	for len(unconnected) > 0 {
		for tile := range unconnected {
			for _, transform := range transforms {
				transform(tile)
				if tryConnect(tile) {
					break
				}
			}
		}
	}

	cornerCheckSum = 1
	var topLeft *Tile
	for tile := range connected {
		connectionsCount := 0
		if tile.Top != nil {
			connectionsCount++
		}
		if tile.Bottom != nil {
			connectionsCount++
		}
		if tile.Left != nil {
			connectionsCount++
		}
		if tile.Right != nil {
			connectionsCount++
		}
		if connectionsCount == 2 {
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

func countSeaMonsters(puzzle []string) int {
	count := 0
	re := regexp.MustCompile(fmt.Sprintf(`#[#\.\n]{%[1]d}#[#\.]{4}##[#\.]{4}##[#\.]{4}###[#\.\n]{%[1]d}#[#\.]{2}#[#\.]{2}#[#\.]{2}#[#\.]{2}#[#\.]{2}#`, len(puzzle[0])-18))
	s := strings.Join(puzzle, "\n")
	for {
		match := re.FindStringIndex(s)
		if match == nil {
			break
		}
		count++
		s = s[match[0]+1:]
	}
	return count
}
