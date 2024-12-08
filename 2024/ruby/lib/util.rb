# frozen_string_literal: true

module Util
  Point2D = Data.define(:x, :y)

  class Array2D
    def initialize(n_rows, n_cols)
      @n_rows = n_rows
      @n_cols = n_cols
      @data = Array.new(n_rows * n_cols)
    end

    def [](p)
      if p.instance_of? Point2D
        row_idx = p.y
        col_idx = p.x
      else
        row_idx, col_idx = p
      end

      raise IndexError if row_idx.negative? || row_idx >= @n_rows || col_idx.negative? || col_idx >= @n_cols

      @data[(row_idx * @n_cols) + col_idx]
    end

    def []=(p, value)
      if p.instance_of? Point2D
        row_idx = p.y
        col_idx = p.x
      else
        row_idx, col_idx = p
      end

      raise IndexError if row_idx.negative? || row_idx >= @n_rows || col_idx.negative? || col_idx >= @n_cols

      @data[(row_idx * @n_cols) + col_idx] = value
    end

    def self.parse(s)
      a = Array2D.new(
        s.split.length,
        s.split[0].length
      )
      s.split.each_with_index do |row, row_idx|
        row.chars.each_with_index do |char, col_idx|
          a[[row_idx, col_idx]] = char
        end
      end
      a
    end
  end
end
