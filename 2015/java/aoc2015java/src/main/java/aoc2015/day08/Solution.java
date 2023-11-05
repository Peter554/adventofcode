package aoc2015.day08;

import java.util.List;

public class Solution {
    public static int part1(List<String> input) {
        var count = 0;

        for (var s : input) {
            var characterCount = 0;
            var i = 1;  // skip the opening quote
            while (i < s.length() - 1) {  // skip the closing quote
                var character = s.charAt(i);
                if (character == '\\') {
                    var nextCharacter = i < s.length() - 2 ? s.charAt(i + 1) : null;
                    if (nextCharacter != null && nextCharacter == '\\') {
                        i += 2;
                    } else if (nextCharacter != null && nextCharacter == '\"') {
                        i += 2;
                    } else if (nextCharacter != null && nextCharacter == 'x') {
                        i += 4;
                    } else {
                        i++;
                    }
                } else {
                    i++;
                }
                characterCount++;
            }
            count += s.length() - characterCount;
        }

        return count;
    }

    public static int part2(List<String> input) {
        var count = 0;

        for (var s : input) {
            var encodingCount = 0;
            for (var character : s.toCharArray()) {
                if (character == '\\') {
                    encodingCount += 2;
                } else if (character == '\"') {
                    encodingCount += 2;
                } else {
                    encodingCount += 1;
                }
            }
            encodingCount += 2;  // add the opening and closing quotes
            count += encodingCount - s.length();
        }

        return count;
    }
}
