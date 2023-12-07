set -e

if [[ -z $1 ]]; then
    echo "No day provided."
    exit 1
fi

export DAY=$(printf "%02d" $1)

mkdir ./src/day$DAY

touch ./src/day$DAY/sample
touch ./src/day$DAY/input

touch ./src/day$DAY/mod.rs
cat << EOF > ./src/day$DAY/mod.rs
use anyhow::Result;
use std::{fs, path::Path};

pub fn part1(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(42)
}

pub fn part2(input_path: &Path) -> Result<i64> {
    let input = fs::read_to_string(input_path)?;
    Ok(42)
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_part1() {
        let input_path = Path::new("./src/day$DAY/sample");
        assert_eq!(part1(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day$DAY/input");
        assert_eq!(part1(input_path).unwrap(), 42);
    }

    #[test]
    fn test_part2() {
        let input_path = Path::new("./src/day$DAY/sample");
        assert_eq!(part2(input_path).unwrap(), 42);

        let input_path = Path::new("./src/day$DAY/input");
        assert_eq!(part2(input_path).unwrap(), 42);
    }
}
EOF

echo "pub mod day$DAY;" >> ./src/lib.rs