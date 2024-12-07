# frozen_string_literal: true

require 'minitest/autorun'
require_relative '../lib/day03'

class TestDay03 < Minitest::Test
  def test_part1
    assert_equal 161_085_926, Day03.part1('data/day03/input')
  end

  def test_part2
    assert_equal 82_045_421,  Day03.part2('data/day03/input')
  end
end
