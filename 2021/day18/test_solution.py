from day18 import solution


def test_explode() -> None:
    sfn = solution.SnailfishNumber.parse("[[[[[9,8],1],2],3],4]")
    node: solution.SnailfishNumber = sfn.left.left.left.left  # type:ignore
    assert node.depth == 4
    assert str(node) == "[9,8]"
    node.explode()
    assert str(sfn) == "[[[[0,9],2],3],4]"

    sfn = solution.SnailfishNumber.parse("[7,[6,[5,[4,[3,2]]]]]")
    node: solution.SnailfishNumber = sfn.right.right.right.right  # type:ignore
    assert node.depth == 4
    assert str(node) == "[3,2]"
    node.explode()
    assert str(sfn) == "[7,[6,[5,[7,0]]]]"

    sfn = solution.SnailfishNumber.parse("[[6,[5,[4,[3,2]]]],1]")
    node: solution.SnailfishNumber = sfn.left.right.right.right  # type:ignore
    assert node.depth == 4
    assert str(node) == "[3,2]"
    node.explode()
    assert str(sfn) == "[[6,[5,[7,0]]],3]"

    sfn = solution.SnailfishNumber.parse("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    node: solution.SnailfishNumber = sfn.left.right.right.right  # type:ignore
    assert node.depth == 4
    assert str(node) == "[7,3]"
    node.explode()
    assert str(sfn) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"

    sfn = solution.SnailfishNumber.parse("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    node: solution.SnailfishNumber = sfn.right.right.right.right  # type:ignore
    assert node.depth == 4
    assert str(node) == "[3,2]"
    node.explode()
    assert str(sfn) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"


def test_addition() -> None:
    sfn = solution.SnailfishNumber.parse("[[[[4,3],4],4],[7,[[8,4],9]]]")
    sfn = sfn + solution.SnailfishNumber.parse("[1,1]")
    assert str(sfn) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

    sfn = solution.SnailfishNumber.parse("[1,1]")
    sfn = sfn + solution.SnailfishNumber.parse("[2,2]")
    sfn = sfn + solution.SnailfishNumber.parse("[3,3]")
    sfn = sfn + solution.SnailfishNumber.parse("[4,4]")
    assert str(sfn) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    sfn = sfn + solution.SnailfishNumber.parse("[5,5]")
    assert str(sfn) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
    sfn = sfn + solution.SnailfishNumber.parse("[6,6]")
    assert str(sfn) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"

    sfn = solution.SnailfishNumber.parse("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
    sfn = sfn + solution.SnailfishNumber.parse("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
    assert str(sfn) == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
    sfn = sfn + solution.SnailfishNumber.parse(
        "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]"
    )
    assert str(sfn) == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"
    sfn = sfn + solution.SnailfishNumber.parse(
        "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]"
    )
    assert str(sfn) == "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"
    sfn = sfn + solution.SnailfishNumber.parse("[7,[5,[[3,8],[1,4]]]]")
    assert str(sfn) == "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]"


def test_magnitude() -> None:
    assert (
        solution.SnailfishNumber.parse(
            "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
        ).magnitude
        == 3488
    )


def test_part_1() -> None:
    assert solution.part_1("day18/sample") == 4140
    assert solution.part_1("day18/input") == 4132


def test_part_2() -> None:
    assert solution.part_2("day18/sample") == 3993
    assert solution.part_2("day18/input") == 4685
