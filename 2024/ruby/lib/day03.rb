# frozen_string_literal: true

module Day03
  def self.part1(filepath)
    File.readlines(filepath, chomp: true).join.scan(/mul\((\d{1,3}),(\d{1,3})\)/).map do |match|
      match[0].to_i * match[1].to_i
    end.sum
  end

  def self.part2(filepath)
    s = File.readlines(filepath, chomp: true).join

    sum = 0
    on = true
    until s.empty?
      case s
      when /^do\(\)/
        on = true
        s.slice!(...4)
      when /^don't\(\)/
        on = false
        s.slice!(...7)
      when /^mul\((\d{1,3}),(\d{1,3})\)/
        match = s.match(/^mul\((\d{1,3}),(\d{1,3})\)/)
        sum += match.captures[0].to_i * match.captures[1].to_i if on
        s.slice!(...match.to_s.length)
      else
        s.slice!(0)
      end
    end

    sum
  end
end
