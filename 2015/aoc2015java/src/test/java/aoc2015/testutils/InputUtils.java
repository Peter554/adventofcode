package aoc2015.testutils;

import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class InputUtils {
    public static String readInputAsString(Object testClass) {
        Path inputPath;
        try {
            inputPath = Paths.get(testClass.getClass().getResource("input").toURI());
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }

        try {
            return Files.readString(inputPath);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
