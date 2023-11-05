package aoc.day04;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Solution {
    public static int part1(String prefix) {
        for (var i = 1; true; i++) {
            var s = String.format("%s%d", prefix, i);
            var hash = hashMd5(s.getBytes(StandardCharsets.UTF_8));
            if (bytesToHex(hash).startsWith("00000")) {
                return i;
            }
        }
    }

    public static int part2(String prefix) {
        for (var i = 1; true; i++) {
            var s = String.format("%s%d", prefix, i);
            var hash = hashMd5(s.getBytes(StandardCharsets.UTF_8));
            if (bytesToHex(hash).startsWith("000000")) {
                return i;
            }
        }
    }

    private static byte[] hashMd5(byte[] b) {
        try {
            return MessageDigest.getInstance("MD5").digest(b);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    private static String bytesToHex(byte[] b) {
        var sb = new StringBuilder();
        for (var bi : b) {
            sb.append(String.format("%02x", bi));
        }
        return sb.toString();
    }
}
