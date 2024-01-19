from property_testing.property_testing import property_testing
from property_testing.property_set import create_property_set
from property_testing.argument_info import ArgumentInfo


def test_check() -> None:
    assert True
    return


def test_simple_func() -> None:
    @property_testing(
        property_sets=[
            create_property_set(
                1,
                "min(x, x) == x",
                [
                    ArgumentInfo(
                        argument_name="x",
                        argument_type="int",
                        corner_value=["-1", "0", "1"],
                        argument_constrains=["x > -10", "x < 10", "x in range(-5, 5)"],
                    )
                ],
            )
        ]
    )
    def min(x: int, y: int) -> int:
        if x < y:
            return x
        return y

    @property_testing(
        property_sets=[
            create_property_set(
                1,
                "min_m(x, x, x) == x",
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
    def min_m(x: int, y: int, z: int) -> int:
        if x < y and x < z:
            return x
        elif y < x and y < z:
            return y
        return z

    assert min_m(1, 2, 3) == 1
    assert False
