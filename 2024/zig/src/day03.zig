const std = @import("std");

pub fn part1(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const data = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(data);

    var total: u64 = 0;
    var rest: []const u8 = data;
    while (true) {
        if (mul().parse(rest)) |ok| {
            const value, rest = ok;
            total += value;
        } else |_| if (anyOneChar().parse(rest)) |ok| {
            _, rest = ok;
        } else |_| {
            break; // EOF.
        }
    }

    return total;
}

pub fn part2(allocator: std.mem.Allocator, input_path: []const u8) !u64 {
    const data = try std.fs.cwd().readFileAlloc(input_path, allocator, .unlimited);
    defer allocator.free(data);

    var enabled: bool = true;
    var total: u64 = 0;
    var rest: []const u8 = data;
    while (true) {
        if (mul().parse(rest)) |ok| {
            const value, rest = ok;
            if (enabled) {
                total += value;
            }
        } else |_| if (literal("do()").parse(rest)) |ok| {
            _, rest = ok;
            enabled = true;
        } else |_| if (literal("don't()").parse(rest)) |ok| {
            _, rest = ok;
            enabled = false;
        } else |_| if (anyOneChar().parse(rest)) |ok| {
            _, rest = ok;
        } else |_| {
            break; // EOF.
        }
    }

    return total;
}

const ParseError = error{FailedToParse};

fn Parser(comptime T: type) type {
    return struct {
        const Self = @This();
        const Ok = struct { T, []const u8 };

        parseFn: *const fn ([]const u8) ParseError!Ok,

        fn parse(self: Self, input: []const u8) ParseError!Ok {
            return self.parseFn(input);
        }
    };
}

const StringParser = Parser([]const u8);
const NumberParser = Parser(u64);

fn literal(comptime lit: []const u8) StringParser {
    const Closure = struct {
        fn parse(input: []const u8) ParseError!StringParser.Ok {
            if (lit.len <= input.len and std.mem.eql(u8, lit, input[0..lit.len])) {
                return .{ input[0..lit.len], input[lit.len..] };
            } else {
                return ParseError.FailedToParse;
            }
        }
    };
    return .{ .parseFn = Closure.parse };
}

fn digit() StringParser {
    const Closure = struct {
        fn parse(input: []const u8) ParseError!StringParser.Ok {
            if (input.len > 0 and input[0] >= '0' and input[0] <= '9') {
                return .{ input[0..1], input[1..] };
            } else {
                return ParseError.FailedToParse;
            }
        }
    };
    return .{ .parseFn = Closure.parse };
}

fn oneOrMore(comptime p: StringParser) StringParser {
    const Closure = struct {
        fn parse(input: []const u8) ParseError!StringParser.Ok {
            var value, var rest = try p.parse(input);

            var i = value.len;
            while (true) {
                if (p.parse(rest)) |r| {
                    value, rest = r;
                    i += value.len;
                } else |_| {
                    break;
                }
            }

            return .{ input[0..i], input[i..] };
        }
    };
    return .{ .parseFn = Closure.parse };
}

fn number() NumberParser {
    const Closure = struct {
        fn parse(input: []const u8) ParseError!NumberParser.Ok {
            const value_str, const rest = try oneOrMore(digit()).parse(input);
            const value = std.fmt.parseInt(u64, value_str, 10) catch return ParseError.FailedToParse;
            return .{ value, rest };
        }
    };
    return .{ .parseFn = Closure.parse };
}

fn mul() NumberParser {
    const Closure = struct {
        fn parse(input: []const u8) ParseError!NumberParser.Ok {
            _, var rest = try literal("mul(").parse(input);
            const a, rest = try number().parse(rest);
            _, rest = try literal(",").parse(rest);
            const b, rest = try number().parse(rest);
            _, rest = try literal(")").parse(rest);
            return .{ a * b, rest };
        }
    };
    return .{ .parseFn = Closure.parse };
}

fn anyOneChar() StringParser {
    const Closure = struct {
        fn parse(input: []const u8) ParseError!StringParser.Ok {
            if (input.len == 0) return ParseError.FailedToParse;
            return .{ input[0..1], input[1..] };
        }
    };
    return .{ .parseFn = Closure.parse };
}

test "part 1" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(161085926, part1(allocator, "data/day03/input.txt"));
}

test "part 2" {
    const allocator = std.testing.allocator;
    try std.testing.expectEqual(82045421, part2(allocator, "data/day03/input.txt"));
}
