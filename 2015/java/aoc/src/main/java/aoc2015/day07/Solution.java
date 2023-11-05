package aoc.day07;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Solution {
    public static Map<String, Integer> solve(List<String> input) {
        return solve(input, Map.of());
    }

    public static Map<String, Integer> solve(List<String> input, Map<String, Integer> signalOverrides) {
        var wires = new HashMap<String, Wire>();

        for (var rawInstruction : input) {
            var rawInstructionLeft = rawInstruction.split(" -> ")[0];
            var rawInstructionRight = rawInstruction.split(" -> ")[1];

            Gate gate;
            if (rawInstructionLeft.contains("AND")) {
                var leftWire = getSetWire(rawInstructionLeft.split(" AND ")[0], wires);
                var rightWire = getSetWire(rawInstructionLeft.split(" AND ")[1], wires);
                gate = new Gate(leftWire, rightWire, (l, r) -> l.getSignal() & r.getSignal());
            } else if (rawInstructionLeft.contains("OR")) {
                var leftWire = getSetWire(rawInstructionLeft.split(" OR ")[0], wires);
                var rightWire = getSetWire(rawInstructionLeft.split(" OR ")[1], wires);
                gate = new Gate(leftWire, rightWire, (l, r) -> l.getSignal() | r.getSignal());
            } else if (rawInstructionLeft.contains("NOT")) {
                var wire = getSetWire(rawInstructionLeft.substring(4), wires);
                gate = new Gate(wire, null, (l, r) -> Solution.correctBits(~l.getSignal()));
            } else if (rawInstructionLeft.contains("LSHIFT")) {
                var wire = getSetWire(rawInstructionLeft.split(" LSHIFT ")[0], wires);
                var shift = Integer.parseInt(rawInstructionLeft.split(" LSHIFT ")[1]);
                gate = new Gate(wire, null, (l, r) -> l.getSignal() << shift);
            } else if (rawInstructionLeft.contains("RSHIFT")) {
                var wire = getSetWire(rawInstructionLeft.split(" RSHIFT ")[0], wires);
                var shift = Integer.parseInt(rawInstructionLeft.split(" RSHIFT ")[1]);
                gate = new Gate(wire, null, (l, r) -> l.getSignal() >> shift);
            } else {
                var wire = getSetWire(rawInstructionLeft, wires);
                gate = new Gate(wire, null, (l, r) -> l.getSignal());
            }
            
            var targetWire = getSetWire(rawInstructionRight, wires);
            targetWire.setGate(gate);
        }

        signalOverrides.forEach((k, v) -> {
            wires.get(k).setSignal(v);
        });

        return wires.entrySet().stream().collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue().getSignal()));
    }

    private static Wire getSetWire(String name, Map<String, Wire> wires) {
        if (Pattern.compile("^\\d+$").matcher(name).find()) {
            // "Anonymous wire".
            return new Wire(null, Integer.parseInt(name));
        }
        var wire = wires.getOrDefault(name, new Wire(name));
        wires.put(name, wire);
        return wire;
    }

    private static Integer correctBits(Integer i) {
        i = i & Integer.MAX_VALUE; // make sure negative bit is not set.
        i = i & ((1 << 16) - 1);  // ensure no extra bits are set.
        return i;
    }
}

class Wire {
    private final String name;
    private Integer signal;
    private Gate gate;


    public Wire(String name) {
        this.name = name;
    }

    public Wire(String name, int signal) {
        this.name = name;
        this.signal = signal;
    }


    public int getSignal() {
        if (signal == null) {
            signal = this.gate.getSignal();
        }
        return signal;
    }

    public void setSignal(int signal) {
        this.signal = signal;
    }

    public void setGate(Gate gate) {
        this.gate = gate;
    }
}


class Gate {
    private final Wire leftWire;
    private final Wire rightWire;
    private final BiFunction<Wire, Wire, Integer> logicFunction;

    public Gate(Wire leftWire, Wire rightWire, BiFunction<Wire, Wire, Integer> logicFunction) {
        this.leftWire = leftWire;
        this.rightWire = rightWire;
        this.logicFunction = logicFunction;
    }

    public int getSignal() {
        return logicFunction.apply(leftWire, rightWire);
    }
}