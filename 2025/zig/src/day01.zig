const std = @import("std");

fn part1(allocator: std.mem.Allocator, input_path: []const u8) !i64 {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);
    var lines = std.mem.splitScalar(u8, file, '\n');

    var dial: i64 = 50;
    var password: i64 = 0;

    while (lines.next()) |line| {
        if (line.len == 0) continue;
        const delta_dial = try std.fmt.parseInt(i64, line[1..], 10);
        if (line[0] == 'R') {
            dial = @mod(dial + delta_dial, 100);
        } else {
            dial = @mod(dial - delta_dial, 100);
        }
        if (dial == 0) {
            password += 1;
        }
    }

    return password;
}

fn part2(allocator: std.mem.Allocator, input_path: []const u8) !i64 {
    const file = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(file);
    var lines = std.mem.splitScalar(u8, file, '\n');

    var dial: i64 = 50;
    var password: i64 = 0;

    while (lines.next()) |line| {
        if (line.len == 0) continue;
        const delta_dial = try std.fmt.parseInt(i64, line[1..], 10);
        if (line[0] == 'R') {
            password += @divFloor(dial + delta_dial, 100);
            dial = @mod(dial + delta_dial, 100);
        } else {
            if (delta_dial >= dial) {
                if (dial == 0) {
                    password += @divFloor(delta_dial, 100);
                } else {
                    password += 1 + @divFloor(delta_dial - dial, 100);
                }
            }
            dial = @mod(dial - delta_dial, 100);
        }
    }

    return password;
}

test "part 1" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(980, part1(allocator, "data/day01/input.txt"));
}

test "part 2" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(5961, part2(allocator, "data/day01/input.txt"));
}
