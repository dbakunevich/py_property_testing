from typing import Callable, Sequence, Any

from property_testing.property_set import PropertySet
from property_testing.run_tests import run_tests_for_property_set


def property_testing(property_sets: Sequence[PropertySet]) -> Any:
    def decorator(func: Callable):
        for property_set in property_sets:
            run_tests_for_property_set(main_function=func, property_set=property_set)
