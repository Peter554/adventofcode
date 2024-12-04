# frozen_string_literal: true

require 'minitest/autorun'
require_relative 'main'

class TestMain < Minitest::Test
  def test_part1
    assert_equal 299, part1('day02/input')
  end

  def test_part2
    assert_equal 364, part2('day02/input')
  end
end
