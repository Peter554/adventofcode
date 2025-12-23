const std = @import("std");

pub fn part1(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);

    const grid = try Grid.parse(allocator, file);
    defer grid.deinit(allocator);

    var count: u64 = 0;
    for (0..grid.width) |x| {
        for (0..grid.height) |y| {
            const xi: isize = @intCast(x);
            const yi: isize = @intCast(y);
            for ([_]i8{ -1, 0, 1 }) |dx| {
                for ([_]i8{ -1, 0, 1 }) |dy| {
                    if (dx == 0 and dy == 0) continue;
                    const word = [_]u8{
                        grid.get(xi, yi) catch continue,
                        grid.get(xi + dx, yi + dy) catch continue,
                        grid.get(xi + 2 * dx, yi + 2 * dy) catch continue,
                        grid.get(xi + 3 * dx, yi + 3 * dy) catch continue,
                    };
                    if (std.mem.eql(u8, &word, "XMAS")) {
                        count += 1;
                    }
                }
            }
        }
    }

    return count;
}

pub fn part2(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);

    const grid = try Grid.parse(allocator, file);
    defer grid.deinit(allocator);

    var count: u64 = 0;
    for (0..grid.width) |x| {
        for (0..grid.height) |y| {
            const xi: isize = @intCast(x);
            const yi: isize = @intCast(y);

            const word1 = [_]u8{
                grid.get(xi - 1, yi - 1) catch continue,
                grid.get(xi, yi) catch continue,
                grid.get(xi + 1, yi + 1) catch continue,
            };

            const word2 = [_]u8{
                grid.get(xi - 1, yi + 1) catch continue,
                grid.get(xi, yi) catch continue,
                grid.get(xi + 1, yi - 1) catch continue,
            };

            if (std.mem.eql(u8, &word1, "MAS") or std.mem.eql(u8, &word1, "SAM")) {
                if (std.mem.eql(u8, &word2, "MAS") or std.mem.eql(u8, &word2, "SAM")) {
                    count += 1;
                }
            }
        }
    }

    return count;
}

const Grid = struct {
    const Self = @This();

    data: []const u8,
    width: usize, // x-dimension
    height: usize, // y-dimension

    fn parse(allocator: std.mem.Allocator, text: []const u8) !Self {
        var data = try std.ArrayList(u8).initCapacity(allocator, 1024);
        defer data.deinit(allocator);

        var line_iter = std.mem.tokenizeScalar(u8, text, '\n');
        var width: usize = 0;
        while (line_iter.next()) |line| {
            if (width == 0) width = line.len;
            try data.appendSlice(allocator, line);
        }
        const height = data.items.len / width;

        return .{
            .data = try data.toOwnedSlice(allocator),
            .width = width,
            .height = height,
        };
    }

    fn deinit(self: Self, allocator: std.mem.Allocator) void {
        allocator.free(self.data);
    }

    fn get(self: Self, x: isize, y: isize) !u8 {
        if (x < 0 or y < 0) return error.OutOfBounds;
        const xu: usize = @intCast(x);
        const yu: usize = @intCast(y);
        if (xu >= self.width or yu >= self.height) return error.OutOfBounds;
        return self.data[yu * self.width + xu];
    }
};

test "part 1" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(18, part1(allocator, "data/day04/example.txt"));
    try std.testing.expectEqual(2547, part1(allocator, "data/day04/input.txt"));
}

test "part 2" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(9, part2(allocator, "data/day04/example.txt"));
    try std.testing.expectEqual(1939, part2(allocator, "data/day04/input.txt"));
}
