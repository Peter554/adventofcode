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
	input := Parse(lines)
	_, sumBadValues := getBadTickets(input)
	return sumBadValues
}

func Part2(lines []string) int {
	input := Parse(lines)

	idxs, _ := getBadTickets(input)
	input.RemoveTickets(idxs)

	fieldToPossibleIdx := map[string]map[int]bool{}
	for _, field := range input.Fields {
		idxs := map[int]bool{}
		for idx := range input.OtherTickets[0] {
			idxs[idx] = true
		}
		for _, ticket := range input.OtherTickets {
			for idx, i := range ticket {
				idxs[idx] = idxs[idx] && field.IsValid(i)
			}
		}
		fieldToPossibleIdx[field.Name] = idxs
	}

	fieldToIdx := map[string]int{}
	for {
		idx := -1
		for field, possibleIdx := range fieldToPossibleIdx {
			if size(possibleIdx) == 1 {
				idx = toSlice(possibleIdx)[0]
				fieldToIdx[field] = idx
			}
		}

		if idx < 0 {
			break

		}

		for _, possibleIdx := range fieldToPossibleIdx {
			possibleIdx[idx] = false
		}
	}

	o := 1
	for _, field := range input.Fields {
		if strings.HasPrefix(field.Name, "departure ") {
			o *= input.MyTicket[fieldToIdx[field.Name]]
		}
	}
	return o
}

type Input struct {
	Fields       []Field
	MyTicket     []int
	OtherTickets [][]int
}

func (i *Input) RemoveTickets(idxs []int) {
	m := map[int]bool{}
	for _, idx := range idxs {
		m[idx] = true
	}
	otherTickets := [][]int{}
	for idx, ticket := range i.OtherTickets {
		if _, exists := m[idx]; exists {
			continue
		}
		otherTickets = append(otherTickets, ticket)
	}
	i.OtherTickets = otherTickets
}

type Field struct {
	Name string
	r    []int
}

func (f Field) IsValid(i int) bool {
	return (i >= f.r[0] && i <= f.r[1]) || (i >= f.r[2] && i <= f.r[3])
}

func Parse(lines []string) Input {
	parts := strings.Split(strings.Join(lines, "\n"), "\n\n")

	fields := []Field{}
	for _, line := range strings.Split(parts[0], "\n") {
		groups := lib.RE(`^([a-z\s]+): (\d+)-(\d+) or (\d+)-(\d+)$`).Groups(line)
		fields = append(fields, Field{
			Name: groups[0],
			r:    []int{lib.AsInt(groups[1]), lib.AsInt(groups[2]), lib.AsInt(groups[3]), lib.AsInt(groups[4])},
		})
	}

	myTicket := []int{}
	for _, s := range strings.Split(strings.Split(parts[1], "\n")[1], ",") {
		myTicket = append(myTicket, lib.AsInt(s))
	}

	otherTickets := [][]int{}
	for _, line := range strings.Split(parts[2], "\n")[1:] {
		otherTicket := []int{}
		for _, s := range strings.Split(line, ",") {
			otherTicket = append(otherTicket, lib.AsInt(s))
		}
		otherTickets = append(otherTickets, otherTicket)
	}

	return Input{
		Fields:       fields,
		MyTicket:     myTicket,
		OtherTickets: otherTickets,
	}
}

func getBadTickets(input Input) (idxs []int, sumBadValues int) {
	idxs, sumBadValues = []int{}, 0
	for idx, ticket := range input.OtherTickets {
		badTicket := false
		for _, i := range ticket {
			validity := map[bool]int{true: 0, false: 0}
			for _, field := range input.Fields {
				validity[field.IsValid(i)]++
			}
			if validity[true] == 0 {
				badTicket = true
				sumBadValues += i
			}
		}
		if badTicket {
			idxs = append(idxs, idx)
		}
	}
	return
}

func size(m map[int]bool) int {
	o := 0
	for _, v := range m {
		if v {
			o++
		}
	}
	return o
}

func toSlice(m map[int]bool) []int {
	o := []int{}
	for k, v := range m {
		if v {
			o = append(o, k)
		}
	}
	return o
}
