package aoc2015.day06;

import aoc2015.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

public class SolutionTest {
    @Test
    public void solvesPart1() {
        Assert.assertEquals(377891, Solution.part1(InputUtils.readInputAsStrings(this)));
    }

    @Test
    public void solvesPart2() {
        Assert.assertEquals(14110788, Solution.part2(InputUtils.readInputAsStrings(this)));
    }
}
