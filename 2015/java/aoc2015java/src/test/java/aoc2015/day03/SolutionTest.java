package aoc2015.day03;

import aoc2015.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

public class SolutionTest {
    @Test
    public void solvesPart1() {
        Assert.assertEquals(2, Solution.part1(">"));
        Assert.assertEquals(4, Solution.part1("^>v<"));
        Assert.assertEquals(2, Solution.part1("^v^v^v^v^v"));

        Assert.assertEquals(2572, Solution.part1(InputUtils.readInputAsString(this)));
    }

    @Test
    public void solvesPart2() {
        Assert.assertEquals(3, Solution.part2("^v"));
        Assert.assertEquals(3, Solution.part2("^>v<"));
        Assert.assertEquals(11, Solution.part2("^v^v^v^v^v"));

        Assert.assertEquals(2631, Solution.part2(InputUtils.readInputAsString(this)));
    }
}
