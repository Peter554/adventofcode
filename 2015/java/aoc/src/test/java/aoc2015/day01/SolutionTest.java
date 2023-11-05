package aoc.day01;

import aoc.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

public class SolutionTest {
    @Test
    public void solvesPart1() {

        Assert.assertEquals(0, Solution.part1("(())"));
        Assert.assertEquals(3, Solution.part1("((("));
        Assert.assertEquals(3, Solution.part1("(()(()("));

        var input = InputUtils.readInputAsString(this);
        Assert.assertEquals(74, Solution.part1(input));
    }

    @Test
    public void solvesPart2() {
        Assert.assertEquals(1, Solution.part2(")"));
        Assert.assertEquals(5, Solution.part2("()())"));

        var input = InputUtils.readInputAsString(this);
        Assert.assertEquals(1795, Solution.part2(input));
    }
}
