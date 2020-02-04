package main

import (
	"regexp"
	"sort"
	"strconv"

	"github.com/peter554/adventofcode/2018-go/common"
)

func main() {
	lines := common.Readlines("./input.txt")
	sort.Strings(lines)

	currentGuard := -1
	isAsleep := false
	previousMinute := -1
	currentMinute := -1
	counter := NewSleepCounter()

	for _, line := range lines {
		previousMinute = currentMinute
		currentMinute = getMinute(line)

		if is, _ := isFallsAsleepLine(line); is {
			isAsleep = true
		}

		if is, _ := isGuardLine(line); is {
			if isAsleep {
				counter.Sleep(currentGuard, previousMinute, 60)
			}
			currentGuard = getGuardNumber(line)
			isAsleep = false
		}

		if is, _ := isWakesUpLine(line); is {
			from := previousMinute
			if previousMinute > currentMinute {
				from = 0
			}
			counter.Sleep(currentGuard, from, currentMinute)
			isAsleep = false
		}
	}

	mostSleepyId := counter.FindMostSleepy()
	mostSleepyMinute := counter.FindMostSleepyMinute(mostSleepyId)
	println(mostSleepyId * mostSleepyMinute)
}

type SleepCounter interface {
	Sleep(id int, from int, to int)
	FindMostSleepy() int
	FindMostSleepyMinute(id int) int
}

func NewSleepCounter() SleepCounter {
	counter := basicSleepCounter{data: make(map[int][]int)}
	return &counter
}

type basicSleepCounter struct {
	data map[int][]int
}

func (o *basicSleepCounter) Sleep(id int, from int, to int) {
	slice := o.get(id)
	for i := from; i < to; i++ {
		slice[i]++
	}
}

func (o *basicSleepCounter) FindMostSleepy() int {
	i := -1
	vMax := -1
	for k, slice := range o.data {
		v := o.sum(slice)
		if v > vMax {
			vMax = v
			i = k
		}
	}
	return i
}

func (o *basicSleepCounter) FindMostSleepyMinute(id int) int {
	slice := o.get(id)
	return o.idxMax(slice)
}

func (o *basicSleepCounter) get(id int) []int {
	if _, ok := o.data[id]; !ok {
		o.data[id] = make([]int, 60)
	}
	return o.data[id]
}

func (o *basicSleepCounter) sum(ints []int) int {
	total := 0
	for _, v := range ints {
		total += v
	}
	return total
}

func (o *basicSleepCounter) idxMax(ints []int) int {
	i := -1
	vMax := -1
	for idx, v := range ints {
		if v > vMax {
			vMax = v
			i = idx
		}
	}
	return i
}

func isGuardLine(line string) (bool, error) {
	return regexp.MatchString(`Guard #\d+ begins shift`, line)
}

func isFallsAsleepLine(line string) (bool, error) {
	return regexp.MatchString(`falls asleep`, line)
}

func isWakesUpLine(line string) (bool, error) {
	return regexp.MatchString(`wakes up`, line)
}

func getMinute(line string) int {
	re := regexp.MustCompile(`\d\d:(\d\d)`)
	text := re.FindStringSubmatch(line)[1]
	i, _ := strconv.Atoi(text)
	return i
}

func getGuardNumber(line string) int {
	re := regexp.MustCompile(`#(\d+)`)
	text := re.FindStringSubmatch(line)[1]
	i, _ := strconv.Atoi(text)
	return i
}
