package main

import (
	"fmt"
	"regexp"
	"sort"

	"github.com/peter554/adventofcode/2018-go/common"
)

func main() {
	lines := common.Readlines("./input.txt")

	steps := NewSteps()
	for _, line := range lines {
		steps.AddDependency(getDependency(line))
	}
	fmt.Println(steps.GetOrder())
}

type Dependency struct {
	Step      string
	DependsOn string
}

type Steps interface {
	AddDependency(dependency Dependency)
	GetOrder() []string
}

func NewSteps() Steps {
	return &basicSteps{
		state: make(map[string][]string),
	}
}

type basicSteps struct {
	state map[string][]string
}

func (o *basicSteps) AddDependency(dependency Dependency) {
	if _, ok := o.state[dependency.Step]; !ok {
		o.state[dependency.Step] = make([]string, 0)
	}
	if _, ok := o.state[dependency.DependsOn]; !ok {
		o.state[dependency.DependsOn] = make([]string, 0)
	}
	o.state[dependency.Step] = append(o.state[dependency.Step], dependency.DependsOn)
}

func (a *basicSteps) GetOrder() []string {
	o := make([]string, 0)
	clone := a.cloneState()
	for {
		next := a.getNext(clone)
		if next == "done" {
			break
		}
		o = append(o, next)
		clone = a.removeStep(clone, next)
	}
	return o
}

func (a *basicSteps) cloneState() map[string][]string {
	o := make(map[string][]string)
	for k, v := range a.state {
		o[k] = a.cloneSlice(v)
	}
	return o
}

func (*basicSteps) cloneSlice(s []string) []string {
	o := make([]string, 0)
	for _, v := range s {
		o = append(o, v)
	}
	return o
}

func (*basicSteps) getNext(state map[string][]string) string {
	o := make([]string, 0)
	for k, v := range state {
		if len(v) == 0 {
			o = append(o, k)
		}
	}
	if len(o) == 0 {
		return "done"
	}
	sort.Strings(o)
	return o[0]
}

func (*basicSteps) removeStep(state map[string][]string, step string) map[string][]string {
	delete(state, step)
	for k, v := range state {
		state[k] = filter(v, func(s string) bool {
			return s != step
		})
	}
	return state
}

func getDependency(line string) Dependency {
	re := regexp.MustCompile(`Step ([A-Z]) must be finished before step ([A-Z]) can begin.`)
	match := re.FindStringSubmatch(line)
	return Dependency{
		Step:      match[2],
		DependsOn: match[1],
	}
}

func filter(a []string, f func(string) bool) []string {
	o := make([]string, 0)
	for _, v := range a {
		if f(v) {
			o = append(o, v)
		}
	}
	return o
}
