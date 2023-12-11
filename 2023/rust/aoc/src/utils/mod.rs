use std::ops::{Add, Sub};

pub trait Int: num::Integer + num::Signed + From<i8> + Clone {}
impl<T: num::Integer + num::Signed + From<i8> + Clone> Int for T {}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct Point2D<T: Int> {
    pub x: T,
    pub y: T,
}

impl<T: Int> Add for Point2D<T> {
    type Output = Point2D<T>;

    fn add(self, rhs: Self) -> Self::Output {
        Point2D::new(self.x + rhs.x, self.y + rhs.y)
    }
}

impl<T: Int> Sub for Point2D<T> {
    type Output = Point2D<T>;

    fn sub(self, rhs: Self) -> Self::Output {
        Point2D::new(self.x - rhs.x, self.y - rhs.y)
    }
}

impl<T: Int> Point2D<T> {
    pub fn new(x: T, y: T) -> Point2D<T> {
        Point2D { x, y }
    }

    #[allow(dead_code)]
    pub fn manhattan(&self) -> T {
        self.x.abs() + self.y.abs()
    }

    #[allow(dead_code)]
    pub fn neighbors4(&self) -> impl Iterator<Item = Point2D<T>> {
        vec![
            self.clone() + Point2D::new(T::from(1), T::from(0)),
            self.clone() + Point2D::new(T::from(-1), T::from(0)),
            self.clone() + Point2D::new(T::from(0), T::from(1)),
            self.clone() + Point2D::new(T::from(0), T::from(-1)),
        ]
        .into_iter()
    }

    #[allow(dead_code)]
    pub fn neighbors8(&self) -> impl Iterator<Item = Point2D<T>> {
        vec![
            self.clone() + Point2D::new(T::from(1), T::from(0)),
            self.clone() + Point2D::new(T::from(-1), T::from(0)),
            self.clone() + Point2D::new(T::from(0), T::from(1)),
            self.clone() + Point2D::new(T::from(0), T::from(-1)),
            self.clone() + Point2D::new(T::from(1), T::from(1)),
            self.clone() + Point2D::new(T::from(-1), T::from(-1)),
            self.clone() + Point2D::new(T::from(-1), T::from(1)),
            self.clone() + Point2D::new(T::from(1), T::from(-1)),
        ]
        .into_iter()
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Hash)]
pub struct BoundingBox2D<T: Int> {
    pub x_min: T,
    pub x_max: T,
    pub y_min: T,
    pub y_max: T,
}

impl<T: Int> BoundingBox2D<T> {
    pub fn from_points<I>(points: &I) -> Option<BoundingBox2D<T>>
    where
        I: IntoIterator<Item = Point2D<T>> + Clone,
    {
        if points.clone().into_iter().count() == 0 {
            return None;
        }
        Some(BoundingBox2D {
            x_min: points.clone().into_iter().map(|p| p.x).min().unwrap(),
            x_max: points.clone().into_iter().map(|p| p.x).max().unwrap(),
            y_min: points.clone().into_iter().map(|p| p.y).min().unwrap(),
            y_max: points.clone().into_iter().map(|p| p.y).max().unwrap(),
        })
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use super::*;
    use maplit::hashset;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_point2d_add() {
        assert_eq!(Point2D::new(3, 7) + Point2D::new(4, -2), Point2D::new(7, 5))
    }

    #[test]
    fn test_point2d_subtract() {
        assert_eq!(
            Point2D::new(3, 7) - Point2D::new(4, -2),
            Point2D::new(-1, 9)
        )
    }

    #[test]
    fn test_point2d_manhattan() {
        assert_eq!(Point2D::new(-3, 5).manhattan(), 8)
    }

    #[test]
    fn test_point2d_neighbors4() {
        let point = Point2D::new(42, 21);
        assert_eq!(
            point.neighbors4().collect::<HashSet<_>>(),
            hashset! {
                Point2D::new(43,21),
                Point2D::new(41,21),
                Point2D::new(42,22),
                Point2D::new(42,20),
            }
        )
    }

    #[test]
    fn test_point2d_neighbors8() {
        let point = Point2D::new(42, 21);
        assert_eq!(
            point.neighbors8().collect::<HashSet<_>>(),
            hashset! {
                Point2D::new(41,20),
                Point2D::new(41,21),
                Point2D::new(41,22),
                Point2D::new(42,20),
                Point2D::new(42,22),
                Point2D::new(43,20),
                Point2D::new(43,22),
                Point2D::new(43,21),
            }
        )
    }

    #[test]
    fn test_bounding_box() {
        let points = vec![
            Point2D::new(3, 7),
            Point2D::new(-10, 2),
            Point2D::new(0, -5),
        ];
        assert!(BoundingBox2D::<i32>::from_points(&[]).is_none());
        assert_eq!(
            BoundingBox2D::from_points(&points).unwrap(),
            BoundingBox2D {
                x_min: -10,
                x_max: 3,
                y_min: -5,
                y_max: 7,
            }
        );
    }
}
