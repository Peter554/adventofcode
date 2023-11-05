package aoc.day10;


public class Solution {
    public static String lookAndSay(String s, int nTimes) {
        if (nTimes == 0) {
            return s;
        }

        var pointer = 0;
        var sb = new StringBuilder();
        while (pointer < s.length()) {
            var character = s.charAt(pointer);
            var characterCount = 1;
            while (pointer + 1 < s.length() && s.charAt(pointer + 1) == character) {
                characterCount++;
                pointer++;
            }
            pointer++;
            sb.append(String.format("%d%d", characterCount, Character.getNumericValue(character)));
        }
        return lookAndSay(sb.toString(), nTimes - 1);
    }
}
