package aoc.day02;

import java.util.Arrays;
import java.util.List;


public class Solution {
    public static int part1(List<String> input) {
        var paper = 0;
        for (var presentSpec : input) {
            var dimensions = Arrays.stream(presentSpec.split("x"))
                    .mapToInt(Integer::parseInt)
                    .boxed()
                    .sorted()
                    .toList();
            paper += 3 * dimensions.get(0) * dimensions.get(1)
                    + 2 * dimensions.get(1) * dimensions.get(2)
                    + 2 * dimensions.get(2) * dimensions.get(0);
        }
        return paper;
    }

    public static int part2(List<String> input) {
        var ribbon = 0;
        for (var presentSpec : input) {
            var dimensions = Arrays.stream(presentSpec.split("x"))
                    .mapToInt(Integer::parseInt)
                    .boxed()
                    .sorted()
                    .toList();
            ribbon += 2 * (dimensions.get(0) + dimensions.get(1))
                    + dimensions.get(0) * dimensions.get(1) * dimensions.get(2);
        }
        return ribbon;
    }
}
