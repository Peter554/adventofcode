# frozen_string_literal: true

require 'minitest/autorun'
require_relative 'main'

class TestDay01 < Minitest::Test
  def test_part1
    assert_equal 1_603_498, part1('day01/input')
  end

  def test_part2
    assert_equal 25_574_739, part2('day01/input')
  end
end
