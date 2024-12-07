# frozen_string_literal: true

module Day05
  def self.part1(filepath)
    ordering_rules, updates = parse(filepath)

    updates.filter_map do |u|
      ordered_update = order_update(u, ordering_rules)
      ordered_update == u ? ordered_update : nil
    end.map { |u| u[u.length / 2] }.sum
  end

  def self.part2(filepath)
    ordering_rules, updates = parse(filepath)

    updates.filter_map do |u|
      ordered_update = order_update(u, ordering_rules)
      ordered_update == u ? nil : ordered_update
    end.map { |u| u[u.length / 2] }.sum
  end

  def self.parse(filepath)
    s = File.read(filepath)

    ordering_rules = {}.tap do |h|
      s.split("\n\n")[0].split.each do |rule|
        earlier_page = rule.split('|')[0].to_i
        later_page = rule.split('|')[1].to_i
        if h.key?(earlier_page)
          h[earlier_page] << later_page
        else
          h[earlier_page] = Set[later_page]
        end
      end
    end

    updates = s.split("\n\n")[1].split.map do |update|
      update.split(',').map(&:to_i)
    end

    [ordering_rules, updates]
  end

  def self.order_update(update, ordering_rules)
    update.sort do |a, b|
      if ordering_rules.fetch(a, Set.new).include?(b)
        # a before b
        -1
      elsif ordering_rules.fetch(b, Set.new).include?(a)
        # a after b
        +1
      else
        0
      end
    end
  end
end
