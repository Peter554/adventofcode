package main

import (
	"bufio"
	"fmt"
	"os"
)

func readlines(path string) []string {
	file, _ := os.Open(path)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	out := make([]string, 0)
	for scanner.Scan() {
		line := scanner.Text()
		out = append(out, line)
	}
	return out
}

func main() {
	input := readlines("./input.txt")
	xmax, ymax, track, carts := parseinput(input)
	// print(xmax, ymax, track, carts)

	// crash := findcrash(xmax, ymax, track, carts)
	// fmt.Println(crash)

	_, p := findlastcart(xmax, ymax, track, carts)
	fmt.Println(p)
}

type point struct {
	x int
	y int
}

type historypoint struct {
	p point
	v string
}

type cart struct {
	v string
	i int
	h []historypoint
}

func parseinput(input []string) (int, int, map[point]string, map[point]*cart) {
	track := make(map[point]string)
	carts := make(map[point]*cart)

	xmax, ymax := 0, 0

	for y, line := range input {
		ymax = y
		for x, char := range line {
			xmax = x
			char := string(char)
			if char == " " {
				continue
			} else if char == "^" {
				track[point{x, y}] = "|"
				carts[point{x, y}] = &cart{"up", 0, make([]historypoint, 0)}
			} else if char == "v" {
				track[point{x, y}] = "|"
				carts[point{x, y}] = &cart{"down", 0, make([]historypoint, 0)}
			} else if char == "<" {
				track[point{x, y}] = "-"
				carts[point{x, y}] = &cart{"left", 0, make([]historypoint, 0)}
			} else if char == ">" {
				track[point{x, y}] = "-"
				carts[point{x, y}] = &cart{"right", 0, make([]historypoint, 0)}
			} else {
				track[point{x, y}] = char
			}
		}
	}
	return xmax, ymax, track, carts
}

func findcrash(xmax int, ymax int, track map[point]string, carts map[point]*cart) point {
	for {
		// print(xmax, ymax, track, carts)
		skip := make(map[point]bool)
		for y := 0; y <= ymax; y++ {
			for x := 0; x <= xmax; x++ {
				p := point{x, y}
				if _, ok := skip[p]; ok {
					continue
				}
				if cart, ok := carts[p]; ok {
					delete(carts, p)
					dx, dy := dxdy(cart)
					np := point{p.x + dx, p.y + dy}
					if _, ok := carts[np]; ok {
						return np
					}
					carts[np] = cart
					skip[np] = true
					updatecartvelocity(np, cart, track)
					cart.h = append(cart.h, historypoint{np, cart.v})
					if _, ok := track[np]; !ok {
						printhistory(cart.h, track)
						panic(fmt.Sprintf("New point (%d, %d) off track", np.x, np.y))
					}
				}
			}
		}
	}
}

func findlastcart(xmax int, ymax int, track map[point]string, carts map[point]*cart) (*cart, point) {
	for {
		// print(xmax, ymax, track, carts)
		skip := make(map[point]bool)
		for y := 0; y <= ymax; y++ {
			for x := 0; x <= xmax; x++ {
				p := point{x, y}
				if _, ok := skip[p]; ok {
					continue
				}
				if cart, ok := carts[p]; ok {
					delete(carts, p)
					dx, dy := dxdy(cart)
					np := point{p.x + dx, p.y + dy}
					skip[np] = true
					if _, ok := carts[np]; ok {
						delete(carts, np)
						continue
					}
					carts[np] = cart
					updatecartvelocity(np, cart, track)
					cart.h = append(cart.h, historypoint{np, cart.v})
					if _, ok := track[np]; !ok {
						printhistory(cart.h, track)
						panic(fmt.Sprintf("New point (%d, %d) off track", np.x, np.y))
					}
				}
			}
			if len(carts) == 1 {
				for k, v := range carts {
					return v, k
				}
			}
		}
	}
}

func dxdy(cart *cart) (int, int) {
	dx, dy := 0, 0
	if cart.v == "up" {
		dy = -1
	} else if cart.v == "down" {
		dy = 1
	} else if cart.v == "left" {
		dx = -1
	} else if cart.v == "right" {
		dx = 1
	}
	return dx, dy
}

func updatecartvelocity(np point, cart *cart, track map[point]string) {
	if track[np] == "/" {
		if cart.v == "up" {
			cart.v = "right"
		} else if cart.v == "down" {
			cart.v = "left"
		} else if cart.v == "left" {
			cart.v = "down"
		} else if cart.v == "right" {
			cart.v = "up"
		}
	}
	if track[np] == "\\" {
		if cart.v == "up" {
			cart.v = "left"
		} else if cart.v == "down" {
			cart.v = "right"
		} else if cart.v == "left" {
			cart.v = "up"
		} else if cart.v == "right" {
			cart.v = "down"
		}
	}
	if track[np] == "+" {
		if cart.i%3 == 0 {
			// turn left
			cart.v = map[string]string{
				"up":    "left",
				"down":  "right",
				"left":  "down",
				"right": "up",
			}[cart.v]
		} else if cart.i%3 == 1 {
			// go straight
		} else if cart.i%3 == 2 {
			// turn right
			cart.v = map[string]string{
				"up":    "right",
				"down":  "left",
				"left":  "up",
				"right": "down",
			}[cart.v]
		}
		cart.i++
	}
}

func print(xmax int, ymax int, track map[point]string, carts map[point]*cart) {
	for y := 0; y <= ymax; y++ {
		s := fmt.Sprintf("%d\t", y)
		for x := 0; x <= xmax; x++ {
			p := point{x, y}
			if cart, ok := carts[p]; ok {
				s += map[string]string{
					"up":    "^",
					"down":  "v",
					"left":  "<",
					"right": ">",
				}[cart.v]
			} else if value, ok := track[p]; ok {
				s += value
			} else {
				s += " "
			}
		}
		s += "\n"
		fmt.Print(s)
	}
	fmt.Print("\n\n")
}

func printhistory(history []historypoint, track map[point]string) {
	lastpoint := history[len(history)-1]
	xmin, xmax := lastpoint.p.x-8, lastpoint.p.x+8
	ymin, ymax := lastpoint.p.y-4, lastpoint.p.y+4

	for _, historypoint := range history {
		for y := ymin; y <= ymax; y++ {
			s := fmt.Sprintf("%d\t", y)
			for x := xmin; x <= xmax; x++ {
				p := point{x, y}
				if p == historypoint.p {
					s += map[string]string{
						"up":    "^",
						"down":  "v",
						"left":  "<",
						"right": ">",
					}[historypoint.v]
				} else if value, ok := track[p]; ok {
					s += value
				} else {
					s += " "
				}
			}
			s += "\n"
			fmt.Print(s)
		}
		fmt.Print("\n\n")
	}
}
