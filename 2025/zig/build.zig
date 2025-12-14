const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});
    const day_filter = b.option(u8, "day", "Specific day to test (1-25)");

    const test_step = b.step("test", "Run all tests");

    for (1..26) |day| {
        if (day_filter) |d| {
            if (d != day) continue;
        }

        const path = b.fmt("src/day{d:0>2}.zig", .{day});

        if (std.fs.cwd().access(path, .{})) {
            const day_tests = b.addTest(.{
                .root_module = b.createModule(.{
                    .root_source_file = b.path(path),
                    .target = target,
                    .optimize = optimize,
                }),
            });
            test_step.dependOn(&b.addRunArtifact(day_tests).step);
        } else |_| {}
    }
}
