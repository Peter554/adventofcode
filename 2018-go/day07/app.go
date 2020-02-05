package main

import (
	"fmt"
	"regexp"
	"sort"
	"strings"

	"github.com/peter554/adventofcode/2018-go/common"
)

func main() {
	lines := common.Readlines("./input.txt")

	steps := NewSteps()
	for _, line := range lines {
		steps.AddDependency(getDependency(line))
	}

	fmt.Println(strings.Join(steps.GetOrder(), ""))

	inProgress := make([]string, 0)
	completed := make([]string, 0)
	workers := [5]Worker{NewWorker(), NewWorker(), NewWorker(), NewWorker(), NewWorker()}
	time := 0
	for {
		if steps.IsDone(completed) {
			break
		}

		availableJobs := steps.GetAvailableJobs(inProgress, completed)
		for _, job := range availableJobs {
			for _, w := range workers {
				if w.IsAvailable() {
					w.Accept(job)
					inProgress = append(inProgress, job)
					break
				}
			}
		}

		for _, w := range workers {
			done := w.Tick()
			if done != "none" {
				inProgress = filter(inProgress, func(s string) bool {
					return s != done
				})
				completed = append(completed, done)
			}
		}
		time++
	}
	fmt.Println(time)
}

type Dependency struct {
	Step      string
	DependsOn string
}

type Steps interface {
	AddDependency(dependency Dependency)
	GetOrder() []string
	IsDone(completed []string) bool
	GetAvailableJobs(inProgress []string, completed []string) []string
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
		if next == "none" {
			break
		}
		o = append(o, next)
		clone = a.removeStep(clone, next)
	}
	return o
}

func (a *basicSteps) IsDone(completed []string) bool {
	clone := a.cloneState()
	for _, v := range completed {
		clone = a.removeStep(clone, v)
	}
	keyCount := 0
	for range clone {
		keyCount++
	}
	return keyCount == 0
}

func (a *basicSteps) GetAvailableJobs(inProgress []string, completed []string) []string {
	clone := a.cloneState()
	for _, v := range inProgress {
		clone = a.removeKey(clone, v)
	}
	for _, v := range completed {
		clone = a.removeStep(clone, v)
	}
	keys := make([]string, 0)
	for k, v := range clone {
		if len(v) == 0 {
			keys = append(keys, k)
		}
	}
	sort.Strings(keys)
	return keys
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
		return "none"
	}
	sort.Strings(o)
	return o[0]
}

func (*basicSteps) removeKey(state map[string][]string, step string) map[string][]string {
	delete(state, step)
	return state
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

type Worker interface {
	IsAvailable() bool
	Accept(job string)
	Tick() string
}

func NewWorker() Worker {
	return &worker{counter: 0, currentJob: "none"}
}

type worker struct {
	counter    int
	currentJob string
}

func (o *worker) IsAvailable() bool {
	return o.counter <= 0
}

func (o *worker) Accept(job string) {
	o.counter = int(job[0]) - 64 + 60
	o.currentJob = job
}

func (o *worker) Tick() string {
	o.counter--
	if o.counter == 0 {
		completedJob := o.currentJob
		o.currentJob = "none"
		return completedJob
	}
	return "none"
}
