from property_testing.property_testing import property_testing
from property_testing.property_set import create_property_set
from property_testing.argument_info import ArgumentInfo

@property_testing(
    property_sets=[
        create_property_set(
            20,
            [
                "min(x, x) == x",
                "min(x, x + 1) == x",
                "min(y, x) == min(x, y)",
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
                    argument_type="float",
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
def min(x: int, y: float):
    if x < y:
        return x
    return y

print(min(5, 5.001))
