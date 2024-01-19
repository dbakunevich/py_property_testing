from dataclasses import dataclass
from typing import Sequence, Optional, Any, List

import re
import sys
import random
from builtins import getattr

from sympy import S, Symbol, sympify, Interval, Union, solve_univariate_inequality


@dataclass
class ArgumentInfo:
    """
    TODO
    This class...
    """

    argument_name: str
    argument_type: str
    corner_value: Optional[str | Sequence[str]]
    argument_constrains: Optional[str | Sequence[str]]

    @property
    def argument_symbol(self) -> Symbol:
        return Symbol(self.argument_name)

    @property
    def ranges_of_acceptable_value(self) -> Union:
        if self.argument_type == "int":
            max_value_int = sys.maxsize
            min_value_int = -max_value_int - 1
            bounds: List[Interval | Any] = [Interval(min_value_int, max_value_int)]

        elif self.argument_type == "float":
            max_value_float = sys.float_info.max
            min_value_float = -sys.float_info.max
            bounds = [Interval(min_value_float, max_value_float)]

        else:
            assert False, "Right now can work only with int and float arguments"

        if self.argument_constrains is None:
            return Union(bounds)
        elif isinstance(self.argument_constrains, str):
            self.argument_constrains = [self.argument_constrains]

        for constraint in self.argument_constrains:
            if (self.argument_name.lower() + " in interval") in constraint.lower() or (
                self.argument_name.lower() + " in range"
            ) in constraint.lower():
                values_in_brackets = re.search(r"\((.*?)\)", constraint)
                if values_in_brackets is None:
                    print("WARNING: can't parse range constraint %s" % constraint)
                    continue
                values: List[str] = values_in_brackets.group(1).split(",")
                if len(values) != 2:
                    print(
                        "WARNING: in range constraint %s more or less them 2 values"
                        % constraint
                    )
                    continue
                bounds.append(Interval(float(values[0]), float(values[1])))
            elif any(char in constraint.lower() for char in ["<", "=", ">"]):
                try:
                    constraint_expression = sympify(constraint)
                    solution = solve_univariate_inequality(
                        constraint_expression,
                        self.argument_symbol,
                        relational=False,
                    )
                    if isinstance(solution, Interval):
                        # Single interval case
                        bounds.append(solution)
                    elif solution.is_Or:
                        # Handle multiple intervals
                        for interval in solution.args:
                            bounds.append(Interval(interval.start, interval.end))
                    else:
                        print(
                            f"WARNING: Unexpected result from solve_univariate_inequality: {solution}"
                        )
                except Exception as e:
                    print(f"WARNING: can't parse this inequality {constraint}; {e}")
                    continue
            else:
                print("WARNING: can't parse this constraint %s" % constraint)
                continue
        return Union(*[constr for constr in bounds])

    @property
    def argument_type_type(self) -> type:
        try:
            return getattr(__builtins__, self.argument_type)
        except AttributeError:
            try:
                import builtins

                return getattr(builtins, self.argument_type)
            except AttributeError:
                raise ValueError(f"Unsupported argument_type: {self.argument_type}")

    @property
    def corner_values_list_casts(self) -> Sequence[Any]:
        if self.corner_value is None:
            return []
        return [self.argument_type_type(val) for val in self.corner_value]

    def get_random_value_from_interval(self, intervals: Union):
        for _ in range(10):
            try:
                if intervals.is_Union:
                    valid_intervals = [
                        interval for interval in intervals.args if interval.is_Interval
                    ]
                    if not valid_intervals:
                        raise ValueError("No valid Interval found in Union")

                    random_interval = random.choice(valid_intervals)
                elif intervals.is_Interval:
                    random_interval = intervals
                else:
                    raise ValueError("Invalid type of intervals")

                if random_interval.start == S.NegativeInfinity:
                    start_value = -sys.maxsize - 1
                else:
                    start_value = random_interval.start

                if random_interval.end == S.Infinity:
                    end_value = sys.maxsize
                else:
                    end_value = random_interval.end

                random_value = random.uniform(start_value, end_value)
                return self.argument_type_type(random_value)

            except Exception as e:
                print(f"WARNING: Error while generating random value; {e}")
        if len(self.corner_values_list_casts) != 0:
            return random.choice(self.corner_values_list_casts)
        raise ValueError("Can't get num from interval")

    def get_random_value(self) -> Any:
        if (
            len(self.corner_values_list_casts) == 0
            and len(self.ranges_of_acceptable_value.args) == 0
        ):
            assert False, "Can't possible argument values"
        elif len(self.corner_values_list_casts) == 0:
            intervals = self.ranges_of_acceptable_value
            return self.get_random_value_from_interval(intervals)
        elif len(self.ranges_of_acceptable_value.args) == 0:
            return random.choice(self.corner_values_list_casts)
        else:
            random_number = random.random()
            if random_number < 0.25:
                return random.choice(self.corner_values_list_casts)
            else:
                intervals = self.ranges_of_acceptable_value
                return self.get_random_value_from_interval(intervals)

    def __eq__(self, other):
        return (
            isinstance(other, ArgumentInfo)
            and self.argument_name == other.argument_name
        )

    def __hash__(self):
        return hash(self.argument_name)
