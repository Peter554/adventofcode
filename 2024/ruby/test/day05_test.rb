# frozen_string_literal: true

require 'minitest/autorun'
require_relative '../lib/day05'

class TestDay05 < Minitest::Test
  def test_part1
    assert_equal 143, Day05.part1('data/day05/example')
    assert_equal 5964, Day05.part1('data/day05/input')
  end

  def test_part2
    assert_equal 123, Day05.part2('data/day05/example')
    assert_equal 4719, Day05.part2('data/day05/input')
  end
end
