# frozen_string_literal: true

require 'minitest/autorun'
require_relative '../lib/day04'

class TestDay04 < Minitest::Test
  def test_part1
    assert_equal 18, Day04.part1('data/day04/example')
    assert_equal 2547, Day04.part1('data/day04/input')
  end

  def test_part2
    assert_equal 9, Day04.part2('data/day04/example')
    assert_equal 1939, Day04.part2('data/day04/input')
  end
end
