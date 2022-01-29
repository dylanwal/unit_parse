from typing import Union, Any
from enum import Enum
import math

from unit_parse.config import Quantity, Unit
from unit_parse.utils import quantity_approx_equal, quantity_difference
from unit_parse.logger import log_debug, log_info, logger


class QuantClass(Enum):
    """ Classifications for data. """
    NUMBER = 0
    SINGLE = 1
    SERIES = 2
    CONDITIONS = 3
    SERIES_CONDITIONS = 4


@log_info
def reduce_quantities(data_in: Any,
                      order: tuple[QuantClass] = (QuantClass.SERIES_CONDITIONS, QuantClass.CONDITIONS,
                                                  QuantClass.SERIES, QuantClass.SINGLE, QuantClass.NUMBER),
                      prefer_unit: Unit = None,
                      ) -> Quantity:
    """ reduce quantities

    First cleaning is done by units, then by data type.

    Unit ordering:
        1) preferred unit
        2) most common unit, Unless it is dimensionless than -->
            2a) take the most common non-dimensionless

    data type ordering:
        1) series condition (the largest series)
        2) conditions
        3) series (the largest series)
        4) single (the highest repeated)
        5) single (middle value)
        6) number (the highest repeated)
        7) number (middle value)

    Parameters
    ----------
    data_in: Any
        data to be cleaned
    order: tuple[int]
        See QuantClass for integer values
    prefer_unit: Unit
        This unit will be preferred when down selecting

    Returns
    -------
    output: Any

    """
    # guard statements
    if not isinstance(data_in, list) or data_in == []:
        return data_in
    if len(data_in) <= 1:
        return data_in[0]

    # generate data_dictionary
    data_dict = quantity_list_to_dict(data_in)

    # if data collapses to a single data_dict, then return early
    if len(data_dict.keys()) == 1:
        return data_dict.popitem()[1]["quantity"]

    # remove bad dimensionality
    data_dict = remove_bad_dim(data_dict, prefer_unit)

    # if data collapses to a single data_dict, then return early
    if len(data_dict.keys()) == 1:
        return data_dict.popitem()[1]["quantity"]

    # select base on ordering
    return _select_from_data_dict(data_dict, order=order)


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
    data_in = clean_data_in(data_in)

    data_dict = {}
    for i, data in enumerate(data_in):
        if isinstance(data, Quantity):
            # if data is similar to existing, increase count
            if any([quantity_approx_equal(data, v["quantity"])
                    for v in data_dict.values() if v["type"] == QuantClass.SINGLE]):
                for k, v in data_dict.items():
                    if quantity_approx_equal(data, v["quantity"]):
                        data_dict[k]["count"] += 1
            else:
                # new data
                data_dict[i] = {"quantity": data, "count": 1, "unit": data.units, "type": QuantClass.SINGLE}

        elif isinstance(data, (int, float)):
            # if data is similar to existing, increase count
            if any([math.isclose(data, v["quantity"], rel_tol=0.05)
                    for v in data_dict.values() if v["type"] == QuantClass.NUMBER]):

                for k, v in data_dict.items():
                    if math.isclose(data, v["quantity"], rel_tol=0.05):
                        data_dict[k]["count"] += 1
            else:
                # new data
                data_dict[i] = {"quantity": data, "unit": Unit(""), "count": 1, "type": QuantClass.NUMBER}

        elif isinstance(data, list):
            if isinstance(data[0], list):
                if len(data) == 1:
                    data_dict[i] = {
                        "quantity": data, "unit": _get_dim(data[0][0]), "count": 1,
                        "type": QuantClass.CONDITIONS
                    }
                else:
                    data_dict[i] = {
                        "quantity": data, "count": 1, "len": len(data[0]), "unit": _get_dim([i[0] for i in data]),
                        "type": QuantClass.SERIES_CONDITIONS
                    }
            else:
                data_dict[i] = {
                    "quantity": data, "count": 1, "len": len(data), "unit": _get_dim(data),
                    "type": QuantClass.SERIES
                }

    return data_dict


def clean_data_in(data_in: list[Any]) -> list[Any]:
    """ Removes list[] of length 1. """
    out = []
    for obj in data_in:
        if isinstance(obj, list):
            if len(obj) == 1:
                if isinstance(obj[0], list):
                    if len(obj[0]) == 1:
                        out.append(obj[0][0])
                    else:
                        out.append(obj)
                else:
                    out.append(obj[0])
            else:
                sub_out = []
                for obj_ in obj:
                    if isinstance(obj_, list):
                        if len(obj_) == 1:
                            sub_out.append(obj_[0])
                        else:
                            sub_out.append(obj_)
                    else:
                        sub_out.append(obj_)
                out.append(sub_out)
        else:
            out.append(obj)

    return out


def _get_dim(obj: Union[int, float, Quantity]):
    if isinstance(obj, Quantity):
        return obj.units
    if isinstance(obj, list):
        unit_ = _get_dim(obj[0])
        for v in obj:
            unit__ = _get_dim(v)
            if unit_ != unit__:
                return None  # removes series that don't have homogenous units
        else:
            return unit_

    return Unit("")


@log_debug
def _select_from_data_dict(data_dict: dict, order: tuple[QuantClass]) \
        -> Union[list[Quantity], Quantity]:
    """
    Select data based on order
    """
    for order_ in order:
        # check if QuantClass in dict in order given by 'order' parameter
        keys_of_hits = [k for k, v in data_dict.items() if order_ == v["type"]]

        if len(keys_of_hits) == 0:  # no QuantClass in data
            continue

        elif len(keys_of_hits) == 1:  # one QuantClass found
            if order_ == QuantClass.SERIES_CONDITIONS or order_ == QuantClass.SERIES or \
                    order_ == QuantClass.CONDITIONS:
                # return data_dict[keys_of_hits[0]]["quantity"]
                return double_check_output(data_dict, keys_of_hits)

            return data_dict[keys_of_hits[0]]["quantity"]

        else:  # two or more of a similar QuantClass found
            if order_ == QuantClass.SERIES_CONDITIONS or order_ == QuantClass.SERIES:
                return double_check_output(data_dict, keys_of_hits)

            elif order_ == QuantClass.CONDITIONS:
                return double_check_output(data_dict, keys_of_hits)

            elif order_ == QuantClass.SINGLE:
                return _get_best_single(data_dict)

            elif order_ == QuantClass.NUMBER:
                return _get_best_number(data_dict)

    else:
        raise ValueError("Order parameter issue.")


def _get_best_single(data_dict: dict):
    single = [[v["count"], v["quantity"]] for v in data_dict.values() if QuantClass.SINGLE == v["type"]]

    # get one with most counts
    max_counts = max(single, key=lambda x: x[0])
    if max_counts[0] > 1:
        return max_counts[1]

    # get one in the middle
    return get_middle_quantity([i[1] for i in single])


def _get_best_number(data_dict: dict):
    single = [[v["count"], v["quantity"]] for v in data_dict.values() if QuantClass.NUMBER == v["type"]]

    # get one with most counts
    max_counts = max(single, key=lambda x: x[0])
    if max_counts[0] > 1:
        return max_counts[1]

    # get one in the middle
    return get_middle_quantity([i[1] for i in single])


@log_debug
def get_middle_quantity(data_in: list[Quantity]) -> Quantity:
    """ Remove data furthest from average till 1 point left."""
    data_in.sort()
    if len(data_in) % 2 == 0:
        index = int(len(data_in) / 2)
    else:
        index = int((len(data_in) - 1) / 2)

    return data_in[index]


def double_check_output(data_dict: dict, most_promising_key: list):
    """ double check output

    Check conditions, series and condition series against single (if there is a popular single).
    If unit dimensions don't match, take single.

    """
    # Check if there is some Single data to check against
    keys_of_hits = [k for k, v in data_dict.items() if QuantClass.SINGLE == v["type"]]
    counts = sum([data_dict[k]["count"] for k in keys_of_hits])
    if counts <= 2:  # if not more than two others, nothing to double-check
        return data_dict[most_promising_key[0]]["quantity"]

    # get most common single unit
    single_quantity = _get_best_single(data_dict)

    best_results = [1, single_quantity]
    for key in most_promising_key:
        smallest_diff = 1
        if data_dict[key]["type"] == QuantClass.SERIES_CONDITIONS:
            # look through SERIES_CONDITIONS for value closest to single_quantity
            for value in data_dict[key]["quantity"]:
                diff = quantity_difference(value[0], single_quantity)
                smallest_diff = diff if diff < smallest_diff else smallest_diff

        elif data_dict[key]["type"] == QuantClass.CONDITIONS:
            smallest_diff = quantity_difference(data_dict[key]["quantity"][0][0], single_quantity)

        else:  # QuantClass.SERIES:
            # look through SERIES for value closest to single_quantity
            for value in data_dict[key]["quantity"]:
                diff = quantity_difference(value, single_quantity)
                smallest_diff = diff if diff < smallest_diff else smallest_diff

        if smallest_diff < best_results[0]:
            best_results = [smallest_diff, data_dict[key]["quantity"]]

    return best_results[1]


@log_debug
def remove_bad_dim(data_dict: dict, prefer_unit: Unit = None) -> dict:
    """

    Remove data that doesn't match the most common dimension

    Parameters
    ----------
    data_dict: dict

    prefer_unit: Unit
        Unit that will be preferred over all others. (If not found, choose most common).

    Returns
    -------

    """
    # remove Nones
    data_dict = {k: v for k, v in data_dict.items() if v["unit"] is not None}

    dims = {}
    for v in data_dict.values():
        dim = v["unit"].dimensionality
        if dim in dims:  # if in dict, increase count
            dims[dim] += v["count"]
        else:
            dims[dim] = v["count"]

    most_common_dim = max(dims, key=dims.get)

    # prefer unit
    skip_flag = True
    if prefer_unit is not None:
        if most_common_dim != prefer_unit.dimensionality:
            most_common_dim = prefer_unit.dimensionality
            skip_flag = False

    # prefer non-dimensionless values first
    if skip_flag and most_common_dim == Unit("") and len(dims) > 1:
        dims.pop(most_common_dim)
        most_common_dim = max(dims, key=dims.get)

    # remove data that doesn't match most common dim
    out_dict = {k: v for k, v in data_dict.items() if v["unit"].dimensionality == most_common_dim}

    # logging
    remove_dict = {k: data_dict[k] for k in set(data_dict) - set(out_dict)}
    if len(remove_dict) >= 1:
        logger.info(f"Remove least common unit: {[v['quantity'] for v in remove_dict.values()]} ")

    return out_dict
