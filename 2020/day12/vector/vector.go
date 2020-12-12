package vector

type Vector struct {
	X int
	Y int
}

func New(x, y int) *Vector {
	return &Vector{X: x, Y: y}
}

func (v *Vector) Copy() *Vector {
	return &Vector{X: v.X, Y: v.Y}
}

func (v *Vector) Add(x, y int) *Vector {
	v.X += x
	v.Y += y
	return v
}

func (v *Vector) Multiply(i int) *Vector {
	v.X *= i
	v.Y *= i
	return v
}

func (v *Vector) RotateBy90() *Vector {
	t := v.X
	v.X = -v.Y
	v.Y = t
	return v
}

func (v *Vector) Manhattan() int {
	abs := func(i int) int {
		if i < 0 {
			return -i
		}
		return i
	}
	return abs(v.X) + abs(v.Y)
}
