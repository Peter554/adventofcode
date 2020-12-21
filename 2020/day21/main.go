package main

import (
	"fmt"
	"sort"
	"strings"

	"github.com/peter554/adventofcode/2020/lib"
)

func main() {
	lines := lib.ReadInput()
	lib.Result{Part: 1, Value: Part1(lines)}.Print()
	fmt.Println("Part 2 =", Part2(lines))
}

func Part1(lines []string) int {
	ingredient2Allergen := parseFoods(lines)

	count := 0
	for _, line := range lines {
		ingredients, _ := parseFood(line)
		for ingredient, allergen := range ingredient2Allergen {
			if allergen == nil && ingredients.Contains(ingredient) {
				count++
			}
		}
	}
	return count
}

func Part2(lines []string) string {
	ingredient2Allergen := parseFoods(lines)

	allergens := []string{}
	allergen2Ingredient := map[string]string{}
	for ingredient, allergen := range ingredient2Allergen {
		if allergen != nil {
			allergens = append(allergens, *allergen)
			allergen2Ingredient[*allergen] = ingredient
		}
	}

	sort.Strings(allergens)

	o := []string{}
	for _, allergen := range allergens {
		o = append(o, allergen2Ingredient[allergen])
	}
	return strings.Join(o, ",")
}

func parseFood(line string) (ingredients, allergens *StringSet) {
	ingredients, allergens = NewStringSet(), NewStringSet()
	parts := strings.Split(line, "(")
	for _, s := range strings.Split(parts[0][:len(parts[0])-1], " ") {
		ingredients.Add(strings.TrimSpace(s))
	}
	for _, s := range strings.Split(parts[1][8:len(parts[1])-1], ",") {
		allergens.Add(strings.TrimSpace(s))
	}
	return
}

func parseFoods(lines []string) (ingredient2Allergen map[string]*string) {
	allIngredients, allAllergens := NewStringSet(), NewStringSet()
	for _, line := range lines {
		ingredients, allergens := parseFood(line)
		allIngredients = allIngredients.Union(ingredients)
		allAllergens = allAllergens.Union(allergens)
	}

	allergen2Ingredients := map[string]*StringSet{}
	for _, allergen := range allAllergens.ToSlice() {
		allergen2Ingredients[allergen] = allIngredients.Copy()
	}
	for _, line := range lines {
		ingredients, allergens := parseFood(line)
		for _, allergen := range allergens.ToSlice() {
			allergen2Ingredients[allergen] = allergen2Ingredients[allergen].Intersection(ingredients)
		}
	}

	ingredient2Allergen = map[string]*string{}
	for _, ingredient := range allIngredients.ToSlice() {
		ingredient2Allergen[ingredient] = nil
	}
	for len(allergen2Ingredients) > 0 {
		for allergen, ingredients := range allergen2Ingredients {
			if ingredients.Size() == 1 {
				ingredient := ingredients.ToSlice()[0]
				delete(allergen2Ingredients, allergen)
				ingredient2Allergen[ingredient] = &allergen // copy?
				for _, ingredients := range allergen2Ingredients {
					ingredients.Remove(ingredient)
				}
				break
			}
		}
	}

	return
}

type StringSet struct {
	m map[string]bool
}

func NewStringSet() *StringSet {
	return &StringSet{m: map[string]bool{}}
}

func (ss *StringSet) Add(s string) {
	ss.m[s] = true
}

func (ss *StringSet) Remove(s string) {
	delete(ss.m, s)
}

func (ss *StringSet) Contains(s string) bool {
	_, exists := ss.m[s]
	return exists
}

func (ss *StringSet) Size() int {
	return len(ss.m)
}

func (ss *StringSet) ToSlice() []string {
	o := []string{}
	for s := range ss.m {
		o = append(o, s)
	}
	return o
}

func (ss *StringSet) Copy() *StringSet {
	m := map[string]bool{}
	for s := range ss.m {
		m[s] = true
	}
	return &StringSet{m: m}
}

func (ss *StringSet) Union(other *StringSet) *StringSet {
	new := NewStringSet()
	for s := range ss.m {
		new.m[s] = true
	}
	for s := range other.m {
		new.m[s] = true
	}
	return new
}

func (ss *StringSet) Intersection(other *StringSet) *StringSet {
	new := NewStringSet()
	for s := range ss.m {
		if other.Contains(s) {
			new.m[s] = true
		}
	}
	return new
}

func (ss *StringSet) String() string {
	o := []string{}
	for s := range ss.m {
		o = append(o, s)
	}
	return "{" + strings.Join(o, ", ") + "}"
}
