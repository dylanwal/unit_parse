from typing import Union, Any
from enum import Enum
import math

from unit_parse.config import Quantity
from unit_parse.utils import quantity_approx_equal
from unit_parse.logger import log_debug, log_info


class QuantClass(Enum):
    """ Classifications for data. """
    NUMBER = 0
    SINGLE = 1
    SERIES = 2
    CONDITIONS = 3
    SERIES_CONDITIONS = 4


@log_info
def reduce_quantities(data_in: Any,
                      order: tuple[QuantClass] = (QuantClass.SERIES_CONDITIONS,
                                                  QuantClass.CONDITIONS,
                                                  QuantClass.SERIES,
                                                  QuantClass.SINGLE,
                                                  QuantClass.NUMBER)) -> Quantity:
    """

    Ordering of returned quantity is set by QuantClass
    default ordering:
    series condition (largest series) > conditions > series (largest series) >
    single (highest repeated) > single (middle value with most common unit) > number (highest
    repeated) > single (middle value with most common unit)

    Parameters
    ----------
    data_in: Any

    order: tuple[int]
        See QuantClass for integer values

    Returns
    -------
    output: Any

    """
    if isinstance(data_in, list) and data_in != []:
        if len(data_in) <= 1:
            return data_in[0]

        data_dict = quantity_list_to_dict(data_in)
        return _select_from_data_dict(data_dict, order=order)

    return data_in


@log_debug
def quantity_list_to_dict(data_in: list[Any]) -> dict:
    """ quantity list to dict

    Generates a dict from list inside list, doing some classification.

    Parameters
    ----------
    data_in: list[Any]

    Returns
    -------
    output: dict
        "Quantity" : {"type": QuantClass(Enum),"count": int}

    """
    data_dict = {}
    for i, data in enumerate(data_in):
        if isinstance(data, Quantity):
            # if data is similar to existing, increase count
            if any([quantity_approx_equal(data, v["quantity"]) for v in data_dict.values()]):
                for k, v in data_dict.items():
                    if quantity_approx_equal(data, v["quantity"]):
                        data_dict[k]["count"] += 1
            else:
                # new data
                data_dict[i] = {"quantity": data, "count": 1, "type": QuantClass.SINGLE}

        elif isinstance(data, (int, float)):
            # if data is similar to existing, increase count
            if any([math.isclose(data, v["quantity"], rel_tol=0.05) for v in data_dict.values()]):
                for k, v in data_dict.items():
                    if math.isclose(data, v["quantity"], rel_tol=0.05):
                        data_dict[k]["count"] += 1
            else:
                # new data
                data_dict[i] = {"quantity": data, "count": 1, "type": QuantClass.NUMBER}

        elif isinstance(data, list):
            if isinstance(data[0], list):
                if len(data) == 1:
                    data_dict[i] = {"quantity": data, "count": 1, "type": QuantClass.CONDITIONS}
                else:
                    data_dict[i] = {
                        "quantity": data, "count": 1, "len": len(data[0]),
                        "type": QuantClass.SERIES_CONDITIONS
                    }
            else:
                data_dict[i] = {"quantity": data, "count": 1, "len": len(data), "type": QuantClass.SERIES}

    return data_dict


@log_debug
def _select_from_data_dict(data_dict: dict, order: tuple[QuantClass]) -> Union[list[Quantity], Quantity]:
    """
    Select the list or Quantity that is most likely to be right.
    Rules: Series_conditions > conditions > single (mean of single)
    """
    if len(data_dict.keys()) == 1:
        return data_dict[0]["quantity"]

    for order_ in order:
        # check if QuantClass in dict in order given by 'order' parameter
        keys_of_hits = [k for k, v in data_dict.items() if order_ == v["type"]]
        if len(keys_of_hits) == 0:
            continue
        elif len(keys_of_hits) == 1:
            return data_dict[keys_of_hits[0]]["quantity"]
        else:
            if order_ == QuantClass.SERIES_CONDITIONS or order_ == QuantClass.SERIES:
                # get one with largest series
                lens = [data_dict[k]["len"] for k in keys_of_hits]
                key_largest = keys_of_hits[lens.index(max(lens))]
                key_largest = double_check_output(data_dict, key_largest)
                return data_dict[key_largest]["quantity"]

            elif order_ == QuantClass.CONDITIONS:
                key = double_check_output(data_dict, keys_of_hits[0])
                return data_dict[key]["quantity"]

            elif order_ == QuantClass.SINGLE or order_ == QuantClass.NUMBER:
                # get one with most counts
                counts = [data_dict[k]["count"] for k in keys_of_hits]
                if max(counts) > 1:
                    key_most_counts = keys_of_hits[counts.index(max(counts))]
                    return data_dict[key_most_counts]["quantity"]

                # get one in the middle
                list_of_quantities = [data_dict[k]["quantity"] for k in keys_of_hits]
                return _get_middle_quantity(_filter_out_by_dimensionality(list_of_quantities))
    else:
        raise ValueError(f"Order parameter issue.")


@log_debug
def _filter_out_by_dimensionality(data_in: list[Quantity]) -> list[Quantity]:
    """ Find most common dimension and filter out any bad ones."""

    unit_dimensionality_count = {}
    for data in data_in:
        if data.dimensionality not in unit_dimensionality_count:
            unit_dimensionality_count[data.dimensionality] = 1
        else:
            unit_dimensionality_count[data.dimensionality] += 1

    most_common_unit = max(unit_dimensionality_count, key=unit_dimensionality_count.get)
    return [data for data in data_in if most_common_unit == data.dimensionality]


@log_debug
def _get_middle_quantity(data_in: list[Quantity]) -> Quantity:
    """ Remove data furthest from average till 1 point left."""
    for i in range(len(data_in) - 1):
        data_average = sum([data.to_base_units() for data in data_in]) / len(data_in)
        differance_list = [abs(data.to_base_units() - data_average) for data in data_in]
        data_in.pop(differance_list.index(max(differance_list)))

    return data_in[0]


def double_check_output(data_dict: dict, most_promising_key):
    """ Check conditions, series and condition series against single (if there is a popular single). If unit dimensions
    don't match, take single. """
    keys_of_hits = [k for k, v in data_dict.items() if QuantClass.SINGLE == v["type"]]
    counts = [data_dict[k]["count"] for k in keys_of_hits]
    if max(counts) > 1:
        if data_dict[most_promising_key]["type"] == QuantClass.SERIES_CONDITIONS or \
                data_dict[most_promising_key]["type"] == QuantClass.CONDITIONS:
            quantity = data_dict[most_promising_key]["quantity"][0][0]
        else:  # data_dict[most_promising_key]["type"] == QuantClass.SERIES:
            quantity = data_dict[most_promising_key]["quantity"][0]

        single_quantity_key = keys_of_hits[counts.index(max(counts))]
        single_quantity = data_dict[single_quantity_key]["quantity"]

        if not isinstance(single_quantity_key, Quantity) or not isinstance(quantity, Quantity):
            return single_quantity_key

    return most_promising_key
