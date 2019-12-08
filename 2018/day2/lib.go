package main

import "errors"

func letterAppearsExactlyNTimes(s string, n int) bool {
	m := make(map[rune]int)

	for _, b := range s {
		m[b]++
	}

	for _, value := range m {
		if value == n {
			return true
		}
	}

	return false
}

func lettersInCommon(s1 string, s2 string) (common string, removed int, err error) {
	if len(s1) != len(s2) {
		return common, removed, errors.New("Strings must have the same length")
	}

	for i, r := range s1 {
		switch {
		case r == rune(s2[i]):
			common += string(r)

		default:
			removed++
		}

	}

	return common, removed, nil
}
