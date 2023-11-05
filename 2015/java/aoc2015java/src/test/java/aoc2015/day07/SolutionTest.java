package aoc2015.day07;

import aoc2015.testutils.InputUtils;
import org.junit.Assert;
import org.junit.Test;

import java.util.Map;

public class SolutionTest {
    @Test
    public void testSolve() {
        var solution = Solution.solve(InputUtils.readInputAsStrings(this, "sample"));
        Map<String, Integer> expectedSolution = Map.of(
                "d", 72,
                "e", 507,
                "f", 492,
                "g", 114,
                "h", 65412,
                "i", 65079,
                "x", 123,
                "y", 456
        );

        Assert.assertEquals(expectedSolution.size(), solution.size());
        expectedSolution.forEach((k, v) -> {
            Assert.assertEquals(v, solution.get(k));
        });
    }

    @Test
    public void testPart1() {
        var solution = Solution.solve(InputUtils.readInputAsStrings(this));
        Assert.assertEquals(956, solution.get("a").intValue());
    }

    @Test
    public void testPart2() {
        var solution = Solution.solve(InputUtils.readInputAsStrings(this), Map.of(
                "b", 956
        ));
        Assert.assertEquals(40149, solution.get("a").intValue());
    }
}
