package aoc.day02;


import aoc.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

import java.util.List;

public class SolutionTest {
    @Test
    public void solvesPart1() {

        Assert.assertEquals(58, Solution.part1(List.of("2x3x4")));
        Assert.assertEquals(58, Solution.part1(List.of("3x4x2")));

        Assert.assertEquals(43, Solution.part1(List.of("1x1x10")));

        var input = InputUtils.readInputAsStrings(this);
        Assert.assertEquals(1598415, Solution.part1(input));
    }

    @Test
    public void solvesPart2() {

        Assert.assertEquals(34, Solution.part2(List.of("2x3x4")));
        Assert.assertEquals(34, Solution.part2(List.of("3x4x2")));

        Assert.assertEquals(14, Solution.part2(List.of("1x1x10")));

        var input = InputUtils.readInputAsStrings(this);
        Assert.assertEquals(3812909, Solution.part2(input));
    }


}
