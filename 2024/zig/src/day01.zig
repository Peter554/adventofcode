const std = @import("std");

pub fn part1(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const left_numbers, const right_numbers = try parseInput(allocator, input_path);
    defer allocator.free(left_numbers);
    defer allocator.free(right_numbers);

    std.mem.sort(u64, left_numbers, {}, std.sort.asc(u64));
    std.mem.sort(u64, right_numbers, {}, std.sort.asc(u64));

    var distance: u64 = 0;
    for (left_numbers, right_numbers) |l, r| {
        distance += if (l > r) l - r else r - l;
    }
    return distance;
}

pub fn part2(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const left_numbers, const right_numbers = try parseInput(allocator, input_path);
    defer allocator.free(left_numbers);
    defer allocator.free(right_numbers);

    var right_number_counts = std.AutoHashMap(u64, u64).init(allocator);
    defer right_number_counts.deinit();
    for (right_numbers) |r| {
        const entry = try right_number_counts.getOrPut(r);
        entry.value_ptr.* = if (entry.found_existing) entry.value_ptr.* + 1 else 1;
    }

    var similarity: u64 = 0;
    for (left_numbers) |l| {
        similarity += l * (right_number_counts.get(l) orelse 0);
    }
    return similarity;
}

fn parseInput(allocator: std.mem.Allocator, input_path: []const u8) !struct { []u64, []u64 } {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);

    var left_numbers = try std.ArrayList(u64).initCapacity(allocator, 1024);
    defer left_numbers.deinit(allocator);
    var right_numbers = try std.ArrayList(u64).initCapacity(allocator, 1024);
    defer right_numbers.deinit(allocator);

    var lines = std.mem.tokenizeScalar(u8, file, '\n');
    while (lines.next()) |line| {
        var columns = std.mem.tokenizeScalar(u8, line, ' ');
        try left_numbers.append(allocator, try std.fmt.parseInt(u64, columns.next().?, 10));
        try right_numbers.append(allocator, try std.fmt.parseInt(u64, columns.next().?, 10));
    }

    return .{
        try left_numbers.toOwnedSlice(allocator),
        try right_numbers.toOwnedSlice(allocator),
    };
}

test "part 1" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(1603498, part1(allocator, "data/day01/input.txt"));
}

test "part 2" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(25574739, part2(allocator, "data/day01/input.txt"));
}
