from typing import Callable, Sequence, List

import re
import random
import inspect

from property_testing.property_set import PropertySet
from property_testing.argument_info import ArgumentInfo


def __get_predicate(predicates: str | Sequence[str]) -> str:
    if isinstance(predicates, str):
        return predicates
    return random.choice(predicates)


def __get_arguments_list(
    main_function_name: str, predicate: str, property_set: PropertySet
) -> List[ArgumentInfo]:
    def extract_arguments_from_function_string(
        main_function_name: str, function_string: str
    ) -> List[str]:
        pattern = re.compile(re.escape(f"{main_function_name}(") + r"(.*?)\)")
        variables_in_parentheses = re.findall(pattern, function_string)

        if variables_in_parentheses:
            variables = [var.strip() for var in variables_in_parentheses[0].split(",")]
            return variables
        else:
            return []

    arguments_name_from_predicate = extract_arguments_from_function_string(
        main_function_name, predicate
    )

    result: List[ArgumentInfo] = []
    for var in arguments_name_from_predicate:
        for arg in property_set.arguments_info:
            if var == arg.argument_name:
                result.append(arg)

    assert len(arguments_name_from_predicate) == len(result)
    return result


def __evaluate_predicate(predicate_str, main_function_name, func, **values):
    substituted_predicate = predicate_str
    for arg_name, arg_value in values.items():
        substituted_predicate = substituted_predicate.replace(arg_name, repr(arg_value))

    try:
        result = eval(
            substituted_predicate, globals(), {main_function_name: func, **values}
        )
        return result
    except Exception as e:
        print(f"Error evaluating predicate: {e}")
        return False


def run_tests_for_property_set(main_function: Callable, property_set: PropertySet):
    if property_set.count_tests is None:
        property_set.count_tests = 10
    for _ in range(property_set.count_tests):
        predicate = __get_predicate(property_set.predicates)
        print(predicate)
        print(main_function.__name__)
        arguments_list: List[ArgumentInfo] = __get_arguments_list(
            main_function.__name__, predicate, property_set
        )
        print(arguments_list)
        assert len(arguments_list) == len(inspect.signature(main_function).parameters)

        arguments_list = list(set(arguments_list))

        values = {arg.argument_name: arg.get_random_value() for arg in arguments_list}
        print(predicate)
        print(main_function)
        print(values)
        result = __evaluate_predicate(
            predicate,
            main_function_name=main_function.__name__,
            func=main_function,
            values=values,
        )
        if result:
            print("Good")
        else:
            print("Bad")
