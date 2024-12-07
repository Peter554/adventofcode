# frozen_string_literal: true

require 'minitest/autorun'
require_relative '../lib/day01'

class TestDay01 < Minitest::Test
  def test_part1
    assert_equal 1_603_498, Day01.part1('data/day01/input')
  end

  def test_part2
    assert_equal 25_574_739, Day01.part2('data/day01/input')
  end
end
