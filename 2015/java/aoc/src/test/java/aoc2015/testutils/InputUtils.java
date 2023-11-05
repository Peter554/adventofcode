package aoc.testutils;

import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class InputUtils {
    public static String readInputAsString(Object testClass, String filename) {
        Path inputPath;
        try {
            inputPath = Paths.get(testClass.getClass().getResource(filename).toURI());
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }

        try {
            return Files.readString(inputPath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static String readInputAsString(Object testClass) {
        return readInputAsString(testClass, "input");
    }

    public static List<String> readInputAsStrings(Object testClass, String filename) {
        Path inputPath;
        try {
            inputPath = Paths.get(testClass.getClass().getResource(filename).toURI());
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }

        try {
            return Files.readAllLines(inputPath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static List<String> readInputAsStrings(Object testClass) {
        return readInputAsStrings(testClass, "input");
    }
}
