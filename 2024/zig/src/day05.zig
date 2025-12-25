const std = @import("std");

pub fn part1(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);

    var sections_iter = std.mem.tokenizeSequence(u8, file, "\n\n");

    const deps_section = sections_iter.next().?;
    var deps_graph = try DepsGraph.parse(allocator, deps_section);
    defer deps_graph.deinit();

    const page_updates_section = sections_iter.next().?;
    var page_updates_iter = std.mem.tokenizeScalar(u8, page_updates_section, '\n');

    var sum: u64 = 0;
    while (page_updates_iter.next()) |page_updates_str| {
        const page_updates = try parsePageUpdates(allocator, page_updates_str);
        defer allocator.free(page_updates);

        var deps_subgraph = try deps_graph.subgraph(allocator, page_updates);
        defer deps_subgraph.deinit();
        const topological_order = try deps_subgraph.topologicalOrder(allocator);
        defer allocator.free(topological_order);

        if (std.mem.eql(u64, page_updates, topological_order)) {
            sum += topological_order[topological_order.len / 2];
        }
    }

    return sum;
}

pub fn part2(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);

    var sections_iter = std.mem.tokenizeSequence(u8, file, "\n\n");

    const deps_section = sections_iter.next().?;
    var deps_graph = try DepsGraph.parse(allocator, deps_section);
    defer deps_graph.deinit();

    const page_updates_section = sections_iter.next().?;
    var page_updates_iter = std.mem.tokenizeScalar(u8, page_updates_section, '\n');

    var sum: u64 = 0;
    while (page_updates_iter.next()) |page_updates_str| {
        const page_updates = try parsePageUpdates(allocator, page_updates_str);
        defer allocator.free(page_updates);

        var deps_subgraph = try deps_graph.subgraph(allocator, page_updates);
        defer deps_subgraph.deinit();
        const topological_order = try deps_subgraph.topologicalOrder(allocator);
        defer allocator.free(topological_order);

        if (!std.mem.eql(u64, page_updates, topological_order)) {
            sum += topological_order[topological_order.len / 2];
        }
    }

    return sum;
}

const DepsGraph = struct {
    const Self = @This();

    data: std.AutoHashMap(u64, std.AutoHashMap(u64, void)),

    fn parse(allocator: std.mem.Allocator, s: []const u8) !Self {
        var deps = std.AutoHashMap(u64, std.AutoHashMap(u64, void)).init(allocator);
        errdefer {
            var values_iter = deps.valueIterator();
            while (values_iter.next()) |value| {
                value.deinit();
            }
            deps.deinit();
        }

        var deps_iter = std.mem.tokenizeScalar(u8, s, '\n');
        while (deps_iter.next()) |dep| {
            var iter = std.mem.tokenizeScalar(u8, dep, '|');
            const before_page = try std.fmt.parseInt(u64, iter.next().?, 10);
            const after_page = try std.fmt.parseInt(u64, iter.next().?, 10);
            const before_deps_entry = try deps.getOrPut(before_page);
            if (!before_deps_entry.found_existing) {
                before_deps_entry.value_ptr.* = std.AutoHashMap(u64, void).init(allocator);
            }
            try before_deps_entry.value_ptr.*.put(after_page, {});
            const after_deps_entry = try deps.getOrPut(after_page);
            if (!after_deps_entry.found_existing) {
                after_deps_entry.value_ptr.* = std.AutoHashMap(u64, void).init(allocator);
            }
        }

        return .{ .data = deps };
    }

    fn deinit(self: *Self) void {
        var values_iter = self.data.valueIterator();
        while (values_iter.next()) |value| {
            value.deinit();
        }
        self.data.deinit();
    }

    fn subgraph(self: Self, allocator: std.mem.Allocator, nodes: []u64) !Self {
        var deps = std.AutoHashMap(u64, std.AutoHashMap(u64, void)).init(allocator);
        errdefer {
            var values_iter = deps.valueIterator();
            while (values_iter.next()) |value| {
                value.deinit();
            }
            deps.deinit();
        }

        for (nodes) |node| {
            const entry = try deps.getOrPut(node);
            if (!entry.found_existing) {
                entry.value_ptr.* = std.AutoHashMap(u64, void).init(allocator);
            }

            for (nodes) |n| {
                if (self.data.getEntry(node).?.value_ptr.contains(n)) {
                    try entry.value_ptr.*.put(n, {});
                }
            }
        }

        return .{ .data = deps };
    }

    fn topologicalOrder(self: Self, allocator: std.mem.Allocator) ![]u64 {
        var q = try std.Deque(u64).initCapacity(allocator, 32);
        defer q.deinit(allocator);

        var in_degrees = std.AutoHashMap(u64, u64).init(allocator);
        defer in_degrees.deinit();

        var entry_iter = self.data.iterator();
        // Initialize all in-degrees as 0.
        while (entry_iter.next()) |entry| {
            _ = try in_degrees.getOrPutValue(entry.key_ptr.*, 0);
        }
        // Set the in-degrees based on the dependants graph.
        entry_iter = self.data.iterator();
        while (entry_iter.next()) |entry| {
            var dependants_iter = entry.value_ptr.*.keyIterator();
            while (dependants_iter.next()) |dependant| {
                in_degrees.getPtr(dependant.*).?.* += 1;
            }
        }
        // Push nodes with in-degree of 0 into the queue.
        entry_iter = self.data.iterator();
        while (entry_iter.next()) |entry| {
            if (in_degrees.get(entry.key_ptr.*) == 0) {
                try q.pushBack(allocator, entry.key_ptr.*);
            }
        }

        var result = try std.ArrayList(u64).initCapacity(allocator, 32);
        defer result.deinit(allocator);
        while (q.popFront()) |n| {
            try result.append(allocator, n);

            var dependants_iter = self.data.get(n).?.keyIterator();
            while (dependants_iter.next()) |dependant| {
                const in_degree = in_degrees.getPtr(dependant.*).?;
                in_degree.* -= 1;
                if (in_degree.* == 0) {
                    try q.pushBack(allocator, dependant.*);
                }
            }
        }

        return result.toOwnedSlice(allocator);
    }
};

fn parsePageUpdates(allocator: std.mem.Allocator, s: []const u8) ![]u64 {
    var page_updates = try std.ArrayList(u64).initCapacity(allocator, 64);
    defer page_updates.deinit(allocator);
    var iter = std.mem.tokenizeScalar(u8, s, ',');
    while (iter.next()) |n_str| {
        const n = try std.fmt.parseInt(u64, n_str, 10);
        try page_updates.append(allocator, n);
    }
    return page_updates.toOwnedSlice(allocator);
}

test "part 1" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(143, part1(allocator, "data/day05/example.txt"));
    try std.testing.expectEqual(5964, part1(allocator, "data/day05/input.txt"));
}

test "part 2" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(123, part2(allocator, "data/day05/example.txt"));
    try std.testing.expectEqual(4719, part2(allocator, "data/day05/input.txt"));
}
