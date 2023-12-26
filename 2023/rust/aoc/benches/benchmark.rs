use aoc::day20;
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use std::path::Path;

pub fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("day 20 part 1", |b| {
        b.iter(|| day20::part1(black_box(Path::new("./src/day20/input"))))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
