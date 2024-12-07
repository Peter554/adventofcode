# frozen_string_literal: true

module Day02
  def self.part1(filepath)
    reports = File.readlines(filepath, chomp: true).map do |line|
      line.split.map(&:to_i)
    end
    reports.filter do |report|
      safe(report)
    end.count
  end

  def self.part2(filepath)
    reports = File.readlines(filepath, chomp: true).map do |line|
      line.split.map(&:to_i)
    end
    reports.filter do |report|
      safe_with_tolerance(report)
    end.count
  end

  def self.safe(report)
    report.each_cons(2).map do |l, r|
      l < r and l >= r - 3
    end.all? or report.each_cons(2).map do |l, r|
      l > r and l <= r + 3
    end.all?
  end

  def self.safe_with_tolerance(report)
    return true if safe(report)

    (0...report.length).each do |idx|
      return true if safe(report.dup.tap { |r| r.delete_at(idx) })
    end
    false
  end
end
