from typing import List

from . import Quantity
from .utils import quantity_approx_equal, get_list_depth
from .logger import log_info


@log_info
def remove_duplicates(list_quantities: List[Quantity]) -> List[Quantity]:
    """Remove quantities if the are the same. (can be different units, same dimensionality, and approximately same)"""
    list_dim = get_list_depth(list_quantities)
    if list_dim == 0 or list_dim == 1 and len(list_quantities) <= 1 or list_dim == 2 and len(list_quantities[0]) <= 1:
        return list_quantities

    if isinstance(list_quantities[0], list):
        new_list_quantities = []
        for sublist in list_quantities:
            new_list_quantities.append(duplicate_check(sublist))
    else:
        new_list_quantities = duplicate_check(list_quantities)

    return new_list_quantities


def duplicate_check(list_quantities: List[Quantity]) -> List[Quantity]:
    if len(list_quantities) % 2 == 0:
        new_list_quantities = []
        for i in range(int(len(list_quantities)/2)):
            pair = list_quantities[i*2: i*2+2]
            if quantity_approx_equal(pair[0], pair[1]):
                new_list_quantities.append(pair[0])  # approximate same
            else:
                new_list_quantities.append(pair[0])  # different quantities
                new_list_quantities.append(pair[1])

        list_quantities = new_list_quantities

    return list_quantities
