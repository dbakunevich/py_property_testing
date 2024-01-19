from loguru import logger
from typing import Callable, Sequence, List

import random

from property_testing.property_set import PropertySet
from property_testing.argument_info import ArgumentInfo
from property_testing.property_testing_exception import PropertyTestingException

from property_testing.defines import DEFAULT_NUM_OF_TESTS


def __get_predicate(predicates: str | Sequence[str]) -> str:
    if isinstance(predicates, str):
        return predicates
    return random.choice(predicates)


def __evaluate_predicate(predicate_str, main_function_name, func, values):
    try:
        result = eval(predicate_str, values, {main_function_name: func})
        return result
    except Exception as e:
        logger.error(f"Error evaluating predicate: {e}")
        return False


def run_tests_for_property_set(main_function: Callable, property_set: PropertySet):
    if property_set.count_tests is None:
        property_set.count_tests = DEFAULT_NUM_OF_TESTS
    arguments_list: List[ArgumentInfo] = list(property_set.arguments_info)

    for cnt in range(property_set.count_tests):
        logger.info(f"Run test: {cnt}")
        predicate = __get_predicate(property_set.predicates)
        values = {arg.argument_name: arg.get_random_value() for arg in arguments_list}
        logger.info(f"Testing predicate: {predicate}")
        logger.info(f"With values: {values}")
        result = __evaluate_predicate(
            predicate,
            main_function_name=main_function.__name__,
            func=main_function,
            values=values,
        )
        if result:
            logger.success("The result of testing the predicate is True!")
        else:
            logger.error("The result of testing the predicate is False!")
            raise PropertyTestingException("TEST FAILED!")
        logger.info("")
