package aoc2015.day04;

import org.junit.Assert;
import org.junit.Test;

public class SolutionTest {
    @Test
    public void solvesPart1() {
        Assert.assertEquals(254575, Solution.part1("bgvyzdsv"));
    }

    @Test
    public void solvesPart2() {
        Assert.assertEquals(1038736, Solution.part2("bgvyzdsv"));
    }
}
