package main

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"github.com/peter554/adventofcode/2018/common"
)

func main() {
	lines := common.Readlines("./input1.txt")
	examples := getExamples(lines)

	count := 0
	for _, ex := range examples {
		a, _ := runExample(ex)
		if a >= 3 {
			count++
		}
	}
	fmt.Println(count)

	// for i := 0; i <= 15; i++ {
	// 	ss := strset{map[string]bool{}}
	// 	for _, ex := range examples {
	// 		if ex.cmd[0] == i {
	// 			_, b := runExample(ex)
	// 			for _, v := range b {
	// 				if !contains([]string{
	// 					"eqir",
	// 					"eqri",
	// 					"eqrr",
	// 					"gtri",
	// 					"gtrr",
	// 					"gtir",
	// 					"setr",
	// 					"banr",
	// 					"bani",
	// 					"seti",
	// 					"mulr",
	// 					"addr",
	// 					"addi",
	// 					"bonr",
	// 					"boni",
	// 					"muli",
	// 				}, v) {
	// 					ss.add(v)
	// 				}
	// 			}
	// 		}
	// 	}
	// 	fmt.Printf("%d %s\n", i, ss.values())
	// }

	lines = common.Readlines("./input2.txt")
	commands := [][]int{}
	for _, v := range lines {
		commands = append(commands, getCmd(v))
	}
	fmt.Println(runProgram([]int{0, 0, 0, 0}, commands))
}

func runProgram(input []int, commands [][]int) []int {
	ops := map[int]Opcode{
		0:  eqir{},
		1:  bonr{},
		2:  addr{},
		3:  gtri{},
		4:  muli{},
		5:  gtir{},
		6:  mulr{},
		7:  banr{},
		8:  boni{},
		9:  eqri{},
		10: eqrr{},
		11: bani{},
		12: setr{},
		13: gtrr{},
		14: addi{},
		15: seti{},
	}

	o := clone(input)
	for _, cmd := range commands {
		ops[cmd[0]].Act(o, cmd)
	}
	return o
}

func contains(a []string, s string) bool {
	for _, v := range a {
		if v == s {
			return true
		}
	}
	return false
}

type strset struct {
	data map[string]bool
}

func (ss *strset) add(s string) {
	ss.data[s] = true
}

func (ss *strset) values() []string {
	o := []string{}
	for k := range ss.data {
		o = append(o, k)
	}
	return o
}

type example struct {
	before []int
	cmd    []int
	after  []int
}

func getExamples(lines []string) []example {
	examples := []example{}
	rawExample := []string{}
	for idx, line := range lines {
		rawExample = append(rawExample, line)
		if idx%4 == 3 {
			ex := example{
				getBefore(rawExample[0]),
				getCmd(rawExample[1]),
				getAfter(rawExample[2]),
			}
			examples = append(examples, ex)
			rawExample = []string{}
		}
	}
	if len(rawExample) > 0 {
		ex := example{
			getBefore(rawExample[0]),
			getCmd(rawExample[1]),
			getAfter(rawExample[2]),
		}
		examples = append(examples, ex)
	}
	return examples
}

func getBefore(s string) []int {
	o := []int{}
	for _, v := range strings.Split(regexp.MustCompile(`\[(.*)\]`).FindStringSubmatch(s)[1], ",") {
		i, _ := strconv.Atoi(strings.TrimSpace(v))
		o = append(o, i)
	}
	return o
}

func getCmd(s string) []int {
	o := []int{}
	for _, v := range strings.Split(s, " ") {
		i, _ := strconv.Atoi(strings.TrimSpace(v))
		o = append(o, i)
	}
	return o
}

func getAfter(s string) []int {
	o := []int{}
	for _, v := range strings.Split(regexp.MustCompile(`\[(.*)\]`).FindStringSubmatch(s)[1], ",") {
		i, _ := strconv.Atoi(strings.TrimSpace(v))
		o = append(o, i)
	}
	return o
}

func runExample(ex example) (int, []string) {
	opcodes := []Opcode{
		addr{}, addi{},
		mulr{}, muli{},
		banr{}, bani{},
		bonr{}, boni{},
		setr{}, seti{},
		gtir{}, gtri{}, gtrr{},
		eqir{}, eqri{}, eqrr{}}

	o := []string{}
	for _, opcode := range opcodes {
		data := clone(ex.before)
		opcode.Act(data, ex.cmd)
		if equal(data, ex.after) {
			o = append(o, opcode.Name())
		}
	}
	return len(o), o
}

func clone(a []int) []int {
	o := []int{}
	for _, v := range a {
		o = append(o, v)
	}
	return o
}

func equal(a []int, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if b[i] != v {
			return false
		}
	}
	return true
}

type Opcode interface {
	Name() string
	Act(data []int, cmd []int)
}

// addr

type addr struct{}

func (o addr) Name() string {
	return "addr"
}

func (o addr) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] + data[cmd[2]]
}

// addi

type addi struct{}

func (o addi) Name() string {
	return "addi"
}

func (o addi) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] + cmd[2]
}

// mulr

type mulr struct{}

func (o mulr) Name() string {
	return "mulr"
}

func (o mulr) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] * data[cmd[2]]
}

// muli

type muli struct{}

func (o muli) Name() string {
	return "muli"
}

func (o muli) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] * cmd[2]
}

// banr

type banr struct{}

func (o banr) Name() string {
	return "banr"
}

func (o banr) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] & data[cmd[2]]
}

// bani

type bani struct{}

func (o bani) Name() string {
	return "bani"
}

func (o bani) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] & cmd[2]
}

// bonr

type bonr struct{}

func (o bonr) Name() string {
	return "bonr"
}

func (o bonr) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] | data[cmd[2]]
}

// boni

type boni struct{}

func (o boni) Name() string {
	return "boni"
}

func (o boni) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]] | cmd[2]
}

// setr

type setr struct{}

func (o setr) Name() string {
	return "setr"
}

func (o setr) Act(data []int, cmd []int) {
	data[cmd[3]] = data[cmd[1]]
}

// seti

type seti struct{}

func (o seti) Name() string {
	return "seti"
}

func (o seti) Act(data []int, cmd []int) {
	data[cmd[3]] = cmd[1]
}

// gtir

type gtir struct{}

func (o gtir) Name() string {
	return "gtir"
}

func (o gtir) Act(data []int, cmd []int) {
	if cmd[1] > data[cmd[2]] {
		data[cmd[3]] = 1
	} else {
		data[cmd[3]] = 0
	}
}

// gtri

type gtri struct{}

func (o gtri) Name() string {
	return "gtri"
}

func (o gtri) Act(data []int, cmd []int) {
	if data[cmd[1]] > cmd[2] {
		data[cmd[3]] = 1
	} else {
		data[cmd[3]] = 0
	}
}

// gtrr

type gtrr struct{}

func (o gtrr) Name() string {
	return "gtrr"
}

func (o gtrr) Act(data []int, cmd []int) {
	if data[cmd[1]] > data[cmd[2]] {
		data[cmd[3]] = 1
	} else {
		data[cmd[3]] = 0
	}
}

// eqir

type eqir struct{}

func (o eqir) Name() string {
	return "eqir"
}

func (o eqir) Act(data []int, cmd []int) {
	if cmd[1] == data[cmd[2]] {
		data[cmd[3]] = 1
	} else {
		data[cmd[3]] = 0
	}
}

// eqri

type eqri struct{}

func (o eqri) Name() string {
	return "eqri"
}

func (o eqri) Act(data []int, cmd []int) {
	if data[cmd[1]] == cmd[2] {
		data[cmd[3]] = 1
	} else {
		data[cmd[3]] = 0
	}
}

// eqrr

type eqrr struct{}

func (o eqrr) Name() string {
	return "eqrr"
}

func (o eqrr) Act(data []int, cmd []int) {
	if data[cmd[1]] == data[cmd[2]] {
		data[cmd[3]] = 1
	} else {
		data[cmd[3]] = 0
	}
}
