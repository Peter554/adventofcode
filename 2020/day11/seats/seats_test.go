package seats

import (
	"testing"

	"github.com/peter554/adventofcode/2020/lib"
)

func TestSeats(t *testing.T) {
	lines := lib.TestLines(`
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL`)

	lib.Expect(t, New(lines, 1, 4).Evolve().CountOccupied(), 37)
	lib.Expect(t, New(lines, -1, 5).Evolve().CountOccupied(), 26)
}
