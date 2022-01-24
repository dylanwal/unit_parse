from typing import List, Union, Dict
from enum import Enum, auto

from .config import Quantity
from .utils import quantity_approx_equal, flatten_list


class QuantClass(Enum):
    SINGLE = auto()
    SERIES = auto()
    CONDITIONS = auto()
    SERIES_CONDITIONS = auto()


def reduce_quantities(data_in: Union[Quantity, List[Quantity], List[List[Quantity]]]) -> Quantity:
    if isinstance(data_in, Quantity) or data_in is None or data_in == []:
        return data_in
    if isinstance(data_in, List) and len(data_in) <= 1:
        return data_in[0]

    data_dict = quantity_list_to_dict(data_in)

    return _select_from_data_dict(data_dict)


def quantity_list_to_dict(data_in: List[List[Quantity]]) -> Dict:
    """
    Generates a dict from list inside list, doing some classification.
    out = {
    "Quantity" : {"type": ,"count": }
    }
    """
    data_dict = {}
    for i, data in enumerate(data_in):
        if isinstance(data, Quantity):
            if any([quantity_approx_equal(data, v["quantity"]) for v in data_dict.values()]):
                for k, v in data_dict.items():
                    if quantity_approx_equal(data, v["quantity"]):
                        data_dict[k]["count"] += 1
            else:
                data_dict[i] = {"quantity": data, "count": 1, "type": QuantClass.SINGLE}
        elif isinstance(data, list):
            if isinstance(data[0], list):
                data_dict[i] = {"quantity": data, "count": 1, "type": QuantClass.SERIES_CONDITIONS}
            else:
                if len(data) == 2:
                    data_dict[i] = {"quantity": data, "count": 1, "type": QuantClass.CONDITIONS}
                else:
                    data_dict[i] = {"quantity": data, "count": 1, "type": QuantClass.SERIES}

    return data_dict


def _select_from_data_dict(data_dict: Dict) -> Union[List[Quantity], Quantity]:
    """
    Select the list or Quantity that is most likely to be right.
    Rules: Series_conditions > conditions > single (mean of single)
    """
    if len(data_dict.keys()) == 1:
        return data_dict[0]["quantity"]

    for v in data_dict.values():
        if v["type"] == QuantClass.SERIES_CONDITIONS:
            return v["quantity"]

    for v in data_dict.values():
        if v["type"] == QuantClass.CONDITIONS:
            return v["quantity"]

    single_list = [[v["quantity"]] * v["count"] for v in data_dict.values() if v["type"] == QuantClass.SINGLE]
    single_list = flatten_list(single_list)
    single_list = _filter_out_by_dimensionality(single_list)
    return _get_middle_quantity(single_list)


def _filter_out_by_dimensionality(data_in):
    """ Find most common dimension and filter out any bad ones."""

    unit_dimensionality_count = {}
    for data in data_in:
        if data.dimensionality not in unit_dimensionality_count:
            unit_dimensionality_count[data.dimensionality] = 1
        else:
            unit_dimensionality_count[data.dimensionality] += 1

    most_common_unit = max(unit_dimensionality_count, key=unit_dimensionality_count.get)
    data_in = [data for data in data_in if most_common_unit == data.dimensionality]

    return data_in[0]


def _get_middle_quantity(data_in: Union[Quantity, List[Quantity]]) -> Quantity:
    """ Remove data furthest from average till 1 point left."""
    if isinstance(data_in, Quantity):
        return data_in

    for i in range(len(data_in) - 1):
        data_average = sum([data.to_base_units() for data in data_in]) / len(data_in)
        differance_list = [abs(data.to_base_units() - data_average) for data in data_in]
        data_in.pop(differance_list.index(max(differance_list)))

    return data_in[0]
