package aoc2015.day05;

import java.util.*;

public class Solution {
    private static final Collection<Character> VOWELS = Set.of('a', 'e', 'i', 'o', 'u');
    private static final Collection<String> FORBIDDEN_SUBSTRINGS = Set.of("ab", "cd", "pq", "xy");

    public static int part1(List<String> input) {
        var nice = 0;
        for (var s : input) {
            var containedVowels = new ArrayList<Character>();
            var containsRepeatedLetter = false;
            var containsForbiddenSubstring = false;

            for (var idx = 0; idx < s.length(); idx++) {
                var currentLetter = s.charAt(idx);
                var previousLetter = idx > 0 ? s.charAt(idx - 1) : null;

                if (VOWELS.contains(currentLetter)) {
                    containedVowels.add(currentLetter);
                }
                if (previousLetter != null && currentLetter == previousLetter) {
                    containsRepeatedLetter = true;
                }
                if (previousLetter != null && FORBIDDEN_SUBSTRINGS.contains(new String(new char[]{previousLetter, currentLetter}))) {
                    containsForbiddenSubstring = true;
                }
            }
            if (containedVowels.size() >= 3 && containsRepeatedLetter && !containsForbiddenSubstring) {
                nice++;
            }
        }
        return nice;
    }

    public static int part2(List<String> input) {
        var nice = 0;
        for (var s : input) {
            var seenPairPositions = new HashMap<String, Integer>();
            var containsRepeatedPair = false;
            var containsSplitPair = false;

            for (var idx = 0; idx < s.length(); idx++) {
                var currentLetter = s.charAt(idx);
                var previousLetter = idx > 0 ? s.charAt(idx - 1) : null;
                var previousPreviousLetter = idx > 1 ? s.charAt(idx - 2) : null;

                if (previousLetter != null) {
                    var pair = new String(new char[]{previousLetter, currentLetter});
                    if (seenPairPositions.containsKey(pair)) {
                        if (idx >= seenPairPositions.get(pair) + 2) {
                            containsRepeatedPair = true;
                        }
                    } else {
                        seenPairPositions.put(pair, idx);
                    }
                }

                if (previousPreviousLetter != null && currentLetter == previousPreviousLetter) {
                    containsSplitPair = true;
                }
            }
            if (containsRepeatedPair && containsSplitPair) {
                nice++;
            }
        }
        return nice;
    }
}
