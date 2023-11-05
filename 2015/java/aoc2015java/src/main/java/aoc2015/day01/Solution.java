package aoc2015.day01;

public class Solution {
    public static int part1(String input) {
        var floor = 0;
        for (var c : input.toCharArray()) {
            switch (c) {
                case '(':
                    floor++;
                    break;
                case ')':
                    floor--;
                    break;
            }
        }
        return floor;
    }

    public static int part2(String input) {
        var floor = 0;
        for (var position = 1; position <= input.length(); position++) {
            switch (input.charAt(position - 1)) {
                case '(':
                    floor++;
                    break;
                case ')':
                    floor--;
                    break;
            }
            if (floor == -1) {
                return position;
            }
        }
        throw new RuntimeException();
    }
}
