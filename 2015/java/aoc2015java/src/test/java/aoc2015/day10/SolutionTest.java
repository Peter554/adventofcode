package aoc2015.day10;

import org.junit.Assert;
import org.junit.Test;

public class SolutionTest {
    @Test
    public void testLookAndSay() {
        Assert.assertEquals("312211", Solution.lookAndSay("1", 5));

        // part 1
        Assert.assertEquals(360154, Solution.lookAndSay("1113122113", 40).length());

        // part 2
        Assert.assertEquals(5103798, Solution.lookAndSay("1113122113", 50).length());

    }
}
