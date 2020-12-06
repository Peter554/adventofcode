package computer

import "fmt"

func New(ipr int) *Computer {
	return &Computer{0, ipr, []int{0, 0, 0, 0, 0, 0}}
}

type Computer struct {
	ip   int
	ipr  int
	data []int
}

func (c *Computer) String() string {
	return fmt.Sprintf("%v", c.data)
}

func (c *Computer) Run(instructions [][]int) {
	instructionMap := map[int]func(data []int, a, b, c int){
		0: func(data []int, a, b, c int) {
			if a == data[b] {
				data[c] = 1
			} else {
				data[c] = 0
			}
		},
		1: func(data []int, a, b, c int) {
			data[c] = data[a] | data[b]
		},
		2: func(data []int, a, b, c int) {
			data[c] = data[a] + data[b]
		},
		3: func(data []int, a, b, c int) {
			if data[a] > b {
				data[c] = 1
			} else {
				data[c] = 0
			}
		},
		4: func(data []int, a, b, c int) {
			data[c] = data[a] * b
		},
		5: func(data []int, a, b, c int) {
			if a > data[b] {
				data[c] = 1
			} else {
				data[c] = 0
			}
		},
		6: func(data []int, a, b, c int) {
			data[c] = data[a] * data[b]
		},
		7: func(data []int, a, b, c int) {
			data[c] = data[a] & data[b]
		},
		8: func(data []int, a, b, c int) {
			data[c] = data[a] | b
		},
		9: func(data []int, a, b, c int) {
			if data[a] == b {
				data[c] = 1
			} else {
				data[c] = 0
			}
		},
		10: func(data []int, a, b, c int) {
			if data[a] == data[b] {
				data[c] = 1
			} else {
				data[c] = 0
			}
		},
		11: func(data []int, a, b, c int) {
			data[c] = data[a] & b
		},
		12: func(data []int, a, b, c int) {
			data[c] = data[a]
		},
		13: func(data []int, a, b, c int) {
			if data[a] > data[b] {
				data[c] = 1
			} else {
				data[c] = 0
			}
		},
		14: func(data []int, a, b, c int) {
			data[c] = data[a] + b
		},
		15: func(data []int, a, b, c int) {
			data[c] = a
		},
	}

	for c.ip < len(instructions) {
		c.data[c.ipr] = c.ip
		instruction := instructions[c.ip]
		instructionMap[instruction[0]](c.data, instruction[1], instruction[2], instruction[3])
		c.ip = c.data[c.ipr]
		c.ip++
	}
}
