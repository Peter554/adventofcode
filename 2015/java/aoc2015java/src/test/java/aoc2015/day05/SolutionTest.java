package aoc2015.day05;

import aoc2015.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

import java.util.List;

public class SolutionTest {
    @Test
    public void solvesPart1() {
        Assert.assertEquals(2, Solution.part1(List.of(
                "ugknbfddgicrmopn",
                "aaa",
                "jchzalrnumimnmhp",
                "haegwjzuvuyypxyu",
                "dvszwmarrgswjxmb"
        )));

        Assert.assertEquals(238, Solution.part1(InputUtils.readInputAsStrings(this)));;
    }

    @Test
    public void solvesPart2() {
        Assert.assertEquals(2, Solution.part2(List.of(
                "qjhvhtzxzqqjkmpb",
                "xxyxx",
                "uurcxstgmygtbstg",
                "ieodomkazucvgmuy"
        )));

        Assert.assertEquals(69, Solution.part2(InputUtils.readInputAsStrings(this)));;
    }
}
