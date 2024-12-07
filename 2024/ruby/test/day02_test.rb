# frozen_string_literal: true

require 'minitest/autorun'
require_relative '../lib/day02'

class TestDay02 < Minitest::Test
  def test_part1
    assert_equal 299, Day02.part1('data/day02/input')
  end

  def test_part2
    assert_equal 364, Day02.part2('data/day02/input')
  end
end
