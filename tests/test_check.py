from property_testing.property_testing import property_testing
from property_testing.property_set import create_property_set
from property_testing.argument_info import ArgumentInfo


def test_check() -> None:
    assert True
    return


def test_min_2_func() -> None:
    @property_testing(
        property_sets=[
            create_property_set(
                None,
                [
                    "min_two(x, x) == x",
                    "min_two(x, x + 1) == x",
                    "min_two(y, x) == min_two(x, y)",
                ],
                [
                    ArgumentInfo(
                        argument_name="x",
                        argument_type="int",
                        corner_value=["-1", "0", "1"],
                        argument_constrains=["x > 0", "x < 10", "x in range(-50, 50)"],
                    ),
                    ArgumentInfo(
                        argument_name="y",
                        argument_type="int",
                        corner_value=["-1", "0", "1"],
                        argument_constrains=[
                            "y > -10",
                            "y < 30",
                            "y in interval(-50, 50)",
                        ],
                    ),
                ],
            )
        ]
    )
    def min_two(x: int, y: int) -> int:
        if x < y:
            return x
        return y

    assert min_two(2, 3) == 2


def test_min_3_func() -> None:
    @property_testing(
        property_sets=[
            create_property_set(
                1,
                "min_three(x, x, x) == x",
                [
                    ArgumentInfo(
                        argument_name="x",
                        argument_type="int",
                        corner_value=["-1", "0", "1"],
                        argument_constrains=["x > -10", "x < 10", "x in range(-5, 5)"],
                    )
                ],
            ),
        ]
    )
    def min_three(x: int, y: int, z: int) -> int:
        if x < y and x < z:
            return x
        elif y < x and y < z:
            return y
        return z

    assert min_three(1, 2, 3) == 1
