import { readFileSync } from "fs";

export function part1(filePath: string): number {
  const fileData = readFileSync(filePath, { encoding: "utf8" }).split("\n");
  let prioritySum = 0;
  fileData.forEach((rucksackContents) => {
    const rucksackSize = rucksackContents.length;
    const compartment1Contents = rucksackContents.slice(0, rucksackSize / 2);
    const compartment2Contents = rucksackContents.slice(rucksackSize / 2);
    const compartmentIntersection = setIntersection(
      new Set(compartment1Contents.split("")),
      new Set(compartment2Contents.split(""))
    );
    let commonItem = [...compartmentIntersection][0];
    if (commonItem.toLowerCase() != commonItem) {
      commonItem = commonItem.toLowerCase();
      prioritySum += 26;
    }
    prioritySum += commonItem.charCodeAt(0) - 96;
  });
  return prioritySum;
}

export function part2(filePath: string): number {
  const fileData = readFileSync(filePath, { encoding: "utf8" }).split("\n");
  let prioritySum = 0;
  for (let i = 0; i < fileData.length - 2; i += 3) {
    const elfGroupRucksacks = fileData.slice(i, i + 3);
    const commonItems = elfGroupRucksacks
      .map((rucksack) => rucksack.split(""))
      .map((rucksackContents) => new Set(rucksackContents))
      .reduce((state, action) => {
        return setIntersection(state, action);
      });
    let commonItem = [...commonItems][0];
    if (commonItem.toLowerCase() != commonItem) {
      commonItem = commonItem.toLowerCase();
      prioritySum += 26;
    }
    prioritySum += commonItem.charCodeAt(0) - 96;
  }
  return prioritySum;
}

function setIntersection<T>(s1: Set<T>, s2: Set<T>): Set<T> {
  return new Set([...s1].filter((element) => s2.has(element)));
}
