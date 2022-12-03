import { part1, part2 } from "./solution";

describe("solution", () => {
  it("solves part1", () => {
    expect(part1("day03/sample")).toEqual(157);
    expect(part1("day03/input")).toEqual(8394);
  });

  it("solves part2", () => {
    expect(part2("day03/sample")).toEqual(70);
    expect(part2("day03/input")).toEqual(2413);
  });
});
