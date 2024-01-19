from dataclasses import dataclass
from typing import Sequence, Optional

from property_testing.argument_info import ArgumentInfo


@dataclass
class PropertySet:
    """
    TODO
    This class...
    """

    count_tests: Optional[int]
    predicates: str | Sequence[str]
    arguments_info: Sequence[ArgumentInfo]


def create_property_set(
    count_tests: Optional[int],
    predicates: str | Sequence[str],
    arguments_info: Sequence[ArgumentInfo],
) -> PropertySet:
    return PropertySet(
        count_tests=count_tests, predicates=predicates, arguments_info=arguments_info
    )
