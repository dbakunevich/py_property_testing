from property_testing.property_testing import property_testing
from property_testing.property_set import create_property_set
from property_testing.argument_info import ArgumentInfo

@property_testing(
    property_sets=[
        create_property_set(
            20,
            [
                "xor_two(x, x) == 0",
                "xor_two(x, 0) == x",
                "xor_two(x, y) == xor_two(y, x)",
                "xor_two(x, y) == x ^ y",
                "xor_two(x, y) == ~x & y | x & ~y",
            ],
            [
                ArgumentInfo(
                    argument_name="x",
                    argument_type="int",
                    corner_value=["1", "10", "100"],
                    argument_constrains=["x > 0", "x < 20", "x in range(-50, 50)"],
                ),
                ArgumentInfo(
                    argument_name="y",
                    argument_type="int",
                    corner_value=["1", "2", "3"],
                    argument_constrains=[
                        "y > 0",
                        "y < 30",
                        "y in interval(-50, 50)",
                    ],
                ),
            ],
        )
    ]
    )
def xor_two(a: int, b: int) -> int:
    return a ^ b

print(xor_two(5, 6))
print(xor_two(5, 6))
