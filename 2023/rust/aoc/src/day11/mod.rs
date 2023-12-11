use anyhow::Result;
use std::{fs, path::Path};

use crate::utils::{BoundingBox2D, Point2D};

type Point = Point2D<i64>;

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;

    let mut galaxies = vec![];
    for (y, row) in input.lines().enumerate() {
        for (x, c) in row.chars().enumerate() {
            if c == '#' {
                galaxies.push(Point::new(x as i64, y as i64));
            }
        }
    }

    let mut y = BoundingBox2D::from_points(&galaxies).unwrap().y_min;
    while y <= BoundingBox2D::from_points(&galaxies).unwrap().y_max {
        let row_is_empty = !galaxies.iter().any(|p| p.y == y);
        if row_is_empty {
            for galaxy in galaxies.iter_mut() {
                if galaxy.y > y {
                    galaxy.y += 1;
                }
            }
            y += 1;
        }
        y += 1;
    }
    let mut x = BoundingBox2D::from_points(&galaxies).unwrap().x_min;
    while x <= BoundingBox2D::from_points(&galaxies).unwrap().x_max {
        let column_is_empty = !galaxies.iter().any(|p| p.x == x);
        if column_is_empty {
            for galaxy in galaxies.iter_mut() {
                if galaxy.x > x {
                    galaxy.x += 1;
                }
            }
            x += 1;
        }
        x += 1;
    }

    let mut total_distance = 0;
    for (idx, galaxy) in galaxies.iter().enumerate() {
        for other_galaxy in galaxies.iter().skip(idx + 1) {
            total_distance += (galaxy.clone() - other_galaxy.clone()).manhattan();
        }
    }

    Ok(total_distance)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    let _ = input;
    Ok(42)
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day11/sample");
        assert_eq!(part1(input_path).unwrap(), 374);

        let input_path = Path::new("./src/day11/input");
        assert_eq!(part1(input_path).unwrap(), 9565386);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day11/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
