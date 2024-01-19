from loguru import logger
from typing import Callable, Sequence

import os

from property_testing.property_set import PropertySet
from property_testing.run_tests import run_tests_for_property_set

from property_testing.defines import RUN_PROPERTY_TESTING, DEFAULT_NUM_OF_TESTS


def __should_run_property_testing() -> bool:
    return os.getenv(RUN_PROPERTY_TESTING) is not None


def property_testing(property_sets: Sequence[PropertySet]) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            if not hasattr(func, "_decorated") and __should_run_property_testing():
                logger.info(f"Run property_testing for {func.__name__}")
                for property_set in property_sets:
                    logger.info(
                        "Run property testing on property set with next params:"
                    )
                    logger.info(
                        f"Count tests: {property_set.count_tests if property_set.count_tests is not None else DEFAULT_NUM_OF_TESTS}"
                    )
                    logger.info(f"Predicates: {property_set.predicates}")
                    logger.info(
                        f"Arguments names: {[arg.argument_name for arg in property_set.arguments_info]}"
                    )
                    run_tests_for_property_set(
                        main_function=func, property_set=property_set
                    )
                func._decorated = True
            return func(*args, **kwargs)

        return wrapper

    return decorator
