package aoc.day09;

import aoc.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

public class SolutionTest {
    @Test
    public void solvesPart1() {
        Assert.assertEquals(605, Solution.solve(InputUtils.readInputAsStrings(this, "sample"))[0]);
        Assert.assertEquals(207, Solution.solve(InputUtils.readInputAsStrings(this))[0]);
    }

    @Test
    public void solvesPart2() {
        Assert.assertEquals(982, Solution.solve(InputUtils.readInputAsStrings(this, "sample"))[1]);
        Assert.assertEquals(804, Solution.solve(InputUtils.readInputAsStrings(this))[1]);
    }
}
