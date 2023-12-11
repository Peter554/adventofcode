use anyhow::Result;
use std::{fs, path::Path};

use crate::utils::{BoundingBox2D, Point2D};

type Point = Point2D<i64>;

pub fn solve(input_path: &Path, expansion_factor: i64) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;

    // Parse the galaxies.
    let mut galaxies = vec![];
    for (y, row) in input.lines().enumerate() {
        for (x, c) in row.chars().enumerate() {
            if c == '#' {
                galaxies.push(Point::new(x as i64, y as i64));
            }
        }
    }

    // Expand the universe.
    let mut y = BoundingBox2D::from_points(&galaxies).unwrap().y_min;
    while y <= BoundingBox2D::from_points(&galaxies).unwrap().y_max {
        let row_is_empty = !galaxies.iter().any(|p| p.y == y);
        if row_is_empty {
            for galaxy in galaxies.iter_mut() {
                if galaxy.y > y {
                    galaxy.y += expansion_factor - 1;
                }
            }
            y += expansion_factor - 1;
        }
        y += 1;
    }
    let mut x = BoundingBox2D::from_points(&galaxies).unwrap().x_min;
    while x <= BoundingBox2D::from_points(&galaxies).unwrap().x_max {
        let column_is_empty = !galaxies.iter().any(|p| p.x == x);
        if column_is_empty {
            for galaxy in galaxies.iter_mut() {
                if galaxy.x > x {
                    galaxy.x += expansion_factor - 1;
                }
            }
            x += expansion_factor - 1;
        }
        x += 1;
    }

    // Find the total distance.
    // In this case the manhattan distance will always be the length of
    // the shortest path, no fancy pathfinding needed.
    let mut total_distance = 0;
    for (idx, galaxy) in galaxies.iter().enumerate() {
        for other_galaxy in galaxies.iter().skip(idx + 1) {
            total_distance += (galaxy.clone() - other_galaxy.clone()).manhattan();
        }
    }

    Ok(total_distance)
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day11/sample");
        assert_eq!(solve(input_path, 2).unwrap(), 374);

        let input_path = Path::new("./src/day11/input");
        assert_eq!(solve(input_path, 2).unwrap(), 9565386);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day11/input");
        assert_eq!(solve(input_path, 1_000_000).unwrap(), 857986849428);
    }
}
