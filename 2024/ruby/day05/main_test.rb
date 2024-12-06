# frozen_string_literal: true

require 'minitest/autorun'
require_relative 'main'

class TestMain < Minitest::Test
  def test_part1
    assert_equal 143, part1('day05/example')
    assert_equal 5964, part1('day05/input')
  end

  def test_part2
    assert_equal 123, part2('day05/example')
    assert_equal 4719, part2('day05/input')
  end
end
