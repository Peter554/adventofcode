package aoc.day06;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.regex.Pattern;

public class Solution {
    public static int part1(List<String> input) {
        Map<NamedAction, Function<Integer, Integer>> actionMapping = Map.of(
                NamedAction.TURN_ON, i -> 1,
                NamedAction.TURN_OFF, i -> 0,
                NamedAction.TOGGLE, i -> (i + 1) % 2
        );

        var grid = new Grid(1000);
        for (var rawInstruction : input) {
            var instruction = Instruction.parse(rawInstruction, actionMapping);
            grid.apply(instruction);
        }
        return grid.count();
    }

    public static int part2(List<String> input) {
        Map<NamedAction, Function<Integer, Integer>> actionMapping = Map.of(
                NamedAction.TURN_ON, i -> i + 1,
                NamedAction.TURN_OFF, i -> i > 0 ? i - 1 : 0,
                NamedAction.TOGGLE, i -> i + 2
        );

        var grid = new Grid(1000);
        for (var rawInstruction : input) {
            var instruction = Instruction.parse(rawInstruction, actionMapping);
            grid.apply(instruction);
        }
        return grid.count();
    }
}

record Point(int x, int y) {
}

record Box(int xMin, int xMax, int yMin, int yMax) {
}

enum NamedAction {TURN_ON, TURN_OFF, TOGGLE}


record Instruction(Box box, Function<Integer, Integer> action) {

    public static Instruction parse(String rawInstruction, Map<NamedAction, Function<Integer, Integer>> actionMapping) {
        var matcher = Pattern.compile("(\\d+),(\\d+)").matcher(rawInstruction);
        matcher.find();
        var xMin = Integer.parseInt(matcher.group(1));
        var yMin = Integer.parseInt(matcher.group(2));
        matcher.find();
        var xMax = Integer.parseInt(matcher.group(1));
        var yMax = Integer.parseInt(matcher.group(2));
        var box = new Box(xMin, xMax, yMin, yMax);

        var namedAction = rawInstruction.startsWith("turn on") ?
                NamedAction.TURN_ON : rawInstruction.startsWith("turn off") ?
                NamedAction.TURN_OFF : rawInstruction.startsWith("toggle") ?
                NamedAction.TOGGLE : null;  // throw error for unknown action?
        var action = actionMapping.get(namedAction);

        return new Instruction(box, action);
    }
}


class Grid {
    private final Map<Point, Integer> grid;

    public Grid(int size) {
        grid = new HashMap<>();
        for (var x = 0; x < size; x++) {
            for (var y = 0; y < size; y++) {
                grid.put(new Point(x, y), 0);
            }
        }
    }

    public void apply(Instruction instruction) {
        for (var x = instruction.box().xMin(); x <= instruction.box().xMax(); x++) {
            for (var y = instruction.box().yMin(); y <= instruction.box().yMax(); y++) {
                var point = new Point(x, y);
                var initialState = grid.get(point);
                grid.put(point, instruction.action().apply(initialState));
            }
        }
    }

    public int count() {
        return grid.values().stream().mapToInt(Integer::intValue).sum();
    }
}

