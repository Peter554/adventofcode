from day24 import solution


def test_run_alu_program() -> None:
    program = """
inp x
mul x -1
"""
    assert solution.run_alu_program(program, (4,)) == (0, -4, 0, 0)

    program = """
inp z
inp x
mul z 3
eql z x
"""
    assert solution.run_alu_program(program, (4, 11)) == (0, 11, 0, 0)
    assert solution.run_alu_program(program, (4, 12)) == (0, 12, 0, 1)

    program = """
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""
    assert solution.run_alu_program(program, (0,)) == (0, 0, 0, 0)
    assert solution.run_alu_program(program, (1,)) == (0, 0, 0, 1)
    assert solution.run_alu_program(program, (2,)) == (0, 0, 1, 0)
    assert solution.run_alu_program(program, (3,)) == (0, 0, 1, 1)
    assert solution.run_alu_program(program, (4,)) == (0, 1, 0, 0)
    assert solution.run_alu_program(program, (5,)) == (0, 1, 0, 1)
    assert solution.run_alu_program(program, (6,)) == (0, 1, 1, 0)
    assert solution.run_alu_program(program, (7,)) == (0, 1, 1, 1)
    assert solution.run_alu_program(program, (8,)) == (1, 0, 0, 0)
    assert solution.run_alu_program(program, (9,)) == (1, 0, 0, 1)


def test_monad_is_valid() -> None:
    monads = (53999995829399, 11721151118175)
    for monad in monads:
        assert solution.monad_is_valid(monad)
        assert solution.monad_is_valid(monad) == solution.monad_is_valid_reduced(monad)
        for i in range(1, 10):
            # very unlikely...
            assert not solution.monad_is_valid(monad + i)
