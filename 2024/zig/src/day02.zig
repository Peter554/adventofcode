const std = @import("std");

pub fn part1(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const reports = try parseInput(allocator, input_path);
    defer {
        for (reports) |report| {
            allocator.free(report);
        }
        allocator.free(reports);
    }

    var safe: u64 = 0;
    for (reports) |report| {
        if (isSafe(report, null)) {
            safe += 1;
        }
    }

    return safe;
}

pub fn part2(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const reports = try parseInput(allocator, input_path);
    defer {
        for (reports) |report| {
            allocator.free(report);
        }
        allocator.free(reports);
    }

    var safe: u64 = 0;
    reports: for (reports) |report| {
        if (isSafe(report, null)) {
            safe += 1;
            continue :reports;
        }

        for (0..report.len) |i| {
            if (isSafe(report, i)) {
                safe += 1;
                continue :reports;
            }
        }
    }

    return safe;
}

fn parseInput(allocator: std.mem.Allocator, input_path: []const u8) ![][]i64 {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);

    var reports = try std.ArrayList([]i64).initCapacity(allocator, 1024);
    defer reports.deinit(allocator);

    var lines_iter = std.mem.tokenizeScalar(u8, file, '\n');
    while (lines_iter.next()) |report| {
        var levels = try std.ArrayList(i64).initCapacity(allocator, 16);
        defer levels.deinit(allocator);
        var level_iter = std.mem.tokenizeScalar(u8, report, ' ');
        while (level_iter.next()) |level_str| {
            const level = try std.fmt.parseInt(i64, level_str, 10);
            try levels.append(allocator, level);
        }
        try reports.append(allocator, try levels.toOwnedSlice(allocator));
    }

    return try reports.toOwnedSlice(allocator);
}

fn isSafe(report: []i64, skip_level_idx: ?usize) bool {
    var previous_level: ?i64 = null;
    var previous_delta: ?i64 = null;
    for (report, 0..) |level, idx| {
        if (skip_level_idx == idx) continue;
        if (previous_level) |pl| {
            const delta = level - pl;
            if (delta == 0 or @abs(delta) > 3) {
                return false;
            }
            if (previous_delta) |pd| {
                if (delta * pd < 0) {
                    return false;
                }
            }
            previous_delta = delta;
        }
        previous_level = level;
    }
    return true;
}

test "part 1" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(299, part1(allocator, "data/day02/input.txt"));
}

test "part 2" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(364, part2(allocator, "data/day02/input.txt"));
}
