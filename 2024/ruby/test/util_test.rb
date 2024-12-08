# frozen_string_literal: true

require 'minitest/autorun'
require_relative '../lib/util'

module UtilTest
  class Array2DTest < Minitest::Test
    def test_parse
      s = "ABC
DEF"

      a = Util::Array2D.parse(s)

      assert_equal 'A', a[[0, 0]]
      assert_equal 'B', a[[0, 1]]
      assert_equal 'C', a[[0, 2]]
      assert_equal 'D', a[[1, 0]]
      assert_equal 'E', a[[1, 1]]
      assert_equal 'F', a[[1, 2]]
    end
  end
end
