package aoc.day08;

import aoc.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

public class SolutionTest {
    @Test
    public void solvesPart1() {
        Assert.assertEquals(12, Solution.part1(InputUtils.readInputAsStrings(this, "sample")));
        Assert.assertEquals(1333, Solution.part1(InputUtils.readInputAsStrings(this)));
    }

    @Test
    public void solvesPart2() {
        Assert.assertEquals(19, Solution.part2(InputUtils.readInputAsStrings(this, "sample")));
        Assert.assertEquals(2046, Solution.part2(InputUtils.readInputAsStrings(this)));
    }
}
