# frozen_string_literal: true

require 'minitest/autorun'
require_relative 'main'

class TestMain < Minitest::Test
  def test_part1
    assert_equal 161_085_926, part1('day03/input')
  end

  def test_part2
    assert_equal 82_045_421, part2('day03/input')
  end
end
