# frozen_string_literal: true

def part1(filepath)
  left = []
  right = []
  File.readlines(filepath, chomp: true).each do |line|
    left << line.split[0].to_i
    right << line.split[1].to_i
  end

  left.sort.zip(right.sort).sum do |l, r|
    (l - r).abs
  end
end

def part2(filepath)
  left = []
  right = []
  File.readlines(filepath, chomp: true).each do |line|
    left << line.split[0].to_i
    right << line.split[1].to_i
  end

  right_tally = right.tally

  left.sum do |l|
    l * right_tally.fetch(l, 0)
  end
end
