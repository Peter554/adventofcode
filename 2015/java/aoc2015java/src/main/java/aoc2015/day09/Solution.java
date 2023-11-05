package aoc2015.day09;

import java.util.*;
import java.util.regex.Pattern;

public class Solution {
    public static int[] solve(List<String> input) {
        var nodes = new HashMap<String, Node>();
        var edges = new HashMap<Tuple<Node, Node>, Edge>();

        for (var rawEdgeSpec : input) {
            var matcher = Pattern.compile("^(\\w+) to (\\w+) = (\\d+)$").matcher(rawEdgeSpec);
            matcher.find();

            var nodeA = nodes.getOrDefault(matcher.group(1), new Node(matcher.group(1)));
            var nodeB = nodes.getOrDefault(matcher.group(2), new Node(matcher.group(2)));
            nodes.put(nodeA.name(), nodeA);
            nodes.put(nodeB.name(), nodeB);

            var edgeCost = Integer.parseInt(matcher.group(3));
            var edgeA = new Edge(nodeA, nodeB, edgeCost);
            var edgeB = new Edge(nodeB, nodeA, edgeCost);
            edges.put(new Tuple<>(edgeA.from(), edgeA.to()), edgeA);
            edges.put(new Tuple<>(edgeB.from(), edgeB.to()), edgeB);
        }

        var tours = buildTours(nodes, edges);

        Tour shortestTour = tours.get(0);
        Tour longestTour = tours.get(0);
        for (var tour : tours) {
            if (tour.cost() < shortestTour.cost()) {
                shortestTour = tour;
            }
            if (tour.cost() > longestTour.cost()) {
                longestTour = tour;
            }
        }
        return new int[]{shortestTour.cost(), longestTour.cost()};
    }

    private static List<Tour> buildTours(Map<String, Node> nodes, Map<Tuple<Node, Node>, Edge> edges) {
        var tours = new ArrayList<Tour>();
        for (var startingNodeName : nodes.keySet()) {
            tours.addAll(buildToursStartingFrom(startingNodeName, nodes, edges));
        }
        return tours;
    }

    private static List<Tour> buildToursStartingFrom(String startingNodeName, Map<String, Node> nodes, Map<Tuple<Node, Node>, Edge> edges) {
        if (nodes.size() == 1) {
            var tours = new ArrayList<Tour>();
            tours.add(new Tour(0, new Path(nodes.get(startingNodeName), null)));
            return tours;
        }

        var tours = new ArrayList<Tour>();
        var startNode = nodes.get(startingNodeName);
        var targetNodeNames = new HashSet<>(nodes.keySet());
        targetNodeNames.remove(startingNodeName);
        for (var targetNodeName : targetNodeNames) {
            var targetNode = nodes.get(targetNodeName);
            var edge = edges.get(new Tuple<>(startNode, targetNode));
            var remainingNodes = new HashMap<>(nodes);
            remainingNodes.remove(startingNodeName);
            for (var nextTour : buildToursStartingFrom(targetNodeName, remainingNodes, edges)) {
                tours.add(new Tour(edge.cost() + nextTour.cost(), new Path(startNode, nextTour.path())));
            }
        }
        return tours;
    }
}

record Node(String name) {
}

record Tuple<T1, T2>(T1 a, T2 b) {
}

record Edge(Node from, Node to, int cost) {
}

record Tour(int cost, Path path) {
}

record Path(Node node, Path next) {
}

