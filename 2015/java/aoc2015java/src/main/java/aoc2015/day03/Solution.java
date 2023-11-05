package aoc2015.day03;

import java.util.HashSet;
import java.util.Map;

public class Solution {
    private static final Map<Character, Direction> DIRECTION_MAP = Map.of(
            '<', Direction.LEFT,
            '>', Direction.RIGHT,
            '^', Direction.UP,
            'v', Direction.DOWN
    );

    public static int part1(String input) {
        var santa = new Agent();
        var visitedPositions = new HashSet<Point>();
        visitedPositions.add(santa.position);
        for (var instruction : input.toCharArray()) {
            var direction = DIRECTION_MAP.get(instruction);
            santa.move(direction);
            visitedPositions.add(santa.position);
        }
        return visitedPositions.size();
    }

    public static int part2(String input) {
        var santa = new Agent();
        var robot = new Agent();

        var visitedPositions = new HashSet<Point>();
        visitedPositions.add(santa.position);
        visitedPositions.add(robot.position);

        for (var i = 0; i < input.length(); i++) {
            var agent = i % 2 == 0 ? santa : robot;
            var instruction = input.charAt(i);
            var direction = DIRECTION_MAP.get(instruction);
            agent.move(direction);
            visitedPositions.add(agent.position);
        }
        return visitedPositions.size();
    }
}

record Point(int x, int y) {
}

enum Direction {LEFT, RIGHT, UP, DOWN}

class Agent {
    public Point position = new Point(0, 0);

    public void move(Direction direction) {
        switch (direction) {
            case LEFT:
                position = new Point(position.x() - 1, position.y());
                break;
            case RIGHT:
                position = new Point(position.x() + 1, position.y());
                break;
            case UP:
                position = new Point(position.x(), position.y() + 1);
                break;
            case DOWN:
                position = new Point(position.x(), position.y() - 1);
                break;
        }
    }
}