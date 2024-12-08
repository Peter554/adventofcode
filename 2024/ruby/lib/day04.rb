# frozen_string_literal: true

require_relative 'util'

module Day04
  def self.part1(filepath)
    puzzle = Util::Array2D.parse(File.read(filepath))

    count = 0
    (0...puzzle.n_rows).each do |row|
      (0...puzzle.n_cols).each do |col|
        point = Util::Point2D[col, row]
        [
          Util::Point2D[-1, -1],
          Util::Point2D[0, -1],
          Util::Point2D[1, -1],
          Util::Point2D[-1, 0],
          Util::Point2D[1, 0],
          Util::Point2D[-1, 1],
          Util::Point2D[0, 1],
          Util::Point2D[1, 1]
        ].each do |direction|
          count += 1 if search_puzzle_xmas?(puzzle, point, direction)
        end
      end
    end
    count
  end

  def self.part2(filepath)
    puzzle = Util::Array2D.parse(File.read(filepath))

    count = 0
    (0...puzzle.n_rows).each do |row|
      (0...puzzle.n_cols).each do |col|
        point = Util::Point2D[col, row]
        count += 1 if search_puzzle_cross_mas?(puzzle, point)
      end
    end
    count
  end

  def self.search_puzzle_xmas?(puzzle, point, direction)
    s = ''
    (0...4).each do |_|
      s += puzzle[point]
      point += direction
    end
    s == 'XMAS'
  rescue IndexError
    false
  end

  def self.search_puzzle_cross_mas?(puzzle, point)
    s1 = puzzle[point + Util::Point2D[-1, 1]] + puzzle[point] + puzzle[point + Util::Point2D[1, -1]]
    s2 = puzzle[point + Util::Point2D[-1, -1]] + puzzle[point] + puzzle[point + Util::Point2D[1, 1]]
    %w[MAS SAM].include?(s1) && %w[MAS SAM].include?(s2)
  rescue IndexError
    false
  end
end
