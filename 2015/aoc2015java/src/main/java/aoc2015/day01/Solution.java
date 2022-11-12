package aoc2015.day01;

public class Solution {
    public static int part1(String s) {
        var floor = 0;
        for (var c : s.toCharArray()) {
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

    public static int part2(String s) {
        var floor = 0;
        for (var position = 1; position <= s.length(); position++) {
            switch (s.charAt(position - 1)) {
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
